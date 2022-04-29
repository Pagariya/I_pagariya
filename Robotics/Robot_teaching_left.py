#!/usr/bin/env python3 




import tkinter as tk
import yaml
from time import sleep 
#from urx.urrobot import URRobot
import urx.urrobot as urrobot
import logging 
import sys
import os


a = 0.5
v = 0.5
rob = urrobot.URRobot('192.168.0.3', enable_rtde_input=True)
window = tk.Tk()
window.geometry("1000x800")  # Size of the window 
window.title("Robot Teaching")  # Adding a title

### Text parameter


right_robot_param_file = '/home/robotics/Desktop/software-sortbot/sortbot_ws/src/sortbot_state_machine/include/sortbot_7/sortbot_motion_right_3147.yaml'

left_robot_param_file = '/home/robotics/Desktop/software-sortbot/sortbot_ws/src/sortbot_state_machine/include/sortbot_7/sortbot_motion_left_3147.yaml'

inno_garage_file = '/home/q521154/Desktop/Desktop/sortbot_motion_left_4147.yaml'


#Mention the yaml file according to robot


yaml_file = left_robot_param_file





text_update_position = 'Gespeicherte position aktualisiert' #Gespeicherte position aktualisiert  #'Saved Position Updated'

text_to_guide_to_select_one_option_in_drop_down_menu = 'Bearbeitung punkt'              #Wählen Sir eine   #'Select One'

text_to_go_to_saved_position= 'Zur gespeicherten position'  #Zur gespeicherten position  #'Go to saved position'

text_to_save_current_robot_position = 'Aktuelle Roboterposition speichern' #Aktuelle Roboterposition speichern #"Save current robot position"

text_to_show_saved_position =  'Gespeicherte Gelenkposition [rad]' #Gespeicherte Gelenkposition  #"Saved Joint Position"

text_to_show_saved_end_effector_position =  'Gespeicherte Endeffektorposition [mm][rad] ' #Gespeicherte Endeffektorposition  #"Saved End Effector Position"

text_to_show_updated_real_time_position =  'Echtzeit-Roboterposition anzeigen' #Echtzeit-Roboterposition anzeigen  #"Show Robot's real time position"

text_to_show_current_robot_joint_position =  'Aktuelle Gelenkposition [rad]' #Aktuelle Gelenkposition  #"Current joint Position"

text_to_show_current_robot_endeffector_position=  'Aktuelle Endeffektorposition [mm][rad]' #Aktuelle Endeffektorposition  #"Current End Effector Position"

text_to_undo = 'Rückgängig'

text_to_undo_text = 'Rückgängig Erfolgreich'




print(rob.is_normal_mode())
print(rob.get_safety_status())

print(rob.get_runtime_state())
print(rob.is_running()) #(true if robot power on or idle)



def yaml_data():
    with open(yaml_file) as file:
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)

    list_position = []
    list_movement = []

    current_point_data = {} 

    for item, doc in fruits_list.items():
            if item == 'positions':
                for x,y in doc.items():
                    list_position.append(x)
                current_point_data = doc 

            if item == 'movements':
                for x,y in doc.items():
                    list_movement.append(x)

    
    file.close()       
    
    return list_position, list_movement,  current_point_data




def my_show(*args): ##function called when options value changes
    str_out.set(options.get())
    _, _, current_point_data= yaml_data()
    label_3_1_6.config(text = current_point_data[options.get()][0])
    label_3_1_3.config(text = current_point_data[options.get()][1])
    label_3_2_8.config(text = '',bg="gray30", fg="snow" )
    return options.get()



def my_show_(*args): ##function called when options value changes
    str_out1.set(options1.get())
    return options1.get()


def my_show2(*args): ##function called when options value changes
    str_out2.set(options2.get())
        
    with open(yaml_file) as file:

        fruits_list = yaml.load(file, Loader=yaml.FullLoader)

    list2 = []
    for item, doc in fruits_list.items():
            if item == 'movements':
                for x,y in doc.items():
                  if x == options2.get():
                      if isinstance(y[0], list):
                          len_list = len(y[0])
                          for i in range(len_list):
                              list2.append(y[0][i][0])
                              list2.append(y[0][i][4])


    for i in range(1):
       for j in range(2, 3):
            window.columnconfigure(j, weight=1, minsize=100)
            window.rowconfigure(i, weight=1, minsize=100)
            frame_5 = tk.Frame(
                master=window,
                highlightbackground="black", highlightthickness=1
            )
            frame_5.grid(row=i, column=j, padx=5, pady=5)

            if i == 0 and j == 2:
                my_list_3 = list2
                options3 = tk.StringVar(frame_5)
                options3.set('Movement info') # default value
                om3 =tk.OptionMenu(frame_5, options3, *my_list_3)
                om3.grid()
                om3.config(bg="gray30", fg="snow", width = 10)
                str_out3=tk.StringVar(frame_5)
                str_out3.set("Output3")

    return options2.get()


