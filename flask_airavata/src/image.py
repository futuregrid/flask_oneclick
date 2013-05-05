import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')

import os
import time
from flask import Flask, render_template, request
from flask_flatpages import FlatPages

from cloudmesh.cloudmesh import cloudmesh
from datetime import datetime
from cloudmesh.cm_config import cm_config
from datetime import datetime
try:
    from sh import xterm
except:
    print "xterm not suppported"
import yaml


print "Start executing the script" 

#### setting up reading path for the use of yaml################
default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

#### end of setting up reading path for the use of yaml################	

cloud = "grizzly-openstack"
clouds = cloudmesh()
clouds.refresh()
d = clouds.configuration
print d.clouds

#sys.exit()


print clouds.get()
#image = d.get()["cloudmesh"]["clouds"][cloud]["image"]
#print image 
#sys.exit()
#print clouds.configuration


print d.userkeys("default")


key = d.userkeys("default")
print key
#sys.exit()
# cloud_name, prefix, index, image_id, flavor_name, key
clouds.create(cloud, "heshan", "1", "ktanaka/ubuntu1204-ramdisk.manifest.xml", "openstack", "/N/u/heshan/.futuregrid/openstack/pk.pem")


