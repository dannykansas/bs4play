import glob
import logging

inpath = 'rawdata/'
outpath = 'cleandata/'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cleaner')

def get_files():
    filenames = glob.glob(inpath+'pagenum_*')
    log.info('Files loaded')
    for fileitem in filenames:
        clean_file(fileitem)
    
def clean_file(fileitem):
    with open(fileitem,'r') as f:
        try:
            string = f.read()
            # remove artifacts
            if string.startswith('"') and string.endswith('"'):
                string = string[1:-1]
            string = string.replace("\\n"," ")
            string = string.replace("\\r"," ")
            string = string.replace("\\\"",'"')
            write_file(string,fileitem)
        except Exception, err:
            log.exception('Error cleaning file ' + fileitem) 

def write_file(string,fileitem):
    with open(outpath+fileitem,'w') as c:
        try:
            c.writelines(string)
        except Exception, err:
            log.exception('Error writing cleaned file ' + fileitem)

if __name__ == '__main__':
    get_files()
