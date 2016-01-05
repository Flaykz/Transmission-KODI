<<<<<<< HEAD
# -*- coding: UTF-8 -*-
=======
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
import sys
import re
import socket
import requests
import json
from transmissionrpc.t411 import T411 as t411
from urllib2 import urlopen, Request, URLError, HTTPError
from urllib import quote, quote_plus, urlencode
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

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
<<<<<<< HEAD
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()        
        soup = BeautifulStoneSoup(f.text)
=======
        f = urlopen(url)
        soup = BeautifulStoneSoup(f.read())
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
        for item in soup.findAll('item'):
            (seeds, leechers) = re.findall('Ratio: (\d+) seeds, (\d+) leechers', item.description.text)[0]
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(seeds),
                'leechers': int(leechers),
            })
        return torrents
<<<<<<< HEAD

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
=======
class TPB(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uris = ['https://thepiratebay.pw/search/%s/',
                            'http://pirateproxy.net/search/%s/']
    def search(self, terms):
        torrents = []
        f = None
        for url in [u % quote(terms) for u in self.search_uris]:
            req = Request(url)
            req.add_header('User-Agent', self.user_agent)
            try:
                f = urlopen(req)
                break
            except URLError:
                continue
        if not f:
            raise Exception('Out of pirate bay proxies')
        soup = BeautifulSoup(f.read())
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
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
<<<<<<< HEAD

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
=======
class Kickass(Search):
    def __init__(self):
        self.search_uri = 'http://kickass.to/usearch/%s/?field=seeders&sorder=desc&rss=1'
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        try:
            f = urlopen(url)
            soup = BeautifulStoneSoup(f.read())
            for item in soup.findAll('item'):
                torrents.append({
                    'url': item.enclosure['url'],
                    'name': item.title.text,
                    'seeds': int(item.find('torrent:seeds').text),
                    'leechers': int(item.find('torrent:peers').text),
                })
        except HTTPError as e:
            if e.code == 404:
                pass
            else:
                raise
        return torrents
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
class L337x(Search):
    def __init__(self):
        self.uri_prefix = 'http://1337x.to'
        self.search_uri = self.uri_prefix + '/sort-search/%s/seeders/desc/1/'
<<<<<<< HEAD

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
=======
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote_plus(terms)
        f = urlopen(url)
        soup = BeautifulStoneSoup(f.read())
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
        for details in soup.findAll('a', {'href': re.compile('^/torrent/')}):
            div = details.findNext('div')
            seeds = int(div.text)
            div = div.findNext('div')
            f_link = urlopen(self.uri_prefix + details['href'])
            soup_link = BeautifulStoneSoup(f_link.read())
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
<<<<<<< HEAD

# URL ?
class YTS(Search):
    def __init__(self):
        self.search_uri = 'http://yts.to/rss/%s/all/all/0'

=======
class YTS(Search):
    def __init__(self):
        self.search_uri = 'http://yts.to/rss/%s/all/all/0'
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote(terms, '')
        f = urlopen(url)
        soup = BeautifulStoneSoup(f.read())
        for item in soup.findAll('item'):
            item_quality = item.link.text.rpartition('_')[2]
            item_f = urlopen(item.link.text)
            item_soup = BeautifulStoneSoup(item_f.read())
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
<<<<<<< HEAD

class Lime(Search):
    def __init__(self):
        self.search_uri = 'https://www.limetorrents.cc/searchrss/%s/'

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote(terms)
        try :
             f = requests.get(url)
        except :
            raise Exception('something wrong')
        if (f.status_code != requests.codes.ok) :
            f.raise_for_status()
        soup = BeautifulStoneSoup(f.text)
=======
class Lime(Search):
    def __init__(self):
        self.search_uri = 'https://www.limetorrents.cc/searchrss/%s/'
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote(terms)
        f = urlopen(url)
        soup = BeautifulStoneSoup(f.read())
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
        for item in soup.findAll('item'):
            (seeds, leechers) = re.findall('Seeds: (\d+) , Leechers (\d+)', item.description.text)[0]
            torrents.append({
                'url': item.enclosure['url'],
                'name': item.title.text,
                'seeds': int(seeds),
                'leechers': int(leechers)
            })
        return torrents
<<<<<<< HEAD

class EZTV(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'https://eztv.ag/search/%s'
        self.headers = {'User-Agent': self.user_agent}

    def search(self, terms):
        torrents = []
        url = self.search_uri % quote(terms)
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
            link = self.search_uri % quote(info['href'])
            try :
                item_f = requests.get(link, headers=self.headers)
            except :
                raise Exception('something wrong')
            if (item_f.status_code != requests.codes.ok) :
                item_f.raise_for_status()
            item_soup = BeautifulStoneSoup(item_f.text)
=======
class EZTV(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.uri_prefix = 'https://eztv.ch'
        self.search_uri = self.uri_prefix + '/search/'
    def search(self, terms):
        torrents = []
        data = {'SearchString': '', 'SearchString1': terms, 'search': 'Search'}
        req = Request(self.search_uri, urlencode(data))
        req.add_header('User-Agent', self.user_agent)
        f = urlopen(req)
        soup = BeautifulStoneSoup(f.read())
        for (c, item) in enumerate(soup.findAll('a', {'class': 'magnet'})):
            if c == 30: break
            info = item.findPrevious('a')
            link = self.uri_prefix + info['href']
            item_req = Request(link)
            item_req.add_header('User-Agent', self.user_agent)
            item_f = urlopen(item_req)
            item_soup = BeautifulStoneSoup(item_f.read())
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
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

<<<<<<< HEAD
# Error 503
class CPasBien(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'http://www.cpasbien.io/recherche/%s.html,trie-seeds-d'

=======
class CPasBien(Search):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0'
        self.search_uri = 'http://www.cpasbien.pw/recherche/%s.html,trie-seeds-d'
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
    def search(self, terms):
        torrents = []
        url = self.search_uri % quote(terms)
        req = Request(url)
        req.add_header('User-Agent', self.user_agent)
        f = urlopen(req)
        if not f:
            raise Exception('Cloudfare bloque la connexion ?')
        else :
            soup = BeautifulStoneSoup(f.read())
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
        
<<<<<<< HEAD
# Error 500
class GetStrike(Search):
    def __init__(self):
        self.search_uri = 'https://getstrike.net/api/torrents/search/?q=%s'

=======
class GetStrike(Search):
    def __init__(self):
        self.search_uri = 'https://getstrike.net/api/torrents/search/?q=%s'
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
    def search(self, terms):
        torrents = []
        url = self.search_uri % '+'.join(terms.split(' '))
        hdr = {
                    'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
                    'Accept' : 'image/webp,*/*;q=0.8',
                    'Accept-Language' : 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
                    'Connection' : 'keep-alive'
                    }
        req = Request(url, headers=hdr)
        f = urlopen(req).read()
        rep = json.loads(f)
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
            torrents.append({"seeds":int(torrent['seeders']), "leechers":int(torrent['leechers']), "name":str(torrent['name']), "url":str(torrent['id'])})
        return torrents

if __name__ == '__main__':
<<<<<<< HEAD
    sites = [Mininova(), Kickass(), L337x(), Lime(), EZTV(), T411()]
    terms = 'avatar'
=======
    sites = [Mininova(), T411()]
    terms = 'mad max'
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
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
            print "seeds :" + str(torrent['seeds']) + " leechers: " + str(torrent['leechers']) + " name: " + str(torrent['name']) + " url: " + str(torrent['url'])
<<<<<<< HEAD
            if (counter == 3): 
=======
            if (counter == 10): 
>>>>>>> e1d0df718e1b2291b7bef41faeda1b790517d8a9
                break
