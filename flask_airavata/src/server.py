##
## Server logic for the web-app is contained here. 
##


import ConfigParser
from flask import Flask, render_template, request
from image import *
from client import *
app = Flask(__name__)


dict = {}
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
count = 0

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


@app.route('/')
def home():
  return render_template('fluid.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/ack')
def ack():
  return render_template('ack.html')


@app.route('/contact')
def contact():
  return render_template('contact.html')


@app.route('/why')
def why():
  return render_template('why.html')


@app.route('/configuring')
def configuring():
  return render_template('configuring.html')


@app.route('/configure_base')
def configure_base():
  return render_template('configure_base.html')


@app.route('/configure_base_result', methods=['GET', 'POST'])
def configure_base_result():
  # Starting up the image
  infra = request.args.get('dropdown_infrastructure', '')
  archi = request.args.get('dropdown_architecture', '')
  memory = request.args.get('dropdown_memory', '')
  os = request.args.get('dropdown_os', '')

  args2 = {}
  if(infra == "openstack"):
    args2['cloud'] = "india-openstack"
  else:
    args2['cloud'] = "grizzly-openstack"

  global count
  count = count + 1
  args2['username'] = getConfigSectionMap("ImageConfig")['username']  
  args2['publicKey'] = getConfigSectionMap("ImageConfig")['keyfilename']  
  args2['userId'] = str(count)

  print "IMAGE_CONFIGURATION : ", infra, archi, memory, os, args2['username'], args2['publicKey'],  count
  
  if(os == "ubuntu"):
    args2['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args2['imageSize'] = "m1.tiny"
  else:
    args2['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args2['imageSize'] = "m1.tiny"  
  
  manager = CloudConfigManager()
  # TODO : This will work after, Pushkar updates the cloudmesh.create() 
  ip = manager.start_image(args2)

  # Installing software on the image instance
  #ip = request.args.get('ip_address', '')
  java = request.args.get('dropdown_java', '')
  tomcat = request.args.get('dropdown_tomcat', '')
  airavata = request.args.get('dropdown_airavata', '')

  args = {}
  args['privateKey'] = getConfigSectionMap("ImageConfig")['keyfilepath']  
  args['user'] = 'ubuntu'
  args['host'] = ip
  args['airavataDownloadLink'] = 'http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-bin.tar.gz'

  print "SOFTWARE_CONFIG : ", ip, java, tomcat, airavata, args['privateKey']
  
  manager = ImageConfigManager()
  manager.configure_image(args)
  
  return render_template('configure_base_result.html')


@app.route('/configure_custom')
def configure_custom():
  return render_template('configure_custom.html')


@app.route('/configure_custom_result', methods=['GET', 'POST'])
def configure_custom_result():
  # Starting up the image   

  # Installing software on the image instance
  ip = request.args.get('ip_address', '')
  java = request.args.get('dropdown_java', '')
  tomcat = request.args.get('dropdown_tomcat', '')
  airavata = request.args.get('dropdown_airavata', '')

  print ip, java, tomcat, airavata

  # TODO : Change accordingly
  # TODO : Should test this
  args = {}
  args['privateKey'] = '/home/heshan/.ssh/id_dsa'
  args['user'] = 'ubuntu'
  args['host'] = '149.165.158.11'
  args['airavataDownloadLink'] = 'http://apache.mirrors.lucidnetworks.net/airavata/0.7/apache-airavata-server-0.7-bin.tar.gz'

  manager = ImageConfigManager()
  manager.configure_image(args)
      
  return render_template('configure_custom_result.html')


@app.route('/monitoring')
def monitoring():
  return render_template('monitoring.html')


@app.route('/create')
def create():
  return render_template('create.html')


@app.route('/image-result', methods=['GET', 'POST'])
def imageResult():  
  infra = request.args.get('dropdown_infrastructure', '')
  archi = request.args.get('dropdown_architecture', '')
  memory = request.args.get('dropdown_memory', '')
  os = request.args.get('dropdown_os', '')

  args2 = {}
  if(infra == "openstack"):
    args2['cloud'] = "india-openstack"
  else:
    args2['cloud'] = "grizzly-openstack"

  global count
  count = count + 1
  args2['username'] = getConfigSectionMap("ImageConfig")['username']  
  args2['publicKey'] = getConfigSectionMap("ImageConfig")['keyfilename']  
  args2['userId'] = str(count)

  print "IMAGE_CONFIGURATION : ", infra, archi, memory, os, args2['username'], args2['publicKey'],  count
  
  if(os == "ubuntu"):
    args2['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args2['imageSize'] = "m1.tiny"
  else:
    args2['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args2['imageSize'] = "m1.tiny"  
  
  manager = CloudConfigManager()
  manager.start_image(args2)

  return render_template('image-result.html')


def printKeys(myKeys):
  print "Printing keys ... "
  for key in myKeys:
    print """<p>key: %s, value: %s type: %s</p>"""%(key, form[key].value, type(form[key].value)) 


if __name__ == '__main__':
  app.run(debug=True)



##def remoteConnection(id):
##  result = fgrep(nova.show(id), 'network')
##
##  (start, label, ips, rest) = result.replace(' ', '').split('|')
##  print
##  ips
##  try:
##    (private_ip, public_ip) = ips.split(',')
##  except:
##    print 'public IP is not yet assigned'
##    sys.exit()
##  print public_ip
##  rsh = ssh.bake('%s@%s' % ('ubuntu', str(public_ip)))
##  remote = rsh.bake('-o StrictHostKeyChecking no')
##  test1 = remote('uname').replace('\n', '')
##  print '<%s>' % test1
##  print remote('uname -a')
##  print remote('hostname')
##  print remote('pwd')
##
##def boot(index):
##  '''starts a virtual machine with the given index'''
##
##  try:  
##    #number = str(index).zfill(3)
##    #name = '%s-%s' % (prefix, number)
##    name = "airavata-cloud-image"
##    print 'Launching VM %s' % name
##    tmp = nova(
##        'boot',
##        '--flavor=1',
##        '--image=%s' % image_name,
##        '--key_name',
##        '%s' % prefix,
##        '%s' % name,
##        )
##    print tmp
##  except Exception, e:
##    print e
##    print 'Failure to launch %s' % name    
##
