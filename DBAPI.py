import urllib2
from BeautifulSoup import BeautifulSoup


def get_file(star_name, hjd_date, csv=True):
    """Get file given name of star and HJD of observation."""
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
    dates = []
    for x in files:
        arr = x.split('_')
        num = float(arr[1] + '.' + arr[2])
        dates.append([num, x])
    # Currently broken


def get_file_name(file_name, star_name, csv=True):
    """Get file given name of file and the name of the star."""
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
    """Get file given full file name, gets star info from full name."""
    if csv:
        url = 'http://tsethaskew.me/static/' + file_name.split('_')[0] +\
            '/csv/' + file_name
        page = urllib2.urlopen(url)
        text = page.read().splitlines()
        data = [map(float, x.split(',')) for x in text]
        return data
    else:
        url = 'http://tsethaskew.me/static/' + file_name + '/fits/' + file_name


def get_dates(star_name, csv=True):
    """Return list of all HJD dates given the name of the star."""
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
    """Return a list of full file names in the DB for a given star."""
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
    """Return a list of all of the stars in the datbase."""
    url = 'http://tsethaskew.me/static/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    links = soup.contents[2].contents[3].contents[3].findAll('a')[5:]
    stars = [str(x.get('href')[:-1]) for x in links]
    return stars


def show_stars():
    """Print an enumerated list of all of the stars in the database."""
    stars = get_stars()
    for x, star in enumerate(stars):
        print x, ' : ', star


def get_all_files(star_name, csv=True):
    """Get all file names for a given star."""
    # Make sure star valid
    stars = get_stars()
    if star_name not in stars:
        show_stars()
        print 'The star name you entered is not in the database'
        reply = input('Enter the number of the star you want: ')
        star_name = stars[reply]
    # Get all the links
    file_links = get_files(star_name)
    files = [x + '.csv' for x in file_links]
    holder = []
    for f in files:
        holder.append(get_file_name(f, star_name))
    # return holder
    dates = get_dates(star_name)
    final_arr = zip(dates, holder)
    final_dic = {x: y for x, y in final_arr}
    return final_arr, final_dic

# get_all_files('psiper')


def test():
    """test method."""
    all_files = get_all_files('phiper')
    lens = [len(x) for x in all_files]
    return [all_files, lens]
