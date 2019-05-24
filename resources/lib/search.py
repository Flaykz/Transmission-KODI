#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import requests

try :
    from BeautifulSoup import BeautifulStoneSoup
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulStoneSoup
    from bs4 import BeautifulSoup
import cfscrape

socket.setdefaulttimeout(15)

class Search:
    def __init__(self):
        return NotImplemented
    def search(terms):
        return NotImplemented

class Torrent9(Search):
    def __init__(self):
        self.url = "https://www.torrent9.nz"
        self.urlTemp = ""
        self.path = "/search_torrent/"
        self.error = u"Aucun torrents disponibles correspondant à votre recherche :("
        self.initializeScraper()
        
    def initializeScraper(self):
        try:
            scraper = cfscrape.create_scraper(delay=5)
            self.tokens, self.userAgent = scraper.get_tokens(self.url)
            self.headers = {'User-Agent': self.userAgent}
        except:
            raise Exception('something wrong with cfscrape')
    def clean(self, strUnclean):
        search = strUnclean.replace("-", "")
        search = search.replace(" ", "-")
        search = search.replace("(", "")
        search = search.replace(")", "")
        search = search.replace("&", "")
        search = search.replace("'", "")
        search = search.replace("--", "-")
        return search
        
    def search(self, terms):
        torrents = []
        p = []
        if terms.find(' ') :
            p = terms.split(' ')
        else :
            p.append(terms)
        self.urlTemp = self.url
        if p[0] == "series" or p[0] == "films" :
            if p[0] == "series" :
                self.urlTemp += "/torrents_series.html"
            if p[0] == "films" :
                self.urlTemp += "/torrents_films.html"
            if len(p) > 1:
                self.urlTemp += ",page-" + str(int(int(p[1]) - 1))
        else :
            search = self.clean(terms)
            search = search + ".html"
            self.urlTemp += self.path + search
        try :
            f = requests.get(self.urlTemp, cookies=self.tokens, headers=self.headers)
        except:
            self.initializeScraper()
            try :
                f = requests.get(self.urlTemp, cookies=self.tokens, headers=self.headers)
            except:
                if (f.status_code != requests.codes.ok) :
                    f.raise_for_status()
                raise Exception('something wrong')
        response = f.text
        if self.error in response:
            # raise Exception("no torrent")
            return torrents
        else:
            soup = BeautifulSoup(response, 'html.parser')
            tds = soup.find_all("td")
            for td in tds:
                if td.i != None:
                    if "fa" in td.i.get("class") :
                        attributs = td.parent.find_all("td")
                        f2 = requests.get(td.a['href'], cookies=self.tokens, headers=self.headers)
                        soup = BeautifulSoup(f2.text, 'html.parser')
                        dl = soup.find_all('a', {'class': "btn btn-danger download"})
                        torrents.append({
                            'url': self.url + dl[1]['href'],
                            'name': td.a.text.encode('utf-8'),
                            'seeds': int(attributs[2].text),
                            'leechers': int(attributs[3].text),
                        })
        return torrents
        
if __name__ == '__main__':
    sites = [Torrent9()] 
    terms = 'étoile'
    if len(sys.argv) > 1:
        terms = sys.argv[1]
    print('Searching for "' + terms + '"')
    for site in sites:
        print(site.__class__.__name__.center(79, '='))
        torrents = site.search(terms)
        print('Total found = ' + str(len(torrents)))
        counter = 0
        for torrent in torrents:
            counter = counter + 1
            print(str(torrent))
            # print("seeds :" + str(torrent['seeds']) + " leechers: " + str(torrent['leechers']) + " name: " + torrent['name'] + " url: " + torrent['url'])
            if (counter == 3): 
                break
