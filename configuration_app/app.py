#! /usr/bin/env python

import os
import time
import json

from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/config')
def index():
    congregations = read_congregations_json()
    return render_template('config.html', congregations = congregations)


@app.route('/congregations', methods = ['GET', 'POST'])
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


if __name__ == '__main__':
    while os.path.isfile('/etc/raspiwifi/host_mode'):
        time.sleep(10)
    app.run(host = '0.0.0.0', port = 80)
