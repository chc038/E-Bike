import shutil
import time
import os
import prog


PRINT_THINGS = False


def delete_old_directories(parent_directory, days=15):
    if os.path.exists(parent_directory):
        entries = os.scandir(parent_directory)
        dirs = (entry for entry in entries if entry.is_dir()) #directories in first level
        for a_dir in dirs: # (Photos, VF Aleart, Vibration Aleart, Battery)
            msg = '    ' + a_dir.name
            if a_dir.name.count('-') == 2: #2 '-' in folders named with date
                mon = a_dir.name[0:2]
                day = a_dir.name[3:5]
                year = a_dir.name[6:10]
                tm = '{}/{}/{}'.format(mon, day, year)
                struct_tm = time.strptime(tm, '%m/%d/%Y')
                sec_tm = time.mktime(struct_tm)
                #delete the directory and its content if too old
                max_age = days * 24 * 3600
                if time.time()-sec_tm >= max_age:
                    abs_file_name = parent_directory+'/'+a_dir.name
                    shutil.rmtree(abs_file_name)
                    prog.namePrint('Deleted directory "' +abs_file_name)
    else:
        prog.namePrint('Error! Directory "' + parent_directory + '" does not exist!')


time.sleep(3)

prog.start()
while prog.isRunning():
    #videos
    delete_old_directories('/home/pi/Videos/Camera_0', days=3)

    #accerometer data
    delete_old_directories('/home/pi/Documents/Accel_Data', days=10)
    
    #GPS data
    delete_old_directories('/home/pi/Documents/GPS_Data', days=10)
    
    #wait 3 hours before next check
    prog.sleep(3*3600)


prog.end()
