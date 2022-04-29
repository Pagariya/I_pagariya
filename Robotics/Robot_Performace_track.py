#!/usr/bin/env python3


import socket
import sys
from time import time, sleep
#fuer den Parameter Server
from rospy import get_param, set_param, is_shutdown, init_node, Rate, loginfo, logerr, logwarn, logdebug, DEBUG, INFO
import errno
#fuer das Herunterfahren
import subprocess
#fuer die String-Bearbeitung
import string
from datetime import datetime
import logging as log
from subprocess import call
from os import path
#----------Variables----------
#cycletime for sending data
TAKTZEIT = 0.2
#!values are sending the number saved in the parameter
#!messages are checking if the parameter is true/false to send the message
#!texts are sending the string saved in the param


#----------input---------
PARAM_DATA = {'ROBOT_MODE':'/splitbot/robot_mode',
                'KLT_COUNTER_EMPTY':'/splitbot/state_machine/info/depalletized_number/empty_klt',
                'KLT_COUNTER_FILLED':'/splitbot/state_machine/info/depalletized_number/full_klt'}


MAINTENANCE_PARAM =  '/splitbot/maintenance_mode'  ##Needs to be changed for splibot


SYSTEM_SHUTDOWN =  '/splitbot/shutdown'   

#---------output---------
#oee as float: 96.5
#date as str '2020.12.08' for 2020 Dec. 08
#system running time in s
#!value output to rosparam



DATA_VALUE_DICT = {                                    
    'oee_tech':'/ipst/data/oee_tech',
    'oee_orga':'/ipst/data/oee_orga',
    'error_counter':'/ipst/data/error_counter',
    'klt_counter_empty':'/ipst/data/klt_counter_empty',
    'klt_counter_filled':'/ipst/data/klt_counter_filled',
    'robot_mode_id':'/ipst/data/robot_mode_id'
}




#!messages output to rosparam
#M=Meldung(ohne Ausfallzeit);T=Technische Stoerung;I=Geplante Instandhaltung
#O=Organisatorische Stoerung;Z=Warnung(ohne Ausfallzeit)

DATA_MESSAGE_DICT = {
    'technical_error':'/ipst/data/technical_error',
    'organizational_error':'/ipst/data/organizational_error'}




#-------in/out-----
YAML_CONFIG = {                 ##All relevant data
    'config_date':'/ipst/yaml/config_date',
    'config_error_counter':'/ipst/yaml/config_error_counter',
    'config_klt_counter_empty':'/ipst/yaml/config_klt_counter_empty',
    'config_klt_counter_filled':'/ipst/yaml/config_klt_counter_filled',
    'config_oee_tech':'/ipst/yaml/config_oee_tech',
    'config_oee_orga':'/ipst/yaml/config_oee_orga',
    'config_runtime':'/ipst/yaml/config_runtime',
    'config_orga_err_time':'/ipst/yaml/config_orga_err_time',
    'config_maint_time':'/ipst/yaml/config_maint_time',
    'send_config_flag':'/ipst/data/send_config_flag'                       ### What is this used for
    }



YAML_FILE = path.dirname(path.realpath(__file__)) + '/ipst_config_splitbot.yaml'



#-------------------
#!Used for displaying errors on the system for efficiency calculation                         ##Show error
ROBOT_MODES = { 'NORMAL':('RUNNING', 'WAITING_FOR_USER', 'BOOTING', 'POWER_OFF'),
 'ERROR':('PROBLEM', 'PROTECTIVE_STOP', 'EMERGENCY_STOP', 'VIOLATION/FAULT', 'UNKOWN_STATUS')}


#maximum error resolving time in seconds
MAX_ERROR_TIME = 180


#cycle time for date checking and yaml saving
CONFIG_CYCLE_TIME = 15.0



#!rosparam-yaml config
#saving and loading yaml config
PARAM_SAVE_COMMAND = ["rosparam", "dump", YAML_FILE, "/ipst/yaml"]
PARAM_LOAD_COMMAND = ["rosparam", "load", YAML_FILE, "/ipst/yaml"]





