# -*- coding: UTF-8 -*-
import sys
import re
import socket
import requests
import json
from transmissionrpc.t411 import T411 as t411
from urllib import quote_plus
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
import cfscrape

socket.setdefaulttimeout(15)

class Search:
    def __init__(self):
        return NotImplemented
    def search(terms):
        return NotImplemented

class Mininova(Search):
    def __init__(self):
        self.search_uri = 'http://www.mininova.org/rss/%s'
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()        
        soup = BeautifulStoneSoup(f.text)
        for item in soup.findAll('item'):
            (seeds, leechers) = re.findall('Ratio: (\d+) seeds, (\d+) leechers', item.description.text)[0]
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(seeds),
                'leechers': int(leechers),
            })
        return torrents

#Bug Out of proxie ?
class TPB(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'https://thepiratebay.se/search/%s/'
        self.headers = {'User-Agent': self.user_agent}

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url, headers=self.headers)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for details in soup.findAll('a', {'class': 'detLink'}):
            name = details.text
            url = details.findNext('a', {'href': re.compile('^magnet:')})['href']
            td = details.findNext('td')
            seeds = int(td.text)
            td = td.findNext('td')
            leechers = int(td.text)
            torrents.append({
                'url': url,
                'name': name,
                'seeds': seeds,
                'leechers': leechers,
            })
        return torrents

class Kickass(Search):
    def __init__(self):
        self.search_uri = 'https://kat.cr/usearch/%s/?field=seeders&sorder=desc&rss=1'

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for item in soup.findAll('item'):
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(item.find('torrent:seeds').text),
                'leechers': int(item.find('torrent:peers').text),
            })
        return torrents

#Long, A vérifier
class L337x(Search):
    def __init__(self):
        self.uri_prefix = 'http://1337x.to'
        self.search_uri = self.uri_prefix + '/sort-search/%s/seeders/desc/1/'

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for details in soup.findAll('a', {'href': re.compile('^/torrent/')}):
            div = details.findNext('div')
            seeds = int(div.text)
            div = div.findNext('div')
            try :
                f_link = requests.get(self.uri_prefix + details['href'])
            except :
                raise Exception('something wrong')
            if (f.status_code != requests.codes.ok) :
                f.raise_for_status()
            soup_link = BeautifulStoneSoup(f_link.text)
            link = soup_link.find('a', {'href': re.compile('^magnet:')})
            if not link:
                continue
            torrents.append({
                'url': link['href'],
                'name': details.text,
                'seeds': seeds,
                'leechers': int(div.text),
            })
        return torrents

# URL ?
class YTS(Search):
    def __init__(self):
        self.search_uri = 'http://yts.to/rss/%s/all/all/0'

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
            f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for item in soup.findAll('item'):
            item_quality = item.link.text.rpartition('_')[2]
            try :
                item_f = requests.get(item.link.text)
            except :
                raise Exception('something wrong')
            if (f.status_code != requests.codes.ok) :
                f.raise_for_status()
            item_soup = BeautifulStoneSoup(item_f.text)
            qualities = [s.text.strip() for s in
                         item_soup.findAll('span', {'class': re.compile('^tech-quality')})]
            q_index = qualities.index(item_quality)
            span = item_soup.findAll('span', {'title': 'Peers and Seeds'})[q_index]
            ps_pos = len(span.parent.contents) - 1
            ps = span.parent.contents[ps_pos].split('/')
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(ps[1]),
                'leechers': int(ps[0])
            })
        return torrents

class Lime(Search):
    def __init__(self):
        self.search_uri = 'https://www.limetorrents.cc/searchrss/%s/'

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for item in soup.findAll('item'):
            (seeds, leechers) = re.findall('Seeds: (\d+) , Leechers (\d+)', item.description.text)[0]
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(seeds),
                'leechers': int(leechers)
            })
        return torrents

class EZTV(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'https://eztv.ag/search/%s'
        self.headers = {'User-Agent': self.user_agent}

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try :
             f = requests.get(url, headers=self.headers)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
        for (c, item) in enumerate(soup.findAll('a', {'class': 'magnet'})):
            if c == 30: break
            info = item.findPrevious('a')
            link = self.search_uri % quote_plus(info['href'])
            try :
                item_f = requests.get(link, headers=self.headers)
            except :
                raise Exception('something wrong')
            if (item_f.status_code != requests.codes.ok) :
                item_f.raise_for_status()
            item_soup = BeautifulStoneSoup(item_f.text)
            sp = item_soup.findAll('span', {'class': re.compile('^stat_')})
            if sp:
                sp = [int(i.text.replace(',', '')) for i in sp]
            else:
                sp = [0, 0]
            torrents.append({
                'url': item['href'],
                'name': info.text,
                'seeds': sp[0],
                'leechers': sp[1]
            })
        return torrents

class Torrent9(Search):
    def __init__(self):
        self.url = "https://www.torrent9.blue"
        self.path = "/search_torrent/"
        self.error = u"Aucun torrents disponibles correspondant à votre recherche :("
        scraper = cfscrape.create_scraper(delay=5)
        self.tokens, self.userAgent = scraper.get_tokens(self.url)
        self.headers = {'User-Agent': self.userAgent}
        
    def search(self, terms):
        torrents = []
        search = terms
        search = search.replace("-", "")
        search = search.replace(" ", "-")
        search = search + ".html"
        try :
            f = requests.get(self.url + self.path + search, cookies=self.tokens, headers=self.headers)
        except:
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        response = f.text
        if self.error in response:
            raise Exception("no torrent")
        else:
            soup = BeautifulSoup(response, 'html.parser')
            table = soup.find('table', {"class" : "table table-striped table-bordered cust-table"})
            tr = table.find_all("tr")
            for torrent in tr:
                attributs = torrent.find_all("td")
                f2 = requests.get(self.url + attributs[0].find("a")['href'], cookies=self.tokens, headers=self.headers)
                soup = BeautifulSoup(f2.text, 'html.parser')
                dl = soup.find('a', {'class': "btn btn-danger download"})
                torrents.append({
                    'url': self.url + dl['href'],
                    'name': attributs[0].find("a").text,
                    'seeds': int(attributs[2].text),
                    'leechers': int(attributs[3].text),
                })
        return torrents
        
if __name__ == '__main__':
#    sites = [Mininova(), Kickass(), L337x(), Lime(), EZTV(), T411()]
    sites = [Torrent9()] 
    terms = 'Avenger'
    if len(sys.argv) > 1:
        terms = sys.argv[1]
    print 'Searching for "' + terms + '"'
    for site in sites:
        print site.__class__.__name__.center(79, '=')
        torrents = site.search(terms)
        print 'Total found = ' + str(len(torrents))
        counter = 0
        for torrent in torrents:
            counter = counter + 1
            print "seeds :" + str(torrent['seeds']) + " leechers: " + str(torrent['leechers']) + " name: " + torrent['name'].encode('utf-8') + " url: " + torrent['url'].encode('utf-8')
            if (counter == 3): 
                break
