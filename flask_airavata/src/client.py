##
## Image specific configurations pertaining to Airavata server is done through this script
##


import os
import sh
from sh import Command
from sh import ssh


class ImageConfigManager():

    def configure_image(self, args):
        
	privateKey = args['privateKey']
        user = args['user']
        host = args['host']
        machine = user + '@' + host
        downloadLink = args['airavataDownloadLink']
 
        # Copying the Airavata Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec wget ' + downloadLink
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Unzipping the Airavata Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec tar -xvf apache-airavata-server-*-bin.tar.gz'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Installing Java
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "export DEBIAN_FRONTEND=noninteractive | exec sudo apt-get install openjdk-7-jre-headless"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Starting Airavata Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "export JAVA_HOME=/usr/bin/java | exec nohup sh apache-airavata-server-*/bin/airavata-server.sh &"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()


    def configure_tomcat_image(self, args):
        
	privateKey = args['privateKey']
        user = args['user']
        host = args['host']
        machine = user + '@' + host
        airavataDownloadLink = args['airavataDownloadLink']
        tomcatDownloadLink = args['tomcatDownloadLink']
 
        # Downloading the Airavata Webapp
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec wget ' + airavataDownloadLink
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Unzipping the Airavata Webapp
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec tar -xvf apache-airavata-server-*-war.tar.gz'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Downloading the Tomcat Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec wget ' + tomcatDownloadLink
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close() 

        # Unzipping the Tomcat Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec tar -xvf apache-tomcat-*.tar.gz'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()
        
        # Copying the webapps to Tomcat
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' exec cp airavata-*.war apache-tomcat-*/webapps/ -v'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Installing Java
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "export DEBIAN_FRONTEND=noninteractive | exec sudo apt-get install openjdk-7-jre-headless"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()

        # Starting Tomcat Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "export JAVA_HOME=/usr/bin/java | exec nohup sh apache-tomcat-*/bin/catalina.sh run &"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()
        

    def start_airavata(self, args):   

        privateKey = args['privateKey']
        user = args['user']
        host = args['host']
        machine = user + '@' + host
        downloadLink = args['airavataDownloadLink']

        # Starting Airavata Server
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "export JAVA_HOME=/usr/bin/java | exec nohup sh apache-airavata-server-*/bin/airavata-server.sh &"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()


    def stop_airavata(self, args):   

        privateKey = args['privateKey']
        user = args['user']
        host = args['host']
        machine = user + '@' + host
        downloadLink = args['airavataDownloadLink']

        # Stopping Airavata Server
	# TODO : Test this and fix it.
        #cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "exec kill $(ps aux | grep 'airavata' | awk '{print $2}')"'
        cmd = 'ssh -i' + ' ' + privateKey + ' ' + machine + ' "exec kill $(ps aux | grep \'airavata\' | awk \'{print $2}\')"'
        process = os.popen(cmd)
        preprocessed = process.read()
        process.close()


if __name__ == "__main__":
    args = {}
    args['privateKey'] = '/home/heshan/.ssh/id_dsa'
    args['user'] = 'ubuntu'
    args['host'] = '149.165.158.11'    
    args['tomcatDownloadLink'] = 'http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.14/bin/apache-tomcat-6.0.14.tar.gz'

    manager = ImageConfigManager()

    # Uncomment following line to deploy Airavata in vanilla mode
    args['airavataDownloadLink'] = 'http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-bin.tar.gz'
    manager.configure_image(args)

    # Uncomment following line to deploy Airavata on Tomcat
    #args['airavataDownloadLink'] = 'http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-war.tar.gz'
    #manager.configure_tomcat_image(args)


##if __name__ == "__main__":
##    print(sh.ls("/"))
##    run = sh.ssh("-i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec ifconfig")
##    try:        
##        run()
##    except:
##        print("Error running ifconfig command")


##import paramiko
##
##hostname="149.165.158.143"
##username="heshan"
##port = 22
##password = ""
##pkey_file = '/home/heshan/.ssh/id_dsa'
## 
##if __name__ == "__main__":
##    key = paramiko.DSSKey.from_private_key_file(pkey_file)
##    s = paramiko.SSHClient()
##    s.load_system_host_keys()
##    s.connect(hostname, port, username, password, pkey=key)
##    stdin, stdout, stderr = s.exec_command('ifconfig')
##    print stdout.read()
##    print "stderr: ", stderr.readlines()
##    print "pwd: ", stdout.readlines()    
##    s.close()
##
