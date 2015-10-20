import os
import swiftclient.client
from celery import Celery, group, subtask
from flask import Flask, jsonify
import subprocess
import sys
import urllib2
import json
from collections import Counter
from cStringIO import StringIO

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def twts():

   	req = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets")
	response = urllib2.urlopen(req)
	names = response.read().split()


	worker_tasks = []
	for name in names:
		worker_tasks.append(parse_tweets.s(name))

	# Start workers
	tasks = group(worker_tasks)
	res = tasks.apply_async()

	# Wait for result to be ready
	print "Workers started... waiting for them to finnish"
	while res.ready() != True:
		pass
	
	dict_list = res.get()
	

	# Sum the result
	total = {"han":0, "hon": 0, "den":0 ,"det":0 , "denna":0, "denne":0 ,"hen":0}
	c = Counter()
	for dic in dict_list:
		c.update(dic)
		
    	return jsonify(dict(c)), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
