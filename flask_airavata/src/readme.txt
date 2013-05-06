Installation instructions
=========================

1) Checkout and install ClouMesh in a Virtual environment.
   Instruction can be found on http://cloudmesh.blogspot.com/2013/02/setting-up-cloud-mesh-environment-on.html

   GVL: PLEASE REMOVE DEPENDENCY TO GO TO SOME BLOG, INSTAED PUT EXPLENATION IN SELF CONTAINED MANNER HERE

2) Start the server using the following command.
   eg: make server

3) Then connect to the Airavata Deployment Studio app using the following URL.
   eg: http://127.0.0.1:5000/

Configuring config.ini file
===========================
The sample config file has many entried (for legacy reasons) but you only have to configure couple 
of them as they are the only ones which are used within the current program. Following are those params. 

--------------------------------------------------
[ImageConfig]
UserName: heshan
HostName: 156.56.179.116
KeyFileName: heshan-key
KeyFilePath: /home/heshan/.ssh/id_dsa
--------------------------------------------------

UserName - Used when creating the image. 
HostName - Public IP address of the image.
KeyFileName - Name used when exporting the key to your environment
KeyFilePath - Public key path


Limitations/issues
==================
1) At the CloudMesh environment level, when a new image is created, it's id is not returned. Therefore, found it difficult to use it within the app. If I had that information, I could have kept the id in a table. Then I could periodically the do cloud.refresh() and check for 
the public ip. Once it is set, I would install the software on that image. I'm working with Pushkar on this. 

  GVL: this seems a trivial change in the code and could be done easily, why not implement????
       Coordinate with the others
  
  Heshan: Pushkar has done some modifications to resolve this but the returned result is not in a proper format. I have sent him the following email and waiting till he fixes it. 

          "
	  Hi Pushkar,

          Can you change the returned data sturcture to the following format

          { id : 'id-of-the-image', value : 'info of the image' }

          Otherwise if you return { id : value}, I can not programmetically extract out the information from the data structure. 

	  Actually I only need the id of the image (eg. f1c8e310-282c-4572-a605-129e32bc76ae). Then I could find 
          out the other info from the dict{} in the cloudmesh().

	  "

2) CloudMesh does not have any convenience API methods to get information on perticular instances started by a user directly. IMO these should be there so a user could directly use them without any issues rather than trying to parse a large datastruture. 

   GVL: Why not implement? By the way there is in the table a feature to list "my" instances, 
        I am sure that can be wrapped

   Heshan: How can I list my instnces? 

3) Had issues in installing java within a python script with the interactive shell. Tried disabling it but could not resolve the interactivity. Spoke to Koji but we couldn't figure out what to do with it. For, now this is a bug with the software. 

   GVL: ??? can you produce a description on how to create this issue in detail so i can replicate?
        why does java have to be installed? where does it need to beinstalled?

   Heshan: i) You can replicate it by running the client.py program with it's main method. In that logic, I am trying to connect to a remote shell and installing Java but I was not able to resolve the issue I had with the interactive shell.

	   This is simillar to installing Java to your VM using the command "sudo apt-get install openjdk-7-jre-headless". Then you'll be prompted with a [Y/N] : prompt.

  	   ii) Inorder to start apache airavata server, JAVA_HOME property should be set (ie. export JAVA_HOME=/usr/bin/java). Therefore, Java should be installed first. This, could be resolved if we had Java installed base iamges, so that we could only have to set the environment variable within our program (ie. export JAVA_HOME=/usr/bin/java). 
	  
	   iii) It could be installed anywhere. Only thing we have to do is to set the JAVA_HOME environment variable properly.
	   

4) Once an image is created, it takes some time to assign an public IP to it.

   GVL: you should use Grizzly on FG and introduce a wait statement while waiting for the VM that you create.
        logging into the vm and saying uname -a will be a good test
        easy to add

   Heshan : I have fixed this using Python threads and by monitoring the datastructure for the public ip. Once public ip is assigned, software is installed in that particular machine.

