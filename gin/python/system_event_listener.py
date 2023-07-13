import os
import sys
import requests
from json import loads
from supervisor import childutils

from urlParser.parser import url_parse
from githubFileFetcher.githubFileFetcher import GithubFileFetcher

SYSTEM_NAME = os.getenv('SYSTEM_NAME') or 'web'

def parse_settings():
    PUSHDEER_KEY = os.getenv('GITHUB_FETCHER_SETTINGS')
    assert PUSHDEER_KEY, "GITHUB_FETCHER_SETTINGS is required"
    return url_parse(PUSHDEER_KEY)

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def main():
    protocal, params = parse_settings()
    func = protocal_map[protocal]
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
        func(params, text)
        sys.stdout.write('#' * 20)
        sys.stdout.write('\r\n\r\n\r\n')
        sys.stdout.flush()

def pushdeer(params: dict, text: str):
    f = GithubFileFetcher(auth_token=params['password'])
    repo, file_path = params['path'].split('/', 1)
    data = f.fetch(params['username'], repo, file_path)
    pushdeer_keys = loads(data)
    for key in pushdeer_keys:
        requests.get(f'https://api2.pushdeer.com/message/push?pushkey={key}&text=1{text}')

protocal_map = {
    'pushdeer': pushdeer
}

if __name__ == '__main__':
    main()
