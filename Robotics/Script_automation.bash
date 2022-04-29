#!/bin/bash
 



echo First Group:

source /opt/ros/noetic/setup.bash 

wait 




echo second Group:

roscore &

(sleep 10 ; gnome-terminal -e 'sh -c "python3  perf_track_Splitbot.py; exec bash"') &

(sleep 9 ; rosparam set /splitbot/display_mode 'RUNNING') &

(sleep 20 ; gnome-terminal -e 'sh -c "python3  test_4.py; exec bash"') 



wait 
 

