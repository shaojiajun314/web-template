import os
import sys
import requests
from supervisor import childutils

SYSTEM_NAME = os.getenv('SYSTEM_NAME') or 'web'
PUSHDEER_KEY = os.getenv('PUSHDEER_KEY') or 'PDU23127TFIOKLFU8jnDTjuiEPW82hdU2FSdTgRRY'

assert PUSHDEER_KEY, 'env PUSHDEER_KEY is required'

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def main():
    while 1:
        write_stdout('READY\n')
        line = sys.stdin.readline()
        write_stderr(line)
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        write_stderr(data)
        write_stdout('RESULT 2\nOK')
        headers, payload = childutils.listener.wait(sys.stdin, sys.stdout)
        pheaders, pdata = childutils.eventdata(payload + '\n')
        text = f'system: {SYSTEM_NAME}, {", ".join([(k + ": " + v) for k, v in pheaders.items()])}'
        requests.get(f'https://api2.pushdeer.com/message/push?pushkey={PUSHDEER_KEY}&text=1{text}')
        sys.stdout.write('#' * 20)
        sys.stdout.write('\r\n\r\n\r\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main()
