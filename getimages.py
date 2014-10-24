import csv
import urllib
csvfile = 'final/all.csv'
csvfile = csv.reader(open(csvfile))
default_profile_img = ''


for row in csvfile:
    if row[5] != default_profile_img:
       urllib.urlretrieve(row[5],'final/images/'+row[5].split('/')[-1])
 
