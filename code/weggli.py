
# -*- coding: utf-8 -*-
msg = '''
-----------------------------------------------------------------
@author  : Gandalf4a
@file    : main.py 
@time    : 2022/8/5
@site    : www.gandalf.site
@software: ida_check
@version : 2.2.2

_ooOoo_
o8888888o
88" . "88
(| -_- |)  
O\  =  /O  $ sudo rm -rf /
/`---'\____
.'  \\|     |//  `.
/  \\|||  :  |||//  \\
/  _||||| -:- |||||-  \\
|   | \\\  -  /// |   |
| \_|  ''\-/''  |   |
\  .-\__  `-`  ___/-. /
___`. .'  /-.-\  `. . __
."" '<  `.___\_<|>_/___.'  >'"".
| | :  `- \`.;`\ _ /`;.`/ - ` : | |
\  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
-----------------------------------------------------------------
'''
import os 
import magic
import subprocess
from zipfile import ZipFile
import sys
import re
import plistlib
import string
import tempfile
import signal
import time
#reload(sys)
#sys.setdefaultencoding("utf-8")

#win需要修改路径'/'为'\\'
#分析文件路径
_path = "."  
#日志文件路径
f = open ("./_check.log",'a+',encoding='utf-8', errors='ignore')

system = sys.platform
if system == "win32":
    path_symbol = '\\'
else:
    path_symbol = '/'

def change_file_name():
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list: 
            new_file_name = file_name.replace(' ','_').replace('/','_').replace('\\','_').replace('(','_').replace(')','_').replace('（','_').replace('）','_').replace('——','_')
            full_file_name = os.path.join(path,file_name)
            full_new_file_name = os.path.join(path,new_file_name)
            os.rename(full_file_name,full_new_file_name)

