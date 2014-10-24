#!/usr/bin/python

import sys
import requests
import simplejson as json
import time
import logging

outputprefix  = 'default-'
baseurl = ''
zipfile = 'zips.in'
intensity = 3

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def load_zips(baseurl,zipfile):
    zips = []
    with open(zipfile, 'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        line = line.replace('"', '').strip()
        line = line.split(',')
        if len(line[0]) == 5:  # reject clearly invalid zipcodes
            zips.append(line[0])
        else:
            log.info(line[0] + " is too many chars: " + len(line[0]))

    log.info("Loaded " + str(len(zips)) + " zipcodes")
    get_results(baseurl,zips)


def get_results(baseurl,zips):
    for i in zips:
        r = requests.post(baseurl,data={'nameOrZip':i,'pageSize':'2000'})
        try:
            success = r.json()["Success"]
            if success is None: 
                log.info(i + ' returned None')
            elif success == True:
                write_results(i,r)            
                time.sleep(intensity) # be kind and don't hammer their servers too hard
            elif success == False:
                log.info(i + ' was not successful.')
            else:
                log.info(i + ' gave ambiguous response.')
        except Exception, err:
            log.exception('Exception at file ' + i)

def write_results(i,r):
    with open("outfiles/"+outputprefix+i,'w') as o:
        try:
            o.writelines(json.dumps(r.json()["Content"]))
        except Exception, err:
            log.exception('Error in writing file' + i)

if __name__ == '__main__':
    load_zips(baseurl,zipfile)

