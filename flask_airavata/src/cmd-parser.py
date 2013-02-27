import argparse
import os
import sys
import subprocess
import ConfigParser
import fabric

# TODO: Implement the following 
# 1. Create a decorator in python that logs activites to log files when you invoke a perticular function.
# 2. Use sh instead of os
# 3. Have another function to log and run the command


# TODO: 
##fromahimport apt-get sh as _apt-get 
##fromsh import sudo
##apt-get-install =bake(apt-get,"install"
##apt-get(

from fabric.api import *

dict = {}
logfilename = "log.txt"

def getConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

class ConfigManager():

    def configure_image(self, args):
        print "Copying the config script to image ..."
        copyScriptToRemoteServer()
        runScriptOnRemoteServer()
        print "Configuring the image ..."
        install_java(args)
        setup_tomcat(args)

    #@log(logfilename)
    def install_java(self, args):
        print("Updating repositories ...")
        #os.system("sudo add-apt-repository ppa:webupd8team/java")
        os.system("sudo apt-get update")
        print("Installing Java 7 ...")
        #os.system("sudo apt-get install oracle-java7-installer")
        os.system("sudo apt-get install " + dict['JAVA_VERSION'])

    def setup_tomcat(self, args):
        print("Downloading Tomcat ...")
        os.system("wget " + dict['TOMCAT_DOWNLOAD_URL'])
        print("Extracting Tomcat ...")
        #os.system("tar xvzf apache-tomcat-6.0.14.tar.gz")
        os.system("tar xvzf " + dict['TOMCAT_VERSION']+ ".tar.gz")
        setup_airavata_server(args)
        print("Copying the Airavata war files to Tomcat's webapp directory ...")
        #os.system("cp apache-airavata-server-0.6-SNAPSHOT-war/*.war apache-tomcat-6.0.14/webapps -v")
        os.system("cp " + dict['AIRAVATA_VERSION']+ "/*.war " + dict['TOMCAT_VERSION']+ "/webapps -v")
        #os.system("chdmo a+x apache-tomcat-6.0.14/*.sh")
        os.system("chdmo a+x " + dict['TOMCAT_VERSION']+ "/*.sh")

    def setup_airavata_server(self, args):
        print("Downloading Airavata web-app")
        #os.system("wget https://dist.apache.org/repos/dist/dev/airavata/0.6/RC3/apache-airavata-server-0.6-SNAPSHOT-war.zip")
        os.system("wget " + dict['AIRAVATA_DOWNLOAD_URL']+ ".zip")
        print("Extracting Airavata war")
        #os.system("unzip apache-airavata-server-0.6-SNAPSHOT-war.zip")
        os.system("unzip " + dict['AIRAVATA_VERSION']+ ".zip")

    def start_server(self, args):
        print "Starting the Airavata server ..."
        #os.system("nohup ./apache-tomcat-6.0.14/bin/catalina.sh run &")
        os.system("nohup ./" + dict['TOMCAT_VERSION']+ "/bin/catalina.sh run &")

    def stop_server(self, args):
        print "Stopping the Airavata server ..."
        #shutdownCmd = "nohup ./apache-tomcat-6.0.14/bin/catalina.sh run &"
        shutdownCmd = "nohup ./" + dict['TOMCAT_VERSION']+ "/bin/catalina.sh run &"
        subprocess.call([shutdownCmd], shell=true)

        grepCmd = "ps -aef | grep tomcat"
        
        grepResults = subprocess.check_output([grepCmd], shell=true).split()
        for i in range(1, len(grepResults), 9):
          pid = grepResults[i]
          killPidCmd = "kill -9 " + pid
          subprocess.call([killPidCmd], shell=true)

    def kill_server(self, args):
        print "Killing the server with pid : " + args.kill
        os.system("kill -9 args.kill")

    def copyScriptToRemoteServer(self):
        with settings(hosts_string = dict['HOST_NAME'], user = dict['USER_NAME'], key_filename = dict['KEY_FILE_NAME']):
            put(dict['LOCAL_SCRIPT'], dict['DESTINATION_PATH'])
            #run('sh ' + dict['REMOTE_SCRIPT'])

    def runScriptOnRemoteServer(self):
        rsh = ssh.bake("%s@%s" % (dict['USER_NAME'], dict['HOST_NAME']))
        remote = rsh.bake("-o StrictHostKeyChecking no")
        test1 = remote(dict['USER_NAME']).replace("\n","")
        print "<%s>" % test1
        print remote("uname -a")
        print remote('sh ' + dict['REMOTE_SCRIPT'])

    def init(self, args):
        configuration = args.config
        Config.read(configuration)
        
        dict['JAVA_VERSION']= getConfigSectionMap("SoftwareConfig")['javaversion']  
        dict['AIRAVATA_VERSION']= getConfigSectionMap("SoftwareConfig")['airavataversion']  
        dict['AIRAVATA_DOWNLOAD_URL']= getConfigSectionMap("SoftwareConfig")['airavatadownloadurl']  
        dict['TOMCAT_VERSION']= getConfigSectionMap("SoftwareConfig")['tomcatversoin']  
        dict['TOMCAT_DOWNLOAD_URL']= getConfigSectionMap("SoftwareConfig")['tomcatdownloadurl']

        print "***************************************************************************************"
        print "*******************       Software configuration       ********************************"
        print "CONFIGURATION_FILE     :" + configuration
        print "JAVA_VERSION           :" + dict['JAVA_VERSION'] 
        print "AIRAVATA_VERSION       :" + dict['AIRAVATA_VERSION']
        print "AIRAVATA_DOWNLOAD_URL  :" + dict['AIRAVATA_DOWNLOAD_URL'] 
        print "TOMCAT_VERSION         :" + dict['TOMCAT_VERSION']
        print "TOMCAT_DOWNLOAD_URL    :" + dict['TOMCAT_DOWNLOAD_URL']
        print "***************************************************************************************"

        dict['USER_NAME']= getConfigSectionMap("ImageConfig")['username']  
        dict['HOST_NAME'] = getConfigSectionMap("ImageConfig")['hostname']
        dict['KEY_FILE_NAME']= getConfigSectionMap("ImageConfig")['keyfilename']
        dict['LOCAL_SCRIPT'] = getConfigSectionMap("ImageConfig")['localscript']
        dict['LOCAL_CONFIG_FILE'] = getConfigSectionMap("ImageConfig")['localconfigfile']
        dict['DESTINATION_PATH'] = getConfigSectionMap("ImageConfig")['destinationpath']
        dict['REMOTE_SCRIPT'] = getConfigSectionMap("ImageConfig")['remotescript']

        print "*******************        Image configuration         ********************************"
        print "USER_NAME              :" + dict['USER_NAME']
        print "HOST_NAME              :" + dict['HOST_NAME']  
        print "KEY_FILE_NAME          :" + dict['KEY_FILE_NAME']
        print "LOCAL_SCRIPT           :" + dict['LOCAL_SCRIPT']  
        print "LOCAL_CONFIG_FILE      :" + dict['LOCAL_CONFIG_FILE'] 
        print "DESTINATION_PATH       :" + dict['DESTINATION_PATH']
        print "REMOTE_SCRIPT          :" + dict['REMOTE_SCRIPT']
        print "***************************************************************************************"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration file for the script")
    parser.add_argument("--version", action="store_true", help="Version of the program")
    parser.add_argument("--status", action="store_true", help="Status of the Airavata image")
    parser.add_argument("--start", action="store_true", help="Start the Airavata image")
    parser.add_argument("--stop", action="store_true", help="Stop the Airavata image")
    parser.add_argument("--kill", help="Kill the Airavata image with pid")
    parser.add_argument("--install", help="Installs and configures the image based on the configration file")  
    args = parser.parse_args()
    Config = ConfigParser.ConfigParser()
    manager = ConfigManager()
    manager.init(args)

    if args.install:
        manager.configure_image(args)        
    elif args.start:
        manager.start_server(args)       
    elif args.stop:
        manager.stop_server(args)
    elif args.kill:
        manager.kill_server(args)
    elif args.version:
        print "1.0-beta"
    elif args.status:
        print "Displaying status of Airavata server ..."        
    else:
        print "No options provided. use -h flag for help."





