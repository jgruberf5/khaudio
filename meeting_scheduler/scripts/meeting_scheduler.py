#! /usr/bin/env python

import json
import base64
import jinja2
import schedule
import time
from subprocess import call


def main():
    with open('/boot/congregations.json') as cong_json:
        # read congreation data from boot partition
        cong_data = json.load(cong_json)

        # read KHconf SIP client configuration template
        khconf_template = None
        with open('/var/lib/khconf/config/template.conf', 'r') as t_file:
            khconf_template = t_file.read()
        # read KHstreamer darkice configuration template
        khstreamer_template = None
        with open('/var/lib/khstreamer/config/template.conf', 'r') as t_file:
            khstreamer_template = t_file.read()

        for cong in cong_data['congregations']:
            # read in meeting metadata
            print('processing scheduled tasks for the %s congregation\n' %
                  cong['name'])
            id = base64.urlsafe_b64encode(cong['name']).lower()
            mwmd = cong['midweekMeetingDay'].lower()
            mwm_start = cong['midweekMeetingStartTime']
            mwm_stop = cong['midweekMeetingStopTime']
            pmd = cong['publicMeetingDay'].lower()
            pm_start = cong['publicMeetingStartTime']
            pm_stop = cong['publicMeetingStopTime']

            # setup scheduled tasks for KHConf SIP calls
            if 'khConfPhoneNumber' in cong:
                # populate configuration data
                khconf = jinja2.Template(khconf_template).render(
                    caller_id=cong['khConfCallerIDNumber'],
                    congregation_number=cong['khConfPhoneNumber'],
                    admin_pin=cong['khConfAdminPIN'],
                    sip_gateway=cong['khConfSIPGateway'],
                    congregation_name=''.join(cong['name'].split())
                )
                khconf_filename = "/var/lib/khconf/config/%s" % id
                with open(khconf_filename, 'w') as conf_file:
                    conf_file.write(khconf)
                start_script = ['/var/lib/khconf/start',
                                id, '/var/lib/khconf/config/%s' % id, '&']
                stop_script = ['/var/lib/khconf/stop',
                               id, '/var/lib/khconf/config/%s' % id, '&']
                print('\tplacing a SIP call to KHConf on %s at %s' %
                      (mwmd, mwm_start))
                getattr(schedule.every(), mwmd).at(mwm_start).do(
                    call, start_script)
                print('\tterminating a SIP call to KHConf on %s at %s' %
                      (mwmd, mwm_stop))
                getattr(schedule.every(), mwmd).at(mwm_stop).do(
                    call, stop_script)
                print('\tplacing a SIP call to KHConf on %s at %s' %
                      (pmd, pm_start))
                getattr(schedule.every(), pmd).at(pm_start).do(
                    call, start_script)
                print('\tterminating a SIP call to KHConf on %s at %s' %
                      (pmd, pm_stop))
                getattr(schedule.every(), pmd).at(pm_stop).do(
                    call, stop_script)
            # setup scheduled tasks for KHstreamer mp3 streaming
            if 'khStreamerAudioServer' in cong:
                # populate configuration data
                khstreamer = jinja2.Template(khstreamer_template).render(
                    audio_server=cong['khStreamerAudioServer'],
                    audio_port=cong['khStreamerAudioServerPort'],
                    audio_mount=cong['khStreamerAudioMountPoint'],
                    audio_password=cong['khStreamerPassword'],
                    congregation_name=cong['name']
                )
                khstreamer_filename = "/var/lib/khstreamer/config/%s" % id
                with open(khstreamer_filename, 'w') as conf_file:
                    conf_file.write(khstreamer)
                start_script = ['/var/lib/khstreamer/start',
                                id, '/var/lib/khstreamer/config/%s' % id, '&']
                stop_script = ['/var/lib/khstreamer/stop',
                               id, '/var/lib/khstreamer/config/%s' % id, '&']
                print('\tstarting a mp3 stream to KHStreamer on %s at %s' %
                      (mwmd, mwm_start))
                getattr(schedule.every(), mwmd).at(mwm_start).do(
                    call, start_script)
                print('\tterminating a mp3 stream to KHStreamer on %s at %s' %
                      (mwmd, mwm_stop))
                getattr(schedule.every(), mwmd).at(mwm_stop).do(
                    call, stop_script)
                print('\tstarting a mp3 stream to KHStreamer on %s at %s' %
                      (pmd, pm_start))
                getattr(schedule.every(), pmd).at(pm_start).do(
                    call, start_script)
                print('\tterminating a mp3 stream to KHStreamer on %s at %s' %
                      (pmd, pm_stop))
                getattr(schedule.every(), pmd).at(pm_stop).do(
                    call, stop_script)
            print('\n')

    print('next job will run at: %s\n' %
          schedule.next_run().strftime("%a %b %d %Y %H:%M:%S"))

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