#Function to make robot move 
def go_to_saved_position():
    point_name = my_show()
    _ , _,current_point_data = yaml_data()
    joint_pos = current_point_data[point_name][0]
    endeff_pos = current_point_data[point_name][1]

    #move robot to saved point
    if options1.get() == 'movej':
        rob.movej(joint_pos, a, v, True)
    else:
        rob.movel(endeff_pos, a, v, True)


#Function to save the current robot position
def replace_and_save_current_position():
    with open(yaml_file) as file:
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)
          
    
    for item, doc in fruits_list.items():
        if item == 'positions':
            replace_and_save_current_position.temp = doc[my_show()] 
            replace_and_save_current_position.temp_point = my_show()
            doc[my_show()] = [[round(val, 4) for val in rob.getj()], [round(val, 4) for val in rob.getl()]] 

            
    with open(yaml_file, 'w') as file:
        yaml.dump(fruits_list, file,sort_keys=False) 
    

    _, _, current_point_data = yaml_data()
    label_3_1_6.config(text = current_point_data[options.get()][0])
    label_3_1_3.config(text = current_point_data[options.get()][1])
    label_3_2_8.config(text = text_update_position,bg="gray30", fg="snow" )
    file.close()  
    

def movement_list():
    return list2
    

def undo():

    with open(yaml_file) as file:
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)
          
    
    for item, doc in fruits_list.items():
        if item == 'positions':
            if my_show() == replace_and_save_current_position.temp_point:
                doc[my_show()] = replace_and_save_current_position.temp
                with open(yaml_file, 'w') as file:
                    yaml.dump(fruits_list, file, sort_keys=False) 

                _, _, current_point_data = yaml_data()
                label_3_1_6.config(text = current_point_data[options.get()][0])
                label_3_1_3.config(text = current_point_data[options.get()][1])
                label_3_2_8.config(text = text_to_undo_text,bg="gray30", fg="snow" )
                file.close()  

            else: 
                label_3_2_8.config(text = 'Unmöglich',bg="gray30", fg="snow" )
                break
def close():
   os._exit(0)


def stop():
    rob.stop()            


#updates the current robot data on GUI
def  update_current_robot_pose_data():
    label_3_1.config(text = [round(val, 4) for val in rob.getl()])
    label_3_1_2.config(text = [round(val, 4) for val in rob.getj()])
    



for i in range(1):
    for j in range(3):
        window.columnconfigure(j, weight=1, minsize=100)
        window.rowconfigure(i, weight=1, minsize=100)
        frame_1 = tk.Frame(
            master=window,
            highlightbackground="black", highlightthickness=1
        )
        frame_1.grid(row=i, column=j, padx=5, pady=5)
        if i == 0 and j == 0:
            list_1, _, _  = yaml_data()
            my_list = sorted(list_1)
            options = tk.StringVar(frame_1)
            options.set(text_to_guide_to_select_one_option_in_drop_down_menu) # default value

            om1 =tk.OptionMenu(frame_1, options, *my_list)
            om1.grid()
            om1.config(bg="gray30", fg="snow", width = 23)
            str_out=tk.StringVar(frame_1)
            str_out.set(my_list[0])
            
            
        if i == 0 and j == 1:
            _, list_2, _  = yaml_data()
            my_list_2 = list_2
            options2 = tk.StringVar(frame_1)
            options2.set('Movement Info') # default value

            om3 =tk.OptionMenu(frame_1, options2, *my_list_2)
            om3.grid()
            om3.config(bg="gray30", fg="snow", width = 18)
            str_out2=tk.StringVar(frame_1)
            str_out2.set("Output3")







for i in range(1,2):
    for j in range(3):
        window.columnconfigure(j, weight=1, minsize=100)
        window.rowconfigure(i, weight=1, minsize=100)
        frame_2 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            highlightbackground="black", highlightthickness=1
        )
        
        frame_2.grid(row=i, column=j, padx=5, pady=5)

        if i == 1 and j == 0:
          
            label_3_1_5 = tk.Label(frame_2 , text=text_to_show_saved_end_effector_position, width=40 ,  height=1,font=("Times", "15", "bold"), bg="gray30", fg="snow" )
            label_3_1_5.grid()
            label_3_1_8 = tk.Label(frame_2 , text="  X,          Y,       Z,       RX,      RY,     RZ", width=40 ,  font=("Times", "15", "bold") )
            label_3_1_8.grid()
            label_3_1_3 = tk.Label(frame_2 , text='TEST', bg="gray30", fg="snow", width=40 , height=1, font=("Times", "15", "bold"), padx=5, pady=5  )
            label_3_1_3.grid()


        if i == 1 and j == 1:
            label_3_2 = tk.Label(frame_2 , text=text_to_show_saved_position, width=40 ,height=1,  font=("Times", "15", "bold") , bg="gray30", fg="snow" )
            label_3_2.grid()
            label_3_1_7 = tk.Label(frame_2 , text="1,          2,           3,          4,          5,         6", width=40 ,  font=("Times", "15", "bold") )
            label_3_1_7.grid()
            label_3_1_6 = tk.Label(frame_2, text='TEST', bg="gray30", fg="snow", width=40 ,height=1, font=("Times", "15", "bold"), padx=5, pady=5  )
            label_3_1_6.grid()
      


