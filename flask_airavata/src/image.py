## Creates an image in the FutureGrid environement with the given input data
##
##

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

class CloudConfigManager():

    def start_image(self, args):
        print "Generating an image in the FutureGrid environement"

        cloud = args['cloud']
        username = args['username']
        userId = args['userId']
        instanceId = args['instanceId']
        imageSize = args['imageSize']
        publicKey = args['publicKey']

        # setting up reading path for the use of yaml
        default_path = '.futuregrid/cloudmesh.yaml'
        home = os.environ['HOME']
        filename = "%s/%s" % (home, default_path)
        
        clouds = cloudmesh()
        clouds.refresh()
        d = clouds.configuration
        clouds.create(cloud, username, userId, instanceId, imageSize, publicKey)


if __name__ == '__main__':
    args = {}
    args['cloud'] = "india-openstack"
    args['username'] = "heshan"
    args['userId'] = "1"
    args['instanceId'] = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
    args['imageSize'] = "m1.tiny"
    args['publicKey'] = "heshan-key"
    
    manager = CloudConfigManager()
    manager.start_image(args)
    




    
