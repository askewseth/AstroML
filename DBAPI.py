import urllib2
from BeautifulSoup import BeautifulSoup

def get_file(star_name, hjd_date, csv=True):
    whole_date, dec_date = str(hjd_date).split('.')
    url = 'http://tsethaskew.me/static/' + star_name + '/csv/' + hjd

def get_file_path(file_name, star_name=None, csv=True):
    if csv:
        url = 'http://tsethaskew.me/static/' + file_name.split('_')[0] + '/csv/' + file_name
        page = urllib2.urlopen(url)
        text = page.read().splitlines()
        data = [map(float, x.split(',')) for x in text]
        return data
    else:
        url = 'http://tsethaskew.me/static/' + star_name + '/fits/' + file_name

def get_stars():
    url = 'http://tsethaskew.me/static/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    stars = [str(x.get('href')[:-1]) for x in links]
    return stars
