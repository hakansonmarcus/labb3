import os
from random import randrange
import swiftclient.client

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
from novaclient.client import Client
nc = Client('2',**config)

# Create instance
def init(worker_number):
	worker_name = "MH_Worker%i" %(worker_number)
	import time
	image = nc.images.find(name="Ubuntu Server 14.04 LTS (Trusty Tahr)")
	flavor = nc.flavors.find(name="m1.medium")
	network = nc.networks.find(label="ACC-Course-net")
	keypair = nc.keypairs.find(name="MarcusKey")
	ud = open('userdata.yml', 'r')
	nc.keypairs.list()

	server = nc.servers.create(name = worker_name ,image = image.id,flavor = flavor.id,network = network.id,
	key_name = keypair.name, userdata = ud)
	time.sleep(5)

	floating_ip_information_list = nc.floating_ips.list()
	floating_ip_list = []
	#print floating_ip_information_list
	for floating_ip_information in floating_ip_information_list:
		if getattr(floating_ip_information, 'fixed_ip') == None:
			floating_ip_list.append(getattr(floating_ip_information, 'ip'))

	if len(floating_ip_list) == 0:
		new_ip = nc.floating_ips.create(getattr(nc.floating_ip_pools.list()[0],'name'))
		print new_ip
		floating_ip_list.append(getattr(new_ip, 'ip'))

	floating_ip = floating_ip_list[0]

  	print "Attaching IP:"
  	print floating_ip
  	server.add_floating_ip(floating_ip)

for i in range(0,2):
	init(i)
