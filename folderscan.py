import os
import time
import win32api,win32con
import tkinter.messagebox

def check_latest_file(target_dir):
    lists=os.listdir(target_dir)
    lists.sort(key=lambda fn: os.path.getmtime(target_dir + '\\' + fn))
    new_file_name=lists[-1]
    return new_file_name

def rewrite_record(filename,record_filename):
    f1 = open(filename, 'w')
    f1.write(record_filename)
    f1.close()

def run(target_dir,record_file,interval):
    f1 = open(record_file, 'r')
    record_filename=f1.read()
    f1.close()
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            time.sleep(time_remaining)
            # execute the command
            new_file_name=check_latest_file(target_dir)
            if record_filename!=new_file_name:
                rewrite_record(record_file,new_file_name)
                print('find new file')
                #win32api.MessageBox(0,"this is messagebox", "title",MB_OK)
                tkinter.messagebox.showinfo("CV Updated", "There is new CV file to check")
                break
            else:
                print('no new file')
        except:
            print('error')


target_dir='D:\\Renly\\testfolder'
record_file='latest_file_name.txt'
interval=5

run(target_dir,record_file,interval)
