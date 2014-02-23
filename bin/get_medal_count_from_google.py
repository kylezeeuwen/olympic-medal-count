
import os
from urllib2 import urlopen, Request
from lxml.html import fromstring
import pprint
import json
import argparse
import sys

class FromWeb():
    '''Get the medal results from the web'''

    def __init__(self, url_string):
        print "Instantiating FromWeb"
        self.url_string = url_string
        self.req = Request(self.url_string,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        }) 
 
    def getDom(self):
        html = urlopen(self.req).read()
        dom = fromstring(html)
        dom.make_links_absolute(self.url_string)
        self.dom = dom

    def parseDom(self):
        table = self.dom.cssselect('.obcontainer table')[1]
        countries = [span.text_content() for span in table.cssselect('td a span')] 
        counts = [td.text_content() for td in table.cssselect('td div._bs')]
        
        self.stats = {}
        if (len(countries) * 3 != len(counts)):
            print "Warn: counts dont match something bad countries %d counts %s" % (len(countries), len(counts)) 

        for i, country in enumerate(countries):
            self.stats[country] = {
                'gold'   : counts[i*3 + 0],
                'silver' : counts[i*3 + 1],
                'bronze' : counts[i*3 + 2],
            }

    def getStats(self):
        self.getDom()
        self.parseDom()

        json_file = open('results.json', 'w')
        json.dump(self.stats,json_file)
        json_file.close()

        return self.stats

class FromFile():
    '''Get the medal results from a file'''

    def __init__(self, file_path):
        print "Instantiating FromFile"
        self.file_path = file_path

    def getStats(self):
        json_file = open(self.file_path, 'r')
        self.stats = json.load(json_file)
        json_file.close()
        return self.stats
    
def get_top_countries_by_total(stats,num_to_print,sortkey='total'):

    listed = map(lambda x : { 
        'country' : x, 
        'gold' : int(stats[x]['gold']), 
        'silver' : int(stats[x]['silver']), 
        'bronze' : int(stats[x]['bronze']),
        'total' : int(stats[x]['gold']) + int(stats[x]['silver']) + int(stats[x]['bronze']), 
    }, stats.keys())

    sorted_list = sorted(listed,key=lambda entry : -1 * entry[sortkey])
    return sorted_list[0:num_to_print]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="where do we get the datas?", type=str, choices=['FromFile', 'FromWeb'], default='FromFile')
    parser.add_argument("--top", help="How many coutries to list?", type=int, default=5)
    parser.add_argument("--ordered", help="How to sort countries : gold count or total count?", type=str, choices=['total', 'gold'], default='total')
    cli_args = parser.parse_args()    

    default_args = {
        'FromWeb' : r'https://www.google.com.au/search?q=olympic+medal+count+2014',
        'FromFile' : r'/home/dev/projects/olympic-count/results.json',
    }
    pp = pprint.PrettyPrinter(indent=4)
    
    # if module was not '__main__' i would use importlib.import_module(module_name)
    module = sys.modules['__main__']
    class_obj = getattr(module,cli_args.source)

    source = class_obj(default_args[cli_args.source])
    stats = source.getStats()

    top_countries = get_top_countries_by_total(stats,cli_args.top, cli_args.ordered)
    formatted = ["{country:<20} - {total:<3} : {gold:<2} Gold, {silver:<2} Silver, {bronze:<2} Bronze".format(**entry) for entry in top_countries]
    print "\n".join(formatted)


