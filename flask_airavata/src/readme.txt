About
=====

This project is developed by Heshan Suriyaarachchi as part of an independent study for his MS course work and mentored by Gregor Von Laszewski. The project was developed from http://svn.code.sourceforge.net/p/fgairavata/code-0/trunk/ and later moved to https://github.com/futuregrid/flask_oneclick.git.

Installation instructions
=========================

This is done in 3 steps. 
 i) Setting-up Flask
 ii) Setting-up Cloud Mesh
 iii) Setting-up Airavata Deployment Studio


Setting-up Flask
----------------
1). Checkout source
    git clone https://github.com/futuregrid/flask.git

2). Change directory to cm
    cd flask/cm

3). Setup virtualenv and activate it.
    heshan@heshan-ThinkPad-T520:~/Dev/setup/futuregrid/flask/cm$ virtualenv ~/ENV 
    heshan@heshan-ThinkPad-T520:~/Dev/setup/futuregrid/flask/cm$ . ~/ENV/bin/activate

Afterwards you might see your prompt change to ENV.

4). Install flask, Flask-FlatPages and sh (if not already installed).
    pip install flask 
    pip install Flask-FlatPages 
    pip install sh

5). The scripts Assumes cm.git and flask are in the same directory hierarchy
    (ENV)heshan@heshan-ThinkPad-T520:~/Dev/setup/futuregrid/flask/cm$ pwd
    /home/heshan/Dev/setup/futuregrid/flask/cm

6). Source the novarc file
    source ~/.futuregrid/openstack/novarc 


Setting-up Cloud Mesh
---------------------
1). Checkout Cloud Mesh.
    git clone git://github.com/futuregrid/cm.git

2). Activate virtualenv.
    . ~/ENV/bin/activate

3). Run make.
    (ENV)heshan@heshan-ThinkPad-T520:~/Dev/setup/futuregrid/cm.git/trunk$ make

4). Set the key for Open Stack. (You could get this key from your futuregrid account.)
    scp heshan@india.futuregrid.org:.futuregrid/openstack/novarc .  
    cat novarc  
    mkdir -p ~/.futuregrid/openstack/  
    cp novarc ~/.futuregrid/openstack/  
    source ~/.futuregrid/openstack/novarc 

5). Type in a nova command to check whether the key was set properly.
    $ nova list


Setting-up Airavata Deployment Studio
-------------------------------------

1) Checkout Airavata Deployment Studio.
   git clone git://github.com/futuregrid/flask_oneclick.git

2) Start the server.
   cd flask_oneclick/flask_airavata/src
   make server

3) Then connect to the Airavata Deployment Studio app using the following URL.
   eg: http://127.0.0.1:5000/

Configuring config.ini file
===========================
The sample config file has many entried (for legacy reasons) but you only have to configure couple 
of them as they are the only ones which are used within the current program. Following are those params. 

--------------------------------------------------
[ImageConfig]
UserName: heshan
KeyFileName: heshan-key
KeyFilePath: /home/heshan/.ssh/id_dsa
--------------------------------------------------

UserName - Used when creating the image. 
KeyFileName - Name used when exporting the key to your environment
KeyFilePath - Public key path


Limitations/issues
==================

1) CloudMesh does not have any convenience API methods to get information on perticular instances started by a user directly. IMO these should be there so a user could directly use them without any issues rather than trying to parse a large datastruture. 

   GVL: Why not implement? By the way there is in the table a feature to list "my" instances, 
        I am sure that can be wrapped

   Heshan: How can I list my instnces? 

2) Had issues in installing java within a python script with the interactive shell. Tried disabling it but could not resolve the interactivity. Spoke to Koji but we couldn't figure out what to do with it. For, now this is a bug with the software. 

   GVL: ??? can you produce a description on how to create this issue in detail so i can replicate?
        why does java have to be installed? where does it need to beinstalled?

   Heshan: i) You can replicate it by running the client.py program with it's main method. In that logic, I am trying to connect to a remote shell and installing Java but I was not able to resolve the issue I had with the interactive shell.

	   This is simillar to installing Java to your VM using the command "sudo apt-get install openjdk-7-jre-headless". Then you'll be prompted with a [Y/N] : prompt.

  	   ii) Inorder to start apache airavata server, JAVA_HOME property should be set (ie. export JAVA_HOME=/usr/bin/java). Therefore, Java should be installed first. This, could be resolved if we had Java installed base iamges, so that we could only have to set the environment variable within our program (ie. export JAVA_HOME=/usr/bin/java). 
	  
	   iii) It could be installed anywhere. Only thing we have to do is to set the JAVA_HOME environment variable properly.
	   


