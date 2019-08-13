#! /usr/bin/env python

import psutil
import urllib2
import base64
import json

from subprocess import call


def main():
    resp_obj = {'congregations': []}
    with open('/boot/congregations.json') as cong_json:
        # read congreation data from boot partition
        cong_data = json.load(cong_json)
        for cong in cong_data['congregations']:
            cong_id = base64.urlsafe_b64encode(cong['name'].lower())
            cong_obj = {
                'name': cong['name']
            }
            for p in psutil.process_iter():
                cmdline = p.cmdline()
                if len(cmdline) > 1 and cmdline[1] == '/var/lib/khconf/sipcall.py' and cmdline[2] == cong_id:
                    cong_obj['khConfConnected'] = True
                    cong_obj['khConfCount'] = get_khconf_count(
                        cong['khConfCountUsername'], cong['khConfCountPassword'])
                if len(cmdline) > 1 and cmdline[0] == '/usr/bin/darkice' and cmdline[2].endswith(cong_id):
                    cong_obj['khStreamerConnected'] = True
            if not 'khConfConnected' in cong_obj:
                cong_obj['khConfConnecgted'] = False
                cong_obj['khConfCount'] = 0
            if not 'khStreamerConnected' in cong_obj:
                cong_obj['khStreamerConnected'] = False
            resp_obj['congregations'].append(cong_obj)
    print(json.dumps(resp_obj))


def get_khconf_count(username, password):
    count = 'Unknown'
    if username and password:
        request = urllib2.Request('https://report.khconf.com/api.php/count')
        auth = base64.b64encode('%s:%s' % (username, password))
        request.add_header("Authorization", "Basic %s" % auth)
        try:
            count = json.loads(urllib2.urlopen(request).read())['count']
        except Exception as ex:
            count = str(ex)
    return count


if __name__ == '__main__':
    main()
