import sqlite3
import ftplib
import os
import socket
from matplotlib import pyplot as plt
from matplotlib import dates
import sys, getopt
from datetime import datetime

remote_host = "104.225.149.96"
remote_dir = "/"
remote_file = "test.db"

def download():
    try:
        ftp = ftplib.FTP(remote_host)
    except (socket.error, socket.gaierror):
        print("ERROR cannot reach '%s'" % remote_host)
        return
    print("..Connected to remote_host '%s'.." % remote_host)

    try:
        ftp.login('ftpusr','koala') # 使用匿名账号登陆也就是anonymous
    except ftplib.error_perm:
        print("ERROR cannot login anonymously")
        ftp.quit()
        return
    print("...logged in as 'anonymously'...")

    try:
        ftp.cwd(remote_dir)  # 切换当前工作目录
    except ftplib.error_perm:
        print("ERROR cannot cd to '%s'" % remote_dir)
        ftp.quit()
        return
    print("....Changed to '%s' folder...." % remote_dir)


    try:
        ftp.retrbinary("RETR %s" % remote_file, open(remote_file, "wb").write)
    except ftplib.error_perm:
        print("ERROR cannot remote_file '%s'" % remote_file)
        os.unlink(remote_file)
    else:
        print(".....Download '%s' to cwd....." % remote_file)
    ftp.quit()
    return

def trans(argv):
    try:
        opts, args = getopt.getopt(argv, "d:")
    except getopt.GetoptError:
        print ('Error when trans args')
        sys.exit(2)
    return opts,args


if __name__ == "__main__":
    #trans the args
    recd = 600
    opts,args = trans(sys.argv[1:])
    for opt, arg in opts:
        if opt == "-d":
            recd = int(arg)*4
            print("recd is",recd)
    #download dbfile
    download()
    #connect db,get data
    conn = sqlite3.connect('./test.db')
    c = conn.cursor()
    print ("Opened database successfully")
    cursor=c.execute("SELECT pri,TIMESTAMP  from price where type='illy' ORDER BY TIMESTAMP DESC ")
    count = 0
    tmp=[]
    for row in cursor:
        tmp.append(row)
        count=count+1
        if count>recd:
            break
    conn.close()
    tmp.reverse()
    y=[]
    x=[]
    for var in tmp:
        y.append(var[0])
        x.append(var[1])
        print(var[0],"   ",var[1],"\n")
    #draw the pic
    xs = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date() for d in x]
    dfm = dates.DateFormatter('%m-%d')
    plt.gca().xaxis.set_major_formatter(dfm)
    print(xs)
    plt.plot(xs,y)
    plt.gcf().autofmt_xdate()
    plt.show()
#
