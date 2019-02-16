#coding=utf-8
import os
import time
import win32api,win32con
import tkinter.messagebox
import pickle

# 检查某个文件夹下的最新文件名，并返回该文件名
def check_latest_file(target_dir):
    lists=os.listdir(target_dir)
    lists.sort(key=lambda fn: os.path.getmtime(target_dir + '\\' + fn))
    new_file_name=lists[-1]
    return new_file_name

# 将程序运行过程中检查出的最新文件名用pickle以二进制的形式存入文件
def rewrite_record(filename,record_filename_hr,record_filename_con):
    record_filename_dict = {
        'hr':record_filename_hr,
        'consultant':record_filename_con
    }
    f1 = open(filename, 'wb')
    pickle.dump(record_filename_dict, f1)
    f1.close()

# 发送电子邮件通知
def mail_notification(mail_address, foldername):
    return True

# 主程序
def run(target_dir_hr, target_dir_con, record_file, interval, mail_address):
    # 程序运行前先读入之前一次运行的结果，存入字典中
    f1 = open(record_file, 'rb')
    try:
        record_filename_dict = pickle.load(f1)
    except:
        # 当存储字典的文件为空文件或者格式不正确时，初始化字典数据
        record_filename_dict = {'hr':'nofile', 'consultant':'nofile'}
    f1.close()
    # 下面2行代码为不从文件读取，假设每次启动程序时都已经手动检查过没有新文件
    #record_filename_dict['hr'] = new_file_name_hr
    #record_filename_dict['consultant'] = new_file_name_con:
    while True:
        try:
            # 等待
            time_remaining = interval-time.time()%interval
            time.sleep(time_remaining)
            # 获取最新的生成的文件名
            new_file_name_hr = check_latest_file(target_dir_hr)
            new_file_name_con = check_latest_file(target_dir_con)

            if record_filename_dict['hr'] != new_file_name_hr:
                rewrite_record(record_file, new_file_name_hr, new_file_name_con)
                print('find new file in HR folder')
                # 调用发消息函数通知对方
                #tkinter.messagebox.showinfo("CV Updated", "There is new CV file to check in HR folder")
                mail_notification(mail_address, 'hr')
                break
            elif record_filename_dict['consultant'] != new_file_name_con:
                rewrite_record(record_file, new_file_name_hr, new_file_name_con)
                print('find new file in Consultant folder')
                # 调用发消息函数通知对方
                #tkinter.messagebox.showinfo("CV Updated", "There is new CV file to check in Consultant foler")
                mail_notification(mail_address, 'consultant')
                break
            else:
                print('no new file')
        except:
            print('error')


target_dir_hr = 'D:\\Renly\\testfolder1'
target_dir_con = 'D:\\Renly\\testfolder2'
record_file = 'latest_file_name.txt'
interval = 300
mail_address = 'xxx@xxx.com'

run(target_dir_hr, target_dir_con, record_file, interval, mail_address)
