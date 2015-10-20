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

@app.route('/')
def index():
    os.environ['LC_ALL'] = "en_US.utf8"
    return render_template('index.html')


@app.route('/airform')
def airform():
    return render_template('airform.html')
    
    
@app.route('/submit', methods = ['POST'])
def submit():
    angle_start = request.form['angle_start']
    angle_stop = request.form['angle_stop']
    n_angles = request.form['n_angles']
    n_nodes = request.form['n_nodes']
    n_levels = request.form['n_levels']
    toRun = './run.sh' + ' ' + angle_start + ' ' + angle_stop + ' ' + n_angles + ' ' + n_nodes + ' ' + n_levels
    print toRun
    subprocess.call(toRun, shell = True)
    return redirect('/convert')


@app.route('/convert')
def convert():
    for fn in os.listdir('/home/ubuntu/project/msh'):
        print str(fn)
        name = "dolfin-convert " + "/home/ubuntu/project/msh/" + fn + " " + "/home/ubuntu/project/msh/" + fn[:-4] + ".xml"
        print name
        subprocess.call(name, shell=True)
    return redirect('/airform')


@app.route('/airfoil', methods = ['POST'])
def airfoil():
    num_samples = request.form['num_samples']
    visc = request.form['visc']
    speed = request.form['speed']
    time = request.form['time']

    files = os.listdir('/home/ubuntu/project/msh')
    xmlfiles = []
    for file in files:
        if (file.endswith('.xml')):
            xmlfiles.append(file)

    for file in xmlfiles:
        toRun = './navier_stokes_solver/airfoil' + ' ' + num_samples + ' ' + visc + ' ' + speed + ' ' + time + ' ' + 'msh/' + file
        print toRun
        subprocess.call(toRun.split(" "))
        os.rename("drag_ligt.m", file[:-4] + ".m")
    return redirect('/')



@app.route('/params')
def emails():
    return render_template('params.html', params=params)

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
