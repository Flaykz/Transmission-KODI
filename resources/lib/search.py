# -*- coding: UTF-8 -*-
import sys
import re
import socket
import requests
import json
from transmissionrpc.t411 import T411 as t411
from urllib import quote_plus
from BeautifulSoup import BeautifulStoneSoup

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

# Error 503
class CPasBien(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'http://www.cpasbien.io/recherche/%s.html,trie-seeds-d'
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
        for item in soup.findAll('a', {'class':'titre'}):
            name = item.text.strip()
            url = item['href']
            div = item.findNext('div')
            poid = div.text
            div = item.findNext('div').findNext('div')
            seeds = int(div.text)
            div = item.findNext('div').findNext('div').findNext('div')
            leechers = int(div.text)
            torrents.append({
                'url': url,
                'name': name,
                'seeds': seeds,
                'leechers': leechers,
            })
        return torrents
##        p = []
##        if terms.find(' ') :
##            p = terms.split(' ')
##        else :
##            p.append(terms)
##        if p[0] == "series" or p[0] == "films" :
##            if len(p) == 1:
##                self.search_uri = 'http://www.cpasbien.pw/view_cat.php?categorie=%s'
##                url = self.search_uri % p[0]
##            else :
##                self.search_uri = 'http://www.cpasbien.pw/view_cat.php?categorie=%s&page=%s'
##                url = self.search_uri % (p[0],p[1])
##        else :
##            url = self.search_uri % '-'.join(terms.split(' '))
##		hdr = {
##			'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
##			'Accept' : 'image/webp,*/*;q=0.8',
##			'Accept-Language' : 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
##			'Connection' : 'keep-alive'
##		}
##        req = Request(url, headers=hdr)
##        #f = urlopen(req).read()
##        #f = urlopen(url)
##		f = urlopen(req)
##        soup = BeautifulSoup(f.read())
##        for item in soup.findAll('a', {'class':'titre'}):
##            name = item.text.strip()
##            url = item['href']
##            div = item.findNext('div')
##            poid = div.text
##            div = item.findNext('div').findNext('div')
##            seeds = int(div.text)
##            div = item.findNext('div').findNext('div').findNext('div')
##            leechers = int(div.text)
##			req = Request(url, headers=hdr)
##            f2 = urlopen(req)
##            soup2 = BeautifulSoup(f2.read())
##            url = 'http://www.cpasbien.pw' + soup2.find('a', {'id':'telecharger'})['href']
##            torrents.append({
##                'url': url,
##                'name': name,
##                'seeds': seeds,
##                'leechers': leechers,
##            })
##        return torrents
        
# Error 500
class GetStrike(Search):
    def __init__(self):
        self.search_uri = 'https://getstrike.net/api/torrents/search/?q=%s'
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def search(self, terms):
        torrents = []
        url = self.search_uri % '+'.join(terms.split(' '))
        try :
             f = requests.get(url, headers=self.headers)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        rep = json.loads(f.text)
        nbRes = rep[0]['results']
        for i in rep[1] :
            torrents.append({
                'url': i['download_link'],
                'name': i['torrent_title'],
                'seeds': i['seeds'],
                'leechers': i['leechers'],
            })
        return torrents

class T411(Search):
    def __init__(self):
        self.t = t411()

    def search(self, query) :
        torrents = []
        rep = self.t.search(query)
        for torrent in rep['torrents'] :
            torrents.append({"seeds":int(torrent['seeders']), "leechers":int(torrent['leechers']), "name":torrent['name'].encode('utf-8'), "url":torrent['id'].encode('utf-8')})
        return torrents

if __name__ == '__main__':
    sites = [Mininova(), Kickass(), L337x(), Lime(), EZTV(), T411()]
#    sites = [T411()] 
    terms = 'apollo 13'
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
