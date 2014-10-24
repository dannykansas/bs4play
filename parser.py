import csv
import glob
import logging
from BeautifulSoup import BeautifulSoup

inpath = 'datadump/'
baseurl = ''

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_files():
    filenames = sorted(glob.glob(inpath+'pagenum_*'))
    for datafile in filenames:
        get_container(datafile)

def get_container(datafile):
    with open(datafile) as doc:
        try:
            soup = BeautifulSoup(doc)
            # h3 tags indicate the start of each chunk of office data 
            # but they do not contain the actual data, so we need the 
            # parent div one step up from the selected h3 tag
            for office in soup.findAll("h3"):
                container = office.findParent("div")
                get_persons(office,container)
        except Exception, err:
            log.exception('Error soupifying ' + datafile)

def get_persons(office,container):
    for person in container.findAll("div", attrs={"class":"person inner "}):
        try:
            record = {}
            record['office'] = office.text
            record['imgurl'] = baseurl + person.find("img")['src']
	    record['status'] = person.find("span",
                    attrs={"class":"label label-default"}).text
	    record['name'] = person.find("h4",
                    attrs={"class":"name"}).text.replace(record['status'],"")
	    record['title'] = person.h5.span.text
	    record['district'] = person.find("div", attrs={"class":"district"}).text
	    record['profileid'] = person.find("a", attrs={"data-loaded":"false"})['data-id']
            write_office(record)
        except Exception, err:
            log.exception('Error at parsing person from datafile')

def write_office(record):
    with open('final/all.csv','a') as f:
        writer = csv.DictWriter(f,
                fieldnames=record.keys(),quoting=csv.QUOTE_ALL)
        writer.writerow(record)

if __name__ == '__main__':
    load_files()
