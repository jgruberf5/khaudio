#! /usr/bin/env python

import sys
import os
import signal
import threading

from subprocess import Popen, PIPE, STDOUT


def wait_on_call(proc):
    proc.wait()


def call(conf_id, config_file):
    # write out pid file
    pidfile = open('/var/run/khconf/%s.pid' % conf_id, 'w')
    pidfile.write("%d" % os.getpid())
    pidfile.close()

    sip_call_cmd = ['/usr/bin/pjsua', '--config=%s' % config_file]
    print('starting call %s' % " ".join(sip_call_cmd))

    proc = Popen(
        ['/usr/bin/pjsua', '--config=%s' % config_file],
        stdout=PIPE, stdin=PIPE, stderr=PIPE)
    call_thread = threading.Thread(target=wait_on_call, args=[proc]).start()

    def hangup(signum, frame):
        sys.stdout.flush()
        proc.communicate('ha\n')
        proc.communicate('q\n')

    signal.signal(signal.SIGTERM, hangup)
    signal.signal(signal.SIGINT, hangup)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: start confernce_name config_file\n")
        sys.exit(1)
    else:
        call(sys.argv[1], sys.argv[2])
