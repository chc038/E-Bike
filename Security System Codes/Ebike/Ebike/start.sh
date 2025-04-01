#run ebike programs
#copy using ln start.sh new.sh, than rename and move new.sh
cd /home/pi/Ebike
pwd

#input output
python3 io_inputs.py&
python3 io_outputs.py&
python3 io_turn_signal.py&
python3 io_adc.py&
python3 io_vesc.py&
python3 screen_management.py&

#important information
python3 accelerometer.py&
python3 gps_module.py&

#camera
python3 camera_0.py&

#gui
python3 gui_display.py&

#email
#python3 email_reader.py&
python3 email_sender.py&

#security
python3 virtual_fence.py&
python3 vibration_detection.py&

#check stuff
python3 batteries_check.py&

#other
python3 delete_old_file.py&
python3 charger.py&

#wait to quit program
bash wait_to_quit.sh