class  performance_tracking():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def __init__(self):
        #self.logging configuration
        #self.logging = log.getLogger('performance_tracking')
        #self.logging.setLevel(log.DEBUG)
        #log.basicConfig(level=log.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        #log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        #log.basicConfig(level=log.WARN, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        #log.basicConfig(level=log.ERROR, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ros_error = False
        while not ros_error:
            try:
                get_param('/test', None)
                ros_error = True
            except socket.error:
                ros_error = False
                logerr('--- roscore is down ---')
                sleep(TAKTZEIT)
                
        #load yaml config
        call(PARAM_LOAD_COMMAND)
        self.date_today = self.get_date_today()
        #flag if robot is in error
        self.robot_in_error_save = None
        #!variables for resetting error after the max time
        #timestamp when the error first appeared
        self.error_appearence_time = 0
        #flag if error has to be resetted, after max error time
        self.error_appearence_reset = False
        #timestamp since last update of error time
        self.oee_time_error_save = 0
        #---OEE tech. calculation---
        #timestamp since starting robot
        self.oee_time_start = time()
        #leftover variable, not in use right now
        self.oee_time_error = 0.0
        self.oee_tech, self.oee_orga, self.runtime_today, self.maintenance_time, self.abs_error_counter, self.klt_abs_empty,  self.klt_abs_filled, self.orga_error_time = self.get_yaml_config()
        
        
        #initially set all parameters
        set_param(DATA_VALUE_DICT['oee_tech'], self.oee_tech)
        set_param(DATA_VALUE_DICT['oee_orga'], self.oee_orga)
        set_param(DATA_VALUE_DICT['error_counter'], self.abs_error_counter)
        set_param(DATA_VALUE_DICT['klt_counter_empty'], self.klt_abs_empty)
        set_param(DATA_VALUE_DICT['klt_counter_filled'], self.klt_abs_filled)
        set_param(YAML_CONFIG['send_config_flag'], False)
        #--------------------------
        #tracking current klt counter
        self.klt_pallet_counter_empty = None
        self.klt_pallet_counter_filled = None
        

        
        #saving the klt amounts while error appeared [empty, filled];
        #to determine, if error happened in the same klt or not
        self.error_appearence_klt_save = [None, None]                              ###need to watch out here

        #timestamp for config saving
        self.config_timestamp = None


        #---maintenance---
        #shows if maintenance got called and is already registered by program
        self.maintenance_flag = False
        self.maintenance_timestamp = None
        #--------oee_orga--------
        self.orga_error_timestamp = None
        self.orga_error_flag = False

 
    def main(self):
        #--------Errors----------
        self.set_error_param()
        #------klt counter------
        self.set_klt_counter()
        #------maintenance call-------
        self.maintenance_time, self.maintenance_flag, self.maintenance_timestamp = self.maintenance_check(self.maintenance_time, self.maintenance_flag, self.maintenance_timestamp)
        #---------Check Config----------
        #check config timestamp
        if (self.config_timestamp is None or (time() - self.config_timestamp) > CONFIG_CYCLE_TIME):
            #different date?
            if get_param(YAML_CONFIG['config_date']) != datetime.now().strftime('%Y.%m.%d'):
                loginfo('--- beginning new day with OEE: 100% ---')
                self.oee_tech, self.oee_orga, self.runtime_today, self.maintenance_time, self.abs_error_counter, self.klt_abs_empty,  self.klt_abs_filled, self.orga_error_time = self.get_yaml_config()
                set_param(DATA_VALUE_DICT['oee_tech'], self.oee_tech)
                set_param(DATA_VALUE_DICT['oee_orga'], self.oee_orga)
                set_param(DATA_VALUE_DICT['error_counter'], self.abs_error_counter)
                set_param(DATA_VALUE_DICT['klt_counter_empty'], self.klt_abs_empty)
                set_param(DATA_VALUE_DICT['klt_counter_filled'], self.klt_abs_filled)
                set_param(YAML_CONFIG['send_config_flag'], False)
            #same date
            else:
                self.set_yaml_config()
        #---------OEE-----------
        self.oee_tech = self.get_oee_tech(self.runtime_today, self.maintenance_time, (self.klt_abs_empty+self.klt_abs_filled), self.abs_error_counter)
        self.oee_orga = self.get_oee_orga(self.runtime_today, self.orga_error_time)
        #-----------------------
        logdebug('oee_tech: %s; oee_orga: %s; err_count: %s; runtime: %s, err_orga_time: %s, m_time: %s; #empty: %s; #filled: %s',
            str(self.oee_tech), str(self.oee_orga), str(self.abs_error_counter), str(self.runtime_today), str(self.orga_error_time), str(self.maintenance_time),str(self.klt_abs_empty),  str(self.klt_abs_filled))
        #check for system shutdown
        try:
            if not get_param(SYSTEM_SHUTDOWN, True):

                self.close()
                
        except (KeyError, socket.error) as error:
            logwarn('--- system shutdown error: %s ---',error)
        sleep(TAKTZEIT)


    def get_oee_tech(self, runtime, maintenance_time, klt_stacked, errors):
        '''
        returns calculated oee tech
        '''
        #self.logging.debug('--- get_oee_tech with runtime: {}, maint_time:{}, klt: {}, errors: {}'.format(runtime, maintenance_time, klt_stacked, errors))
        try:
            if runtime > maintenance_time and klt_stacked > 0:
                oee_tech = round((1.0 - float(maintenance_time)/float(runtime))*(1.0-float(errors)/float(klt_stacked))*100.0, 2)
            elif runtime > maintenance_time:
                oee_tech = round(((float(runtime) - float(maintenance_time))/float(runtime))*100.0, 2)
            else:
                oee_tech = 0.0
        except ZeroDivisionError:
            oee_tech = 0.0
            logwarn('--- oee_tech: system running time is at zero ---')
        if oee_tech > 100.0 or oee_tech < 0.0:
            logwarn('--- oee_tech value is outside logical borders: %s ---',str(oee_tech))
            oee_tech = 0.0
        set_param(DATA_VALUE_DICT['oee_tech'], oee_tech)
        return oee_tech

    def get_oee_orga(self, runtime, error_time):
        '''
        returns calculated oee_orga
        '''
        try:
            if runtime > error_time:
                oee_orga = round((1.0-float(error_time)/float(runtime))*100.0, 2)
            else:
                oee_orga = 0.0
        except ZeroDivisionError:
            oee_orga = 0.0
            logwarn('--- oee_orga: system running time is at zero ---')
        if oee_orga > 100.0 or oee_orga < 0.0:
            logwarn('--- oee_orga value is outside logical borders: %s ---',str(oee_orga))
            oee_orga = 0.0
        set_param(DATA_VALUE_DICT['oee_orga'], oee_orga)
        return oee_orga

    def maintenance_check(self, maint_time_now, maint_flag, maint_timestamp):
        '''
        input: current maintenance_time
        used to check if maintenance mode is on & update maintenance time;
        flag shows an already detected maintenance call
        returns current time the robot was in maintenance (s)
        '''
        #maintenance call on & flag true?
        if get_param(MAINTENANCE_PARAM, False) and maint_flag:
            maint_time_now += round(time()-maint_timestamp, 2)
            maint_timestamp = time()
        #maintenance call off & flag true?
        elif not get_param(MAINTENANCE_PARAM, False) and maint_flag:
            maint_time_now += round(time()-maint_timestamp, 2)
            maint_timestamp = None
            maint_flag = False
        #maintenance call on & flag false?
        elif get_param(MAINTENANCE_PARAM, False) and not maint_flag:
            maint_flag = True
            maint_timestamp = time()
        #maintenance off & flag false
        else:
            maint_flag = False
            maint_timestamp = None
        #logging.debug('maintenance_check: maintenance_time: {}'.format(maint_time_now))
        return maint_time_now, maint_flag, maint_timestamp

    def set_error_param(self):
        '''
        setting error parameter on rosparam, if robot state changed
        '''
        #get error state & rosparam data
        robot_in_error = self.is_robot_in_error()
        #get KLT amount [empty, filled]
        klt_counter = self.get_klt_amount()
        #robot_in_error changed?
        #self.logging.debug('set_error_param: rob_err: {}, err_reset: {}, org_stamp: {}'.format(robot_in_error, self.error_appearence_reset, self.orga_error_timestamp))
        if not robot_in_error is None:
            #error appeared and KLT amount changed since last error?
            if robot_in_error and self.error_appearence_klt_save != klt_counter:
                self.abs_error_counter +=1
                self.error_appearence_klt_save = klt_counter
                set_param(DATA_MESSAGE_DICT['technical_error'], True)
                set_param(DATA_MESSAGE_DICT['organizational_error'], False)
                set_param(DATA_VALUE_DICT['error_counter'], self.abs_error_counter)
            #switches to organizational error?
            elif self.error_appearence_reset and robot_in_error == False:
                set_param(DATA_MESSAGE_DICT['technical_error'], False)
                set_param(DATA_MESSAGE_DICT['organizational_error'], True)
                #set orga_error
                self.orga_error_flag = True
                self.orga_error_timestamp = time()
            #normal mode?
            elif robot_in_error == False:
                set_param(DATA_MESSAGE_DICT['technical_error'], False)
                set_param(DATA_MESSAGE_DICT['organizational_error'], False)
                self.orga_error_flag = False
        #check for orga error continually and update time
        if self.orga_error_flag and self.orga_error_timestamp is not None and not self.maintenance_flag:
            self.orga_error_time += round(time() - self.orga_error_timestamp, 2)
            self.orga_error_timestamp = time()
        else:
            self.orga_error_timestamp = None

    def set_klt_counter(self):
        klt_update = self.get_klt_update()
        #!
        self.klt_abs_empty += klt_update[0]
        self.klt_abs_filled += klt_update[1]
        set_param(DATA_VALUE_DICT['klt_counter_empty'], self.klt_abs_empty)
        set_param(DATA_VALUE_DICT['klt_counter_filled'], self.klt_abs_filled)

    def is_robot_in_error(self):
        '''
        function to decide whether the robot is running normally or in error and updating timevars;
        after a static amount of time technical error is being switched to an organizational error;
        returning only the latest change, if nothing changed then None will be returned
        '''
        #flag for robot mode id, will be set to param server at return
        robot_mode_id = 0

        
        #update time in automatic mode
        self.runtime_today += round(time()-self.oee_time_start, 2)
        self.oee_time_start = time()



        #update time in error and error appearence time if robot in error
        if self.robot_in_error_save == True and self.error_appearence_reset == False and not self.oee_time_error_save is None:
            self.oee_time_error += round(time()-self.oee_time_error_save, 1)
            self.oee_time_error_save = time()
        #error has to be reset after reaching max time?
        if self.robot_in_error_save and not self.error_appearence_time is None:
            if (time()-self.error_appearence_time) > MAX_ERROR_TIME:


                self.error_appearence_reset = True              ###########################


                #print('\n\n\n\--- resetting error! ---\n\n\n')
        else:
            self.error_appearence_reset = False
        #getting robot state and check if robot is in error
        try:
            robot_mode = get_param(PARAM_DATA['ROBOT_MODE'], 'PROBLEM')
            if robot_mode in ROBOT_MODES['NORMAL']:
                robot_in_error = False
                robot_mode_id = 1
            elif robot_mode in ROBOT_MODES['ERROR']:
                robot_in_error = True
                robot_mode_id = 2
            else:
                logwarn('--- unknown robot mode present ---')
                robot_in_error = True
                robot_mode_id = 2
                #if robot_mode == PALLET_FULL:
                   #robot_mode_id = 3 
            set_param(DATA_VALUE_DICT['robot_mode_id'], robot_mode_id)
        except (KeyError, socket.error) as err:
            logerr('--- parameter server offline/parameter not set yet: %s ---',str(PARAM_DATA['ROBOT_MODE']))
            robot_in_error = True
            sleep(TAKTZEIT/2.0)
        #print('robot in error save: {}, robot_in_error: {}'.format(self.robot_in_error_save, robot_in_error))
        #error changed?
        if self.robot_in_error_save != robot_in_error:
            self.robot_in_error_save = robot_in_error
            if robot_in_error:
                #set error timestamp
                self.error_appearence_time = time()
                self.oee_time_error_save = self.error_appearence_time
            else:
                self.error_appearence_reset = False
            return robot_in_error
        #error not changed, but has to be reset?
        elif self.error_appearence_reset:
            self.error_appearence_time = None
            self.oee_time_error_save = self.error_appearence_time
            return False
        return None

    def get_klt_amount(self):
        '''
        returns amount of KLT [empty, filled]
        '''
        try:
            klt_counter = [get_param(PARAM_DATA['KLT_COUNTER_EMPTY'], 0),  get_param(PARAM_DATA['KLT_COUNTER_FILLED'], 0)]
        except (KeyError, socket.error) as err:
            logerr('--- parameter server offline/parameter not set yet: klt counter empty/filled ---')
            sleep(TAKTZEIT/2.0)
            klt_counter = [0, 0]
        return klt_counter

    def close(self):
        logwarn('--- terminating performance_tracking.py ---')
        self.set_yaml_config()
        quit()

    def get_date_today(self):
        return datetime.now().strftime('%Y.%m.%d')

    def get_yaml_config(self):
        '''
        get data saved inside the yaml-file through rosparam
        and check if date has changed;
        if so, send yesterdays oee value to ipst and reset to 100%
        return:
        oee as float, system_time as dint?, error_time as int,
        abs error counter as int, abs klt counter empty/filled as int
        '''
        #get data
        date_today = self.get_date_today()
        config_date = get_param(YAML_CONFIG['config_date'])
        config_oee_tech = float(get_param(YAML_CONFIG['config_oee_tech']))
        config_oee_orga = float(get_param(YAML_CONFIG['config_oee_orga']))
        config_runtime = int(get_param(YAML_CONFIG['config_runtime']))
        config_abs_error = int(get_param(YAML_CONFIG['config_error_counter']))
        config_abs_klt_empty = int(get_param(YAML_CONFIG['config_klt_counter_empty']))
        config_abs_klt_filled = int(get_param(YAML_CONFIG['config_klt_counter_filled']))
        config_orga_err_time = float(get_param(YAML_CONFIG['config_orga_err_time']))
        time_in_maintenance = float(get_param(YAML_CONFIG['config_maint_time']))

        #---------------------------------
        #same date as today?
        if date_today == config_date:
            loginfo('--- same day ---')
            output = [config_oee_tech, config_oee_orga, config_runtime, time_in_maintenance, config_abs_error, config_abs_klt_empty, config_abs_klt_filled, config_orga_err_time]
        else:
            #if different day, set config flag to true, wait until ipst.py will upload config data from rosparam and reset flag to false, overwrite rosparam
            #& reset config file
            loginfo('--- different day ---')
            #set flag and wait while ipst sends data and reset flag
            set_param(YAML_CONFIG['send_config_flag'], True)
            while get_param(YAML_CONFIG['send_config_flag']) != False:
                loginfo('--- sending config to ipst... ---')
                sleep(TAKTZEIT*10)
            set_param(YAML_CONFIG['config_date'], date_today)
            self.date_today = date_today
            set_param(YAML_CONFIG['config_oee_tech'], 100.0)
            set_param(YAML_CONFIG['config_oee_orga'], 100.0)
            set_param(YAML_CONFIG['config_runtime'], 0.0)
            set_param(YAML_CONFIG['config_error_counter'], 0)
            set_param(YAML_CONFIG['config_klt_counter_empty'], 0)
            set_param(YAML_CONFIG['config_klt_counter_filled'], 0)
            set_param(YAML_CONFIG['config_orga_err_time'], 0.0)
            set_param(YAML_CONFIG['config_maint_time'], 0.0)
            output =[100.0, 100.0, 0, 0, 0, 0, 0, 0.0]
        return output

    def set_yaml_config(self):
        '''
        set data to the rosparam server and save them inside yaml file
        '''
        loginfo('--- saving configuration: ---\noee_tech: %s\noee_orga: %s\ndate: %s\nruntime: %s\nabs_err_counter: %s\nklt_empty: %s\nklt_filled: %s',self.oee_tech,
            str(self.oee_orga), str(self.date_today), str(self.runtime_today), str(self.abs_error_counter), str(self.klt_abs_empty), str(self.klt_abs_filled))
        set_param(YAML_CONFIG['config_date'], self.date_today)
        set_param(YAML_CONFIG['config_oee_tech'], self.oee_tech)
        set_param(YAML_CONFIG['config_oee_orga'], self.oee_orga)
        set_param(YAML_CONFIG['config_runtime'], round(self.runtime_today, 2))
        set_param(YAML_CONFIG['config_error_counter'], self.abs_error_counter)
        set_param(YAML_CONFIG['config_klt_counter_empty'], self.klt_abs_empty)
        set_param(YAML_CONFIG['config_klt_counter_filled'], self.klt_abs_filled)
        set_param(YAML_CONFIG['config_orga_err_time'], round(self.orga_error_time, 2))
        set_param(YAML_CONFIG['config_maint_time'], round(self.maintenance_time, 2))
        #saving rosparam ipst data to yaml file
        call(PARAM_SAVE_COMMAND)
        #saving config timestamp
        self.config_timestamp = time()

    def get_klt_update(self):
        '''
        check if klt amount has been changed
        returns the change:
        klt_empty/filled as int
        return: either 1 if klt added or 0
        '''
        add_klt_empty = 0
        add_klt_filled = 0
        #get current klt amounts
        klt_empty, klt_filled = self.get_klt_amount()
        if klt_empty == 0 and klt_filled == 0:
            self.klt_pallet_counter_empty = 0
            self.klt_pallet_counter_filled = 0
            return [0, 0]
        #check if initial run of program
        if self.klt_pallet_counter_empty is None or self.klt_pallet_counter_filled is None:
            self.klt_pallet_counter_empty = klt_empty
            self.klt_pallet_counter_filled = klt_filled
        #check if someone reseted klt counter manually from UI    
        if klt_empty < self.klt_pallet_counter_empty:
            self.klt_pallet_counter_empty = klt_empty
            loginfo('--- empty klt counter resetted ---')
        #check if klt counter changed to increase klt nr
        elif self.klt_pallet_counter_empty < klt_empty:
            self.klt_pallet_counter_empty = klt_empty
            add_klt_empty = 1
            loginfo('--- empty klt depallatised ---')
        #check if someone resetted klt counter manually form ui
        if klt_filled < self.klt_pallet_counter_filled:
            self.klt_pallet_counter_filled = klt_filled
            loginfo('--- filled klt counter  resetted ---')
        #check if klt counter changed to increase klt nr
        elif self.klt_pallet_counter_filled < klt_filled:
            self.klt_pallet_counter_filled = klt_filled
            add_klt_filled = 1
            loginfo('--- filled klt depallatised ---')
        return add_klt_empty, add_klt_filled


if __name__ == '__main__':
    init_node('perf_track_node', anonymous=False, log_level=INFO)
    client = performance_tracking()
    try:
        while not is_shutdown():
            try:
                client.main()
            except (KeyError, socket.error) as error:
                print('--- main error: {} ---'.format(error))
                sleep(2.0)
    except KeyboardInterrupt:
        client.close()
        quit()
