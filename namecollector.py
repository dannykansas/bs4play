#!/usr/bin/python

import sys
import logging
import requests
import simplejson as json
import time

outprefix = 'rawdata/'
baseurl = ''

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# TODO: get count from an initial query, right now it is based on a manual
# check
count = 1639

def get_results(baseurl,count):
    i = 1
    while i < count:
        # retrieve data for each zipcode
        r = requests.post(baseurl,data={'nameOrZip':' ',
                                        'searchType':'1',
                                        'page':i
                                        })
        try:
            success = r.json()["Success"]
            if success is None: 
                log.info('Page ' + str(i) + ' returned None')
            elif success == True:
                write_results(i,r)            
                log.info('Page ' + str(i) + ' retrieved successfully.')
                time.sleep(5) 
            elif success == False:
                log.info('Page ' + str(i) + ' was not successful.')
            else:
                log.info('Page ' + str(i) + ' gave ambiguous response.')
        except Exception, err:
            log.exception(str(i) + " caused an error.")
        i = i + 1

def write_results(i,r):
    with open(outprefix+"pagenum_"+str(i),'w') as o:
        try:
            o.writelines(json.dumps(r.json()["Content"]))
        except Exception, err:
            log.exception('Error writing ' + i + ' to file.')

if __name__ == '__main__':
    get_results(baseurl,count)