def unzip_zipfile():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip file...")
    print ("Unzip file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            #pip3 install python_magic
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                #print (file_name,file_type)
                if "Zip archive data" in file_type:
                    print ("unzip Zip file",full_file_name,"to",full_file_name[:-4],"...")
                    print ("unzip Zip file",full_file_name,"to",full_file_name[:-4],"...",file=f)
                    zp = ZipFile(full_file_name,"r")
                    zp.extractall(full_file_name[:-4])
                    #zp.close()
            except :
                pass  
    change_file_name()
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def unzip_targzfile():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip tar.gz file...")
    print ("Unzip tar.gz file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            h_name = os.path.splitext(file_name)[-1][1:]
            #pip3 install python_magic
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                if (("gzip compressed data" in file_type) and ("gz" == h_name)) or (("tar archive" in file_type) and ("tar" == h_name)):
                    cmd = "tar xvf {}".format(full_file_name.replace(' ','\ '))
                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
                    p.communicate()
                    p.wait()
                    print ("unzip tar.gz file",full_file_name,"to",full_file_name[:-4],"...")
                    print ("unzip tar.gz file",full_file_name,"to",full_file_name[:-4],"...",file=f)
            except :
                pass 
    change_file_name()            
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def unzip_7z_file():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip 7z file...")
    print ("Unzip 7z file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            h_name = os.path.splitext(file_name)[-1][1:]
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                if "7-zip archive data" in file_type:
                    # brew install rpm2cpio
                    cmd = "7z x {}".format(full_file_name.replace(' ','\ '))
                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
                    p.communicate()
                    p.wait()
                    print ("unzip 7z file",full_file_name,"...")
                    print ("unzip 7z file",full_file_name,"...",file=f)
            except :
                pass  
    change_file_name()
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def unzip_RPMfile():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip rpm file...")
    print ("Unzip rpm file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            h_name = os.path.splitext(file_name)[-1][1:]
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                if ("RPM" in file_type) and ("rpm" == h_name):
                    # brew install rpm2cpio
                    cmd = "rpm2cpio {} | cpio -idmv".format(full_file_name.replace(' ','\ '))
                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
                    p.communicate()
                    p.wait()
                    print ("unzip RPM file",full_file_name,"...")
                    print ("unzip RPM file",full_file_name,"...",file=f)
            except :
                pass  
    change_file_name()
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def unzip_deb_file():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip deb file...")
    print ("Unzip deb file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            h_name = os.path.splitext(file_name)[-1][1:]
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                if ("Debian binary package" in file_type) and ("deb" == h_name):
                    # brew install rpm2cpio
                    cmd = "dpkg-deb -x {} ./{} ".format(full_file_name.replace(' ','\ '),file_name.replace(' ','\ ').replace('.','_'))
                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
                    p.communicate()
                    p.wait()
                    print ("unzip deb file",full_file_name,"...")
                    print ("unzip deb file",full_file_name,"...",file=f)
            except :
                pass  
    change_file_name()
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def unzip_cab_file():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("Unzip cab file...")
    print ("Unzip cab file...",file=f)
    for path,dir_list,file_list in os.walk(_path):  
        for file_name in file_list:  
            full_file_name = os.path.join(path,file_name)
            h_name = os.path.splitext(file_name)[-1][1:]
            m=magic.Magic(uncompress=True)
            try:
                file_type = m.from_file(full_file_name)
                if (("Microsoft Cabinet archive" in file_type) and ("cab" == h_name)) or (("PE32 executable" in file_type) and ("exe" == h_name)):
                    # brew install rpm2cpio
                    cmd = "cabextract {} -d {}".format(full_file_name.replace(' ','\ '),path.replace(' ','\ '))
                    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
                    p.communicate()
                    p.wait()
                    print ("unzip cab file",full_file_name,"...")
                    print ("unzip cab file",full_file_name,"...",file=f)
            except :
                pass  
    change_file_name()
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def weggli_code_check():
    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print ("c/c++源码审计...")
    print ("c/c++源码审计...",file=f)
    cmd = "weggli '{$ret = snprintf($b,_,_);$b[$ret] = _;}' ."
    print ("潜在易受攻击的snprintf(),cmd = ",cmd)
    print ("潜在易受攻击的snprintf(),cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '{kfree($a); NOT: goto _; NOT: break; NOT: continue; NOT: return; NOT: $a = _; kfree($a);}' ."
    print ("双重释放,cmd = ",cmd)
    print ("双重释放,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()
    
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = " weggli --unique -R 'func=co?py' '$func($dest, $src, $size($src));' ."
    print ("复制到目标的大小1,cmd = ",cmd)
    print ("复制到目标的大小1,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()
    
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = " weggli --unique -R 'func=co?py' '$func($dest, $src, $src->$len);' ."
    print ("复制到目标的大小2,cmd = ",cmd)
    print ("复制到目标的大小2,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()
    
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique -R 'func=co?py' '$func($dest, $src->$buf, $src->$len);' ."
    print ("复制到目标的大小3,cmd = ",cmd)
    print ("复制到目标的大小3,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()
    
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli '{    _ $buf[_];    memcpy($buf,_,_);}' ."
    print ("调用写入堆栈缓冲区的 memcpy,cmd = ",cmd)
    print ("调用写入堆栈缓冲区的 memcpy,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli '{   strict: foo(_);}' ."
    print ("不检查返回值的 foo 调用,cmd = ",cmd)
    print ("不检查返回值的 foo 调用,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli '{ _* $p;NOT: $p = _;$func(&$p);}' ."
    print ("可能未初始化的指针,cmd = ",cmd)
    print ("可能未初始化的指针,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --cpp '{$x = _.GetWeakPtr(); DCHECK($x); $x->_;}' ."
    print ("潜在不安全的 WeakPtr 用法,cmd = ",cmd)
    print ("潜在不安全的 WeakPtr 用法,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli '_ $fn(_ $limit) {    _ $buf[_];    for (_; $i<$limit; _) {        $buf[$i]=_;    }}' ."
    print ("基于函数参数执行写入堆栈缓冲区的函数,cmd = ",cmd)
    print ("基于函数参数执行写入堆栈缓冲区的函数,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli -R func=decode '_ $func(_) {_;}' ."
    print ("名称中带有字符串 decode 的函数,cmd = ",cmd)
    print ("名称中带有字符串 decode 的函数,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique -R 'a!=^[A-Z_]+$' 'kmalloc($a * _);'  ."
    print ("kmalloc乘法溢出,cmd = ",cmd)
    print ("kmalloc乘法溢出,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique -R 'a!=^[A-Z_]+$' 'malloc($a * _);'  ."
    print ("malloc乘法溢出,cmd = ",cmd)
    print ("malloc乘法溢出,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique 'kmalloc($a + _); memcpy(_, _, $a);' ."
    print ("kmalloc分配中发生的溢出，而不是在使用中发生的溢出,cmd = ",cmd)
    print ("kmalloc分配中发生的溢出，而不是在使用中发生的溢出,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique 'malloc($a + _); memcpy(_, _, $a);' ."
    print ("malloc分配中发生的溢出，而不是在使用中发生的溢出,cmd = ",cmd)
    print ("malloc分配中发生的溢出，而不是在使用中发生的溢出,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli -R 'func=^mem' --unique '$a * _; $func(_ , _, sizeof($a));' ."
    print ("C中的一个典型错误是使用sizeof(ptr)而不是sizeof(type of the pointed thing),cmd = ",cmd)
    print ("C中的一个典型错误是使用sizeof(ptr)而不是sizeof(type of the pointed thing),cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '_ $func(_ $len) {NOT: _ = $buf[$len];NOT: $buf[$len] = _;_ $buf[$len];}' ."
    print ("变长数组风险；如果长度大于堆栈大小，则会发生堆栈溢出,cmd = ",cmd)
    print ("变长数组风险；如果长度大于堆栈大小，则会发生堆栈溢出,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()
 
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$a = alloca(_); free($a);' ."
    print ("释放堆栈分配变量,cmd = ",cmd)
    print ("释放堆栈分配变量,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique -R '$op=\+\+|--' 'if ( _ && _ $op)' ."
    print ("Shady-looking side-effects,cmd = ",cmd)
    print ("Shady-looking side-effects,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$f($a++, $b++)' ."
    print ("未指定的参数顺序1,cmd = ",cmd)
    print ("未指定的参数顺序1,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$f(++$a, ++$b)' ."
    print ("未指定的参数顺序2,cmd = ",cmd)
    print ("未指定的参数顺序2,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$f($a--, $b--)' ."
    print ("未指定的参数顺序3,cmd = ",cmd)
    print ("未指定的参数顺序3,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$f(--$a, --$b)' ."
    print ("未指定的参数顺序4,cmd = ",cmd)
    print ("未指定的参数顺序4,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$a = 0; _ / $a' ."
    print ("被零除,cmd = ",cmd)
    print ("被零除,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique 'if ($a); else if ($a);' ."
    print ("相同条件,cmd = ",cmd)
    print ("相同条件,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique 'void * $a; sizeof(*$a)' ."
    print ("空隙大小,cmd = ",cmd)
    print ("空隙大小,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '{    NOT: $a = memdup_user(_);    NOT: memset($a);    NOT: memset($a->$b);    copy_to_user(_, $a, sizeof(*$a));}' ."
    print ("未初始化或存在内核指针,cmd = ",cmd)
    print ("未初始化或存在内核指针,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli -R 'a=addr' 'dev_info($a);' ."
    print ("KASLR 绕过,cmd = ",cmd)
    print ("KASLR 绕过,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$a = snprintf(0, 0, _); malloc($a);' ."
    print ("分配字符串时不考虑终端snprintf 0,cmd = ",cmd)
    print ("分配字符串时不考虑终端snprintf 0,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --unique '$pos = snprintf(_ + $pos);' ."
    print ("snprintf误用,cmd = ",cmd)
    print ("snprintf误用,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    cmd = "weggli --cpp --unique '$a = new _; $b = (_) $a; delete $b;' ."
    print ("类型混淆释放的方法,cmd = ",cmd)
    print ("类型混淆释放的方法,cmd = ",cmd,file=f)
    out_temp = tempfile.TemporaryFile(mode='w+')
    fileno = out_temp.fileno()
    #p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno)
    #p.communicate()
    #p.wait()
    try:
        p = subprocess.Popen(cmd,shell=True,stdout=fileno,stderr=fileno,preexec_fn=os.setsid)
        p.communicate(timeout=10)
        p.wait()
    except subprocess.TimeoutExpired:
        p.kill()
        print('超时自动结束任务...')
    out_temp.seek(0)
    rt = out_temp.read()
    print (rt)
    print (rt,file=f)
    out_temp.close()

    print ("-----------------------------------------------------------------")
    print ("-----------------------------------------------------------------",file=f)
    print('\n')

def main():
    if len(sys.argv) < 2:
        print("[*] Don't have project name!!!")
        sys.exit(1)

    program_name = sys.argv[1]

    _path = os.path.join(os.getcwd(),program_name)
    print('\n')
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    print ("System is:",system)
    print ("System is:",system,file=f)
    print ("-----------------------------------------------------------------",file=f)
    print ("-----------------------------------------------------------------")
    print('\n')
    print('\n',file=f)
    unzip_zipfile()
    unzip_7z_file()
    unzip_RPMfile()
    unzip_deb_file()
    unzip_targzfile()
    unzip_cab_file()
    weggli_code_check()


if __name__ == "__main__":
    main()