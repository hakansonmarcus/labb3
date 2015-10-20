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

cel = Celery('test_task', backend='amqp', broker='amqp://dj:dj@130.238.29.85:5672/djvhost')

#cel = Celery('test_task', backend='amqp', broker='amqp://')

@cel.task
def parse_tweets(filename):
	print "Working on " + filename
	#(response, obj)=conn.get_object('tweets', filename)
	req = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + filename)
	response = urllib2.urlopen(req)
	obj = response.read()
	swe_pronouns = {"han":0, "hon": 0, "den":0 ,"det":0 , "denna":0, "denne":0 ,"hen":0}
	pronouns_list = ["han","hon","hen","det","den","denne","denna"]
	txtfile = StringIO(obj)
	for tweet in txtfile:
		if tweet == "\n":
			pass
		else:
			td = json.loads(tweet)
			if not 'retweeted_status' in td:
				obj_name = td['text']
				list_split = obj_name.split()
				for word in list_split:
					for pronoun in pronouns_list:
						if word.lower() == pronoun:
							swe_pronouns[pronoun] += 1

	print "Result from " + filename +" is " + str(swe_pronouns)
	return swe_pronouns


