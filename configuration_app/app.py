#! /usr/bin/env python3

import os
import time
import json
import base64
import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    status = get_status()
    return render_template('status.html', status=status)


@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method == 'GET':
        status = get_status()
        return render_template('status.html', status=status)
    if request.method == 'POST':
        return run_status_cmd(request.json)


@app.route('/config')
def config():
    congregations = read_congregations_json()
    return render_template('config.html', congregations=congregations)


@app.route('/congregations', methods=['GET', 'POST'])
def congregations():
    if request.method == 'POST':
        congs = request.get_data()
        save_congregations(congs)
        response = app.response_class(
            response=congs,
            status=200,
            mimetype='application/json'
        )
        os.system('/usr/bin/python /var/lib/meeting_scheduler/kill_all.py')
        os.system('/bin/systemctl restart meeting_scheduler.service')
        return response
    else:
        response = app.response_class(
            response=read_congregations_json(),
            status=200,
            mimetype='application/json'
        )
        return response


######## FUNCTIONS ##########

def read_congregations_json():
    congregations_json = '[]'
    if os.path.isfile('/boot/congregations.json'):
        congs = open('/boot/congregations.json', 'r')
        congregations_json = congs.read()
        congs.close()
    if len(congregations_json) == 0:
        return '[]'
    else:
        return congregations_json


def save_congregations(congregation_json):
    congs = open('/boot/congregations.json', 'wb')
    congs.write(congregation_json)
    congs.close()


def get_status():
    status_report = subprocess.Popen(
        '/var/lib/meeting_scheduler/status.py', stdout=subprocess.PIPE)
    return status_report.stdout.read().decode('utf-8').rstrip()


def run_status_cmd(status_cmd):
    cong_id = base64.urlsafe_b64encode(status_cmd['name'].lower().encode('utf-8')).decode('utf-8')
    if status_cmd['service'] == 'KHCONF':
        if status_cmd['action'] == 'start':
            subprocess.call(['/var/lib/meeting_scheduler/kill_all_khconf.py'])
            time.sleep(1)
        subprocess.call(['/var/lib/khconf/%s' % status_cmd['action'],
                         cong_id, '/var/lib/khconf/config/%s' % cong_id])
    if status_cmd['service'] == 'KHSTREAMER':
        if status_cmd['action'] == 'start':
            subprocess.call(['/var/lib/meeting_scheduler/kill_all_khstreamer.py'])
            time.sleep(1)
        subprocess.call(['/var/lib/khstreamer/%s' % status_cmd['action'],
                         cong_id, '/var/lib/khstreamer/config/%s' % cong_id])
    time.sleep(1)
    return get_status()


if __name__ == '__main__':
    while os.path.isfile('/etc/raspiwifi/host_mode'):
        time.sleep(10)
    app.run(host='0.0.0.0', port=80)
