#coding=utf-8
import os
import time
import win32api,win32con
import tkinter.messagebox

# 检查某个文件夹下的最新文件名，并返回该文件名
def check_latest_file(target_dir):
    lists=os.listdir(target_dir)
    lists.sort(key=lambda fn: os.path.getmtime(target_dir + '\\' + fn))
    new_file_name=lists[-1]
    return new_file_name

# 将程序运行过程中检查出的最新文件名用字典的形式存入文件
def rewrite_record(filename,record_filename_hr,record_filename_con):
    record_filename_dict = {'hr':record_filename_hr, 'consultant':record_filename_con}
    f1 = open(filename, 'w')
    f1.write(str(record_filename_dict))
    f1.close()

# 主程序
def run(target_dir_hr, target_dir_con, record_file, interval):
    # 程序运行前先读入之前一次运行的结果，存入字典中
    f1 = open(record_file, 'r')
    record_filename_dict = eval(f1.read())
    f1.close()
    while True:
        try:
            # sleep for the remaining seconds of interval
            time_remaining = interval-time.time()%interval
            time.sleep(time_remaining)
            # 获取最新的生成的文件名
            new_file_name_hr = check_latest_file(target_dir_hr)
            new_file_name_con = check_latest_file(target_dir_con)

            if record_filename_dict['hr'] != new_file_name_hr:
                rewrite_record(record_file,new_file_name_hr, new_file_name_con)
                print('find new file in HR folder')
                #win32api.MessageBox(0,"this is messagebox", "title",MB_OK)
                # 调用发消息函数通知对方
                tkinter.messagebox.showinfo("CV Updated", "There is new CV file to check in HR folder")
                break
            elif record_filename_dict['consultant'] != new_file_name_con:
                rewrite_record(record_file, new_file_name_hr, new_file_name_con)
                print('find new file in Consultant folder')
                # win32api.MessageBox(0,"this is messagebox", "title",MB_OK)
                # 调用发消息函数通知对方
                tkinter.messagebox.showinfo("CV Updated", "There is new CV file to check in Consultant foler")
                break
            else:
                print('no new file')
        except:
            print('error')


target_dir_hr='D:\\Renly\\testfolder1'
target_dir_con='D:\\Renly\\testfolder2'
record_file='latest_file_name.txt'
interval=5

run(target_dir_hr, target_dir_con, record_file,interval)
