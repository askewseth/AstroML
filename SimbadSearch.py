"""Module for validating searches and finding alternate names."""
import os
from astroquery.simbad import Simbad

def get_name(entry):
    """Get proper name for star given it's name."""
    # if 'hd' not in entry[:3].lower() and ' ' not in entry and len(entry) > 5:
    #     entry = entry[:3] + ' ' + entry[3:]

    try:
        result = Simbad.query_object(entry, verbose=False)
        if result is not None:
            obj_name = filter(lambda x: x != '*', result[0][0].split())
            prop_name = (' ').join(map(lambda x: x.capitalize(), obj_name))
            # if a hd name capitalize hd
            if prop_name[:2].lower() == 'hd':
                prop_name = 'HD' + prop_name[2:]
        else:
            print "Not Found"
            prop_name = None
        return prop_name
    except:
        print "ERROR"
        return None
