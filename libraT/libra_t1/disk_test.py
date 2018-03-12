#/usr/bin/python
#coding:utf-8

import os,time

HOME_DIR = '/home/ubuntu'
WEBHOOK_PATH = '/data/shell/service/webhook.out'
K = 0

def Make_Files():
    global K
    os.chdir(HOME_DIR)
    os.system('pwd')
    while True:
        if (os.path.exists('file_%d'%K) == False):
	    print '====================MAKE FILE_%d===================='%K
            os.system('sudo dd if=/dev/zero of=file_%d bs=100M count=2'%K)
	    print 
	    print '**file_%d**'%K
	    #print 
	    K+=1
	    os.system('df -h')
	    print 
	    val = os.popen('df -h').read()
	    disk = eval(val.split('\n')[1].split()[4].split('%')[0])
	    if disk > 75:
                time.sleep(60)
                val_2 = os.popen('tail -n 42 %s'%WEBHOOK_PATH).read()
                if 'slim_system hook triggered successfully' in val_2:
                    print 'Slim_system hook triggered successfully'
                else:
                    print 'Slim_system hook triggered failed'
		break
	else:       
            print 'file_%d exists'%K                                                                                                       
            break 
    while True:
        if (os.path.exists('file_%d'%K) == False):
            print '====================MAKE FILE_%d===================='%K
            os.system('sudo dd if=/dev/zero of=file_%d bs=100M count=2'%K)
            print 
            print '**file_%d**'%K
            #print 
            K+=1
            os.system('df -h')
            print 
            val = os.popen('df -h').read()
            disk = eval(val.split('\n')[1].split()[4].split('%')[0])
	    if disk > 95:
                time.sleep(60)
                val_1 = os.popen('tail %s'%WEBHOOK_PATH).read()
                if 'stop_libra hook triggered successfully' in val_1:
                    print 'Stop_libra hook triggered successfully'
		    print                                                                                                                  
                    os.system('sudo docker ps -a')
		    #time.sleep(10)
                else:
                    print 'Stop_libra hook triggered failed'
		break      
	else:
	    print 'file_%d exists'%K
	    break


def Rm_Files():
    global K
    K-=1 
    while True:
	if (os.path.exists('file_%d'%K) == True):
            print '====================DELETE FILE_%d===================='%K
            os.system('rm -f file_%d'%K)
	    #print 
	    print '**file_%d**'%K
	    K-=1
	    os.system('df -h')
	    print 
	    val = os.popen('df -h').read()
            disk = eval(val.split('\n')[1].split()[4].split('%')[0])
	    if disk < 95:
	        time.sleep(60)
	        val_1 = os.popen('tail %s'%WEBHOOK_PATH).read()
	        if 'start_libra hook triggered successfully' in val_1:
		    print 'Start_libra hook triggered successfully'
		    print 
		    os.system('sudo docker ps -a')
		    time.sleep(10)
		else:                                                                                                                      
                    print 'Start_libra hook triggered failed' 
                break
	else:
            print 'file_%d does not exist'%K
            break

    while K>=0:
        if (os.path.exists('file_%d'%K) == True):                                                                                          
            print '====================DELETE FILE_%d===================='%K                                                               
            os.system('rm -f file_%d'%K)
	    #print                                                                                                   
            print '**file_%d**'%K
	    #print                                                                                                               
            K-=1                                                                                                                           
            os.system('df -h')
	else:                                                                                                                              
            print 'file_%d does not exist'%K                                                                                               
            break 

if __name__ == '__main__':
    Make_Files()
    print
    print 'Please to check the Libra-T Config...'
    time.sleep(30)
    Rm_Files()
    print 
    print 'Please to check the Libra-T Config...'
    time.sleep(30)