for i in range(2,3):
    for j in range(3):
        window.columnconfigure(j, weight=1, minsize=100)
        window.rowconfigure(i, weight=1, minsize=100)
        frame_3 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            highlightbackground="black", highlightthickness=1
        )
        
        frame_3.grid(row=i, column=j, padx=5, pady=5)

        if i == 2 and j == 0:
           label_3 = tk.Label(frame_3, text=text_to_show_current_robot_endeffector_position, width=40 , height=1,font=("Times", "15", "bold"), bg="gray30", fg="snow")
           label_3.grid()
           label_3_1_9 = tk.Label(frame_3 , text="  X,          Y,       Z,       RX,      RY,     RZ", width=40 ,  font=("Times", "15", "bold") )
           label_3_1_9.grid()
           label_3_1 = tk.Label(frame_3 , text= 'TEST', bg="gray30", fg="snow", width=40 ,height=1, font=("Times", "15", "bold"), padx=5, pady=5)
           label_3_1.grid()

        if i == 2 and j == 1:
           label_3_1_1 = tk.Label(frame_3 , text=text_to_show_current_robot_joint_position, width=40 , height=1, font=("Times", "15", "bold") , bg="gray30", fg="snow" )
           label_3_1_1.grid()
           label_3_1_1_1 = tk.Label(frame_3 , text="1,          2,           3,          4,          5,         6", width=40 ,  font=("Times", "15", "bold") )
           label_3_1_1_1.grid()
           label_3_1_2 = tk.Label(frame_3 , text = 'TEST', bg="gray30", fg="snow", width=40,height=1, font=("Times", "15", "bold") , padx=5, pady=5 )        
           label_3_1_2.grid()



for i in range(3,5):
    for j in range(3):
        window.columnconfigure(j, weight=1, minsize=100)
        window.rowconfigure(i, weight=1, minsize=100)
        frame_4 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )     
        frame_4.grid(row=i, column=j, padx=5, pady=5)
        if i == 3 and j == 0:
            update_current_robot_pose_data()
            button_2 = tk.Button(frame_4, text=text_to_show_updated_real_time_position, width=30, height=1, bg="gray30", fg="snow", command=update_current_robot_pose_data, font=("Times", "15", "bold") )
            button_2.grid()  

        if i == 3 and j == 2:
            button_4 = tk.Button(frame_4, text=text_to_undo, width=10,  bg="gray30", fg="snow", command=undo, font=("Times", "12", "normal") )
            button_4.grid()  

        if i == 4 and j == 0:
            my_list = ['movej', 'movel']
            options1 = tk.StringVar(frame_1)
            options1.set('select') # default value

            om2 =tk.OptionMenu(frame_4, options1, *my_list)
            om2.grid()
            om2.config(bg="gray30", fg="snow", width = 10)
            str_out1=tk.StringVar(frame_4)
            str_out1.set("Output4")

        if i == 4 and j == 1:
            button_2 = tk.Button(frame_4, text=text_to_go_to_saved_position, width=30, height=1, bg="gray30", fg="snow", command=go_to_saved_position, font=("Times", "15", "bold") )
            button_2.grid()  

        if i == 3 and j == 1:
            button_3 = tk.Button(frame_4, text=text_to_save_current_robot_position, width=30, height=1,bg="gray30", fg="snow", command=replace_and_save_current_position , font=("Times", "15", "bold")  )
            button_3.grid()  

            label_3_2_8 = tk.Label(frame_4, text="", width=30 ,  font=("Times", "15", "bold")  )
            label_3_2_8.grid() 

        if i == 4 and j == 1:
            exit_button2 = tk.Button(frame_4, text = 'Stop', command = stop,  width=10, height=1, bg="gray30", fg="snow",  )
            exit_button2.grid()   

        if i == 4 and j == 2:
            exit_button = tk.Button(frame_4, text = 'Exit', command = close,  width=10, height=1, bg="gray30", fg="snow",  )
            exit_button.grid()   
    
        

options.trace('w',my_show)
options1.trace('w',my_show_)
options2.trace('w',my_show2)



window.mainloop()




