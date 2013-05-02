##
## Server logic for the web-app is contained here. 
##


from flask import Flask, render_template, request
from image import *
app = Flask(__name__)


dict = {}


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


@app.route('/configure_base_result')
def configure_base_result():
  ip = request.args.get('ip_address', '')
  java = request.args.get('dropdown_java', '')
  tomcat = request.args.get('dropdown_tomcat', '')
  airavata = request.args.get('dropdown_airavata', '')

  print ip, java, tomcat, airavata
  
  return render_template('configure_base_result.html')


@app.route('/configure_custom')
def configure_custom():
  return render_template('configure_custom.html')


@app.route('/configure_custom_result')
def configure_custom_result():
  ip = request.args.get('ip_address', '')
  java = request.args.get('dropdown_java', '')
  tomcat = request.args.get('dropdown_tomcat', '')
  airavata = request.args.get('dropdown_airavata', '')

  print ip, java, tomcat, airavata
    
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

  print infra, archi, memory, os

  args = {}
  if(infra == "openstack"):
    args['cloud'] = "india-openstack"
  else:
    args['cloud'] = "grizzly-openstack"

  ## TODO : Read in from the config file  
  args['username'] = "heshan"
  args['publicKey'] = "heshan-key" 
  args['userId'] = "1"

  if(os == "ubuntu"):
    args['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args['imageSize'] = "m1.tiny"
  else:
    args['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args['imageSize'] = "m1.tiny"  
  
  manager = CloudConfigManager()
  manager.start_image(args)

  # TODO : Add logic to create image
  
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
