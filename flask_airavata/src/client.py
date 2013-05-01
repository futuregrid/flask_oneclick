import os
import sh
from sh import Command
from sh import ssh


if __name__ == "__main__":
    privateKey = '/home/heshan/.ssh/id_dsa'
    user = 'ubuntu'
    host = '149.165.158.11'
    machine = user + '@' + host
    downloadLink = 'http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-bin.tar.gz'
    
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
