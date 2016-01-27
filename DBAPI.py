import urllib2
from BeautifulSoup import BeautifulSoup

def get_file(star_name, hjd_date, csv=True):
    '''
    Gets file given name of star and HJD of observation
    '''
    # whole_date, dec_date = str(hjd_date).split('.')
    # url = 'http://tsethaskew.me/static/' + star_name + '/csv/' + hjd
    if csv:
        url = 'http://tsethaskew.me/static/' + star_name + '/csv/'
    else:
        url = 'http://tsethaskew.me/static/' + star_name + '/fits/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    files = [str(x.get('href')[:-4]) for x in links]
    dates_full = []
    for x in files:
        arr = x.split('_')
        num = float(arr[1] + '.' + arr[2])
        dates.append([num,x])

def get_file_name(file_name, star_name, csv=True):
    '''
    Gets file given name of file and the name of the star
    '''
    try:
        url = 'http://tsethaskew.me/static/' + star_name + '/csv/' + file_name
        page = urllib2.urlopen(url)
        str_array = page.read().splitlines()
        float_array = []
        for x in str_array:
            float_array.append(map(float, x.split(',')))

    except:
        float_array = [None]
    return float_array

# print get_file_name('hd10516_2450709_60868.csv', 'phiper')

def get_file_path(file_name, csv=True):
    '''
    Gets file given full file name, gets star info from full name
    '''
    if csv:
        url = 'http://tsethaskew.me/static/' + file_name.split('_')[0] + '/csv/' + file_name
        page = urllib2.urlopen(url)
        text = page.read().splitlines()
        data = [map(float, x.split(',')) for x in text]
        return data
    else:
        url = 'http://tsethaskew.me/static/' + star_name + '/fits/' + file_name

def get_dates(star_name, csv=True):
    '''
    Returns list of all HJD dates given the name of the star
    '''
    if csv:
        url = 'http://tsethaskew.me/static/' + star_name + '/csv/'
    else:
        url = 'http://tsethaskew.me/static/' + star_name + '/fits/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    files = [str(x.get('href')[:-4]) for x in links]
    dates = []
    for x in files:
        arr = x.split('_')
        num = float(arr[1] + '.' + arr[2])
        dates.append(num)
    return dates

def get_files(star_name, csv=True):
    '''
    Returns a list of full file names in the DB for a given star
    '''
    if csv:
        url = 'http://tsethaskew.me/static/' + star_name + '/csv/'
    else:
        url = 'http://tsethaskew.me/static/' + star_name + '/fits/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    files = [str(x.get('href')[:-4]) for x in links]
    return files

def get_stars():
    url = 'http://tsethaskew.me/static/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    stars = [str(x.get('href')[:-1]) for x in links]
    return stars

def get_all_files(star_name, csv=True):
    # Make sure star valid
    stars = get_stars()
    if star_name not in stars:
        for x,y in enumerate(stars):
            print x, ' : ', y
        print 'The star name you entered is not in the database'
        reply = input('Enter the number of the star you want: ')
        star_name = stars[reply]
    # Get all the links
    file_links = get_files(star_name)
    files = [x + '.csv' for x in file_links]
    holder = []
    for f in files:
        holder.append(get_file_name(f, star_name))
    return holder

def test():
    all_files = get_all_files('phiper')
    lens = [len(x) for x in all_files]
    return [all_files, lens]
