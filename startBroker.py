import os
import swiftclient.client

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
from novaclient.client import Client
nc = Client('2',**config)

# Create instance
import time 
image = nc.images.find(name="Ubuntu Server 14.04 LTS (Trusty Tahr)")
flavor = nc.flavors.find(name="m1.medium")
network = nc.networks.find(label="ACC-Course-net")
keypair = nc.keypairs.find(name="mathieukeypair")
ud = open('userdata.yml', 'r')
nc.keypairs.list()
#f = open('cloud.key.pub','r')
#publickey = f.readline()[:-1]
#keypair = nc.keypairs.create('mathieukeypair',publickey)
#f.close()
server = nc.servers.create(name = "mat-test",image = image.id,flavor = flavor.id,network = network.id,
 key_name = keypair.name, userdata = ud)
time.sleep(5)
#try:
#	if nc.floating_ips.list():
#		floating_ip = nc.floating_ips.list()[0]
#		print "*** uses old ip: %s ***" %(floating_ip.ip)
#	else:
#		floating_ip = nc.floating_ips.create(nc['floating_ip_pool'])
#		print "*** no ip available, creating new ip: %s ***" %(floating_ip.ip)
#	server.add_floating_ip(floating_ip)
#except Exception as e:
#	raise ProviderException("Failed to attach a floating IP to the controller.\n{0}".format(e))

floating_ip_information_list = nc.floating_ips.list()
floating_ip_list = []
	#print floating_ip_information_list
for floating_ip_information in floating_ip_information_list:
#print floating_ip_information
	if getattr(floating_ip_information, 'fixed_ip') == None:
		floating_ip_list.append(getattr(floating_ip_information, 'ip'))

if len(floating_ip_list) == 0:
	new_ip = nc.floating_ips.create(getattr(nc.floating_ip_pools.list()[0],'name'))
	print new_ip
	floating_ip_list.append(getattr(new_ip, 'ip'))

floating_ip = floating_ip_list[0]

	#iplist = nc.floating_ips.list()
  	#if (len(iplist) < 1):
  	#	print "No IP:s available!"
   
  	#random_index = randrange(0,len(iplist))
  	#ip_obj = iplist[random_index] # Pick random address
  	#floating_ip = getattr(ip_obj, 'ip')
   
print "Attaching IP:"
print floating_ip
server.add_floating_ip(floating_ip)
#floating_ip = nc.floating_ips.create(nc.floating_ip_pools.list()[0].name)
#server.add_floating_ip(floating_ip)
#print floating_ip.ip

