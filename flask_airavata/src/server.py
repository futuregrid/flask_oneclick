from flask import Flask, render_template, request
app = Flask(__name__)

dict = {}

@app.route('/')
def home():
  return render_template('fluid.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/why')
def why():
  return render_template('why.html')

@app.route('/configuring')
def configuring():
  return render_template('configuring.html')

@app.route('/monitoring')
def monitoring():
  return render_template('monitoring.html')

@app.route('/create')
def create():
  return render_template('create.html')

def remoteConnection(id):
# from gregor

  result = fgrep(nova.show(id), 'network')

  (start, label, ips, rest) = result.replace(' ', '').split('|')
  print
  ips
  try:
    (private_ip, public_ip) = ips.split(',')
  except:
    print 'public IP is not yet assigned'
    sys.exit()
  print public_ip
  rsh = ssh.bake('%s@%s' % ('ubuntu', str(public_ip)))
  remote = rsh.bake('-o StrictHostKeyChecking no')
  test1 = remote('uname').replace('\n', '')
  print '<%s>' % test1
  print remote('uname -a')
  print remote('hostname')
  print remote('pwd')

def boot(index):
  '''starts a virtual machine with the given index'''

  try:  
    #number = str(index).zfill(3)
    #name = '%s-%s' % (prefix, number)
    name = "airavata-cloud-image"
    print 'Launching VM %s' % name
    tmp = nova(
        'boot',
        '--flavor=1',
        '--image=%s' % image_name,
        '--key_name',
        '%s' % prefix,
        '%s' % name,
        )
    print tmp
  except Exception, e:
    print e
    print 'Failure to launch %s' % name    

@app.route('/image-result', methods=['GET', 'POST'])
def imageResult():  
  infrastructure = request.args.get('dropdown_infrastructure', '')
  architecture = request.args.get('dropdown_architecture', '')
  memory = request.args.get('dropdown_memory', '')
  os = request.args.get('dropdown_os', '')
  java = request.args.get('dropdown_java', '')
  tomcat = request.args.get('dropdown_tomcat', '')
  airavata = request.args.get('dropdown_airavata', '')

  if(java == "17"):
    dict['JAVA_VERSION']= java
  else:
    # For now setting like this. Later change it. 
    dict['JAVA_VERSION']= java

  if(airavata == "Airavata0.6"):
    dict['AIRAVATA_VERSION']= airavata
    dict['AIRAVATA_DOWNLOAD_URL']= "https://dist.apache.org/repos/dist/dev/airavata/0.6/RC3/apache-airavata-server-0.6-SNAPSHOT-war.zip"
  else:
    # For now setting like this. Later change it. 
    dict['AIRAVATA_VERSION']= airavata
    dict['AIRAVATA_DOWNLOAD_URL']= "https://dist.apache.org/repos/dist/dev/airavata/0.6/RC3/apache-airavata-server-0.6-SNAPSHOT-war.zip"

  if(tomcat == "tomcat6"):
    dict['TOMCAT_VERSION']= "apache-tomcat-6.0.14.tar.gz"
    dict['TOMCAT_DOWNLOAD_URL']= "http://apache.hoxt.com/tomcat/tomcat-6/v6.0.14/bin/apache-tomcat-6.0.14.tar.gz"
  else:
    # For now setting like this. Later change it. 
    dict['TOMCAT_VERSION']= "apache-tomcat-6.0.14.tar.gz"
    dict['TOMCAT_DOWNLOAD_URL']= "http://apache.hoxt.com/tomcat/tomcat-6/v6.0.14/bin/apache-tomcat-6.0.14.tar.gz"

  ## TODO : Add the following values before running the script. 
  dict['USER_NAME']= ""
  dict['HOST_NAME']= ""
  dict['KEY_FILE_NAME']= ""
  dict['LOCAL_SCRIPT']= "" 
  dict['LOCAL_CONFIG_FILE']= "" 
  dict['DESTINATION_PATH']= "" 
  dict['REMOTE_SCRIPT']= "" 


  # TODO : Add logic to create image
  
  return render_template('image-result.html')

def printKeys(myKeys):
  print "Printing keys ... "
  for key in myKeys:
    print """<p>key: %s, value: %s type: %s</p>"""%(key, form[key].value, type(form[key].value)) 

if __name__ == '__main__':
  app.run(debug=True)
