import argparse
import os
import sys
import subprocess
import ConfigParser
import fabric

from fabric.api import *
from sh import apt_get as _apt_get 
from sh import sudo
from sh import Command
from sh import wget
from sh import unzip
from sh import tar
from sh import cp
from sh import kill

#TODO
##  Add the _tty_in=True to each of the commands being used. eg:
##  r = cm("--set", "quiet", "kill", _tty_in=True)

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


def log(msg):
    print msg
    
class ConfigManager():

    def configure_image(self, args):
        log("Copying the config script to image ...")
        copyScriptToRemoteServer()
        runScriptOnRemoteServer()
        
        log("Configuring the image ...")
        install_java(args)
        setup_tomcat(args)

    #@log(logfilename)
    def install_java(self, args):
        # Add checks to Java version
        with sudo:
            try:
                log("Updating repositories ...")
                apt_get("update")
            except:
                log("Error updating repositories")

            try:    
                log("Installing Java 7 ...")
                apt_get("install", "oracle-java7-installer")
            except:
                log("Error installing Java")

    def setup_tomcat(self, args):
        try:
            log("Downloading Tomcat ...")
            result = wget(dict['TOMCAT_DOWNLOAD_URL'])
        except:
            log("Error getting Tomcat from : " + dict['TOMCAT_DOWNLOAD_URL'])

        try:
            log("Extracting Tomcat ...")            
            result = tar("xvzf " , dict['TOMCAT_VERSION']+ ".tar.gz")
        except:
            log("Error extracting Tomcat ..." + dict['TOMCAT_VERSION']+ ".tar.gz")
        
        setup_airavata_server(args)

        try:
            log("Copying the Airavata war files to Tomcat's webapp directory ...")
            result = cp(dict['AIRAVATA_VERSION']+ "/*.war " , dict['TOMCAT_VERSION']+ "/webapps", "-v")
        except:
            log("Error copying the Airavata war files to Tomcat's webapp directory ...")

        try :
            log("Granting executeable permissions to the script")
            result = chmod("a+x" , dict['TOMCAT_VERSION']+ "/*.sh")
        except:
            log("Error granting executable permissions to " + dict['TOMCAT_VERSION']+ "/*.sh")

    def setup_airavata_server(self, args):
        try:
            log("Downloading Airavata web-app ...")
            result = wget(dict['AIRAVATA_DOWNLOAD_URL']+ ".zip")
        except:
            log("Error Downloading Airavata web-app from: " + dict['AIRAVATA_DOWNLOAD_URL'])

        try:
            log("Extracting Airavata war")
            result = unzip(dict['AIRAVATA_VERSION']+ ".zip")
        except:
            log("Error extracting Airavata war" + dict['AIRAVATA_VERSION']+ ".zip")
            

    def start_server(self, args):
        try: 
            log("Starting the Airavata server ...")
            #os.system("nohup ./apache-tomcat-6.0.14/bin/catalina.sh run &")
            # TODO : talk to Gregor
            os.system("nohup ./" + dict['TOMCAT_VERSION']+ "/bin/catalina.sh run &")
        except:
            log("Error starting the Airavata server ...")
            

    def stop_server(self, args):
        log("Stopping the Airavata server ...")
        #shutdownCmd = "nohup ./apache-tomcat-6.0.14/bin/catalina.sh run &"
        # TODO : talk to Gregor
        shutdownCmd = "nohup ./" + dict['TOMCAT_VERSION']+ "/bin/catalina.sh run &"
        subprocess.call([shutdownCmd], shell=true)

        grepCmd = "ps -aef | grep tomcat"
        
        grepResults = subprocess.check_output([grepCmd], shell=true).split()
        for i in range(1, len(grepResults), 9):
          pid = grepResults[i]
          killPidCmd = "kill -9 " + pid
          subprocess.call([killPidCmd], shell=true)

    def kill_server(self, args):
        try: 
            log("Killing the server with pid : " + args.kill)
            kill("-9", "args.kill")
        except:
            log("Killing the server with pid : " + args.kill)

    def copyScriptToRemoteServer(self):
        try:
            with settings(hosts_string = dict['HOST_NAME'], user = dict['USER_NAME'], key_filename = dict['KEY_FILE_NAME']):
                put(dict['LOCAL_SCRIPT'], dict['DESTINATION_PATH'])
                #run('sh ' + dict['REMOTE_SCRIPT'])
        except:
            log("Error copying the script to the remote server : " + dict['HOST_NAME'])

    def runScriptOnRemoteServer(self):
        try:
            rsh = ssh.bake("%s@%s" % (dict['USER_NAME'], dict['HOST_NAME']))
            remote = rsh.bake("-o StrictHostKeyChecking no")
            test1 = remote(dict['USER_NAME']).replace("\n","")
            log("<%s>" % test1)
            log(remote("uname -a"))
            log(remote('sh ' + dict['REMOTE_SCRIPT']))
        except:
            log("Error running the script on remote server")    
    
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


