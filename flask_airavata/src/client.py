import sh
from sh import Command
from sh import ssh

import os

##var = ssh("149.165.158.142", "-i /home/heshan/.ssh/id_dsa ubuntu" , "exec wget https://dist.apache.org/repos/dist/dev/airavata/0.7/RC5/apache-airavata-xbaya-gui-0.7-bin.zip")

# Copying the Airavata Server 
process = os.popen('ssh -i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec wget http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-bin.tar.gz')
preprocessed = process.read()
process.close()

# Unzipping the Airavata Server
process = os.popen('ssh -i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec tar -xvf apache-airavata-server-0.7-bin.tar.gz')
preprocessed = process.read()
process.close()

# Installing Java
process = os.popen('ssh -i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec sudo apt-get install openjdk-7-jre-headless')
preprocessed = process.read()
process.close()

# Setting JAVA_HOME
process = os.popen('ssh -i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec export JAVA_HOME=/usr/bin/java')
preprocessed = process.read()
process.close()

# Starting Airavata Server
process = os.popen('ssh -i /home/heshan/.ssh/id_dsa ubuntu@149.165.158.142 exec sh apache-airavata-server-0.7/bin/airavata-server.sh &')
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
