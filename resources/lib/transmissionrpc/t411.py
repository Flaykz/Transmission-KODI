# -*- coding: UTF-8 -*-
import getpass
import json
import requests
import os
import base64

HTTP_OK = 200
API_URL = 'https://api.t411.in/%s'
USER_FILE = 'user.json'
CID_FILM_VIDEO = "210"

class T411Exception(BaseException):
    pass

class T411(object):
    """ Base class for t411 interface """

    def __init__(self, username = None, password = None) :
        """ Get user credentials and authentificate it, if any credentials
        defined use token stored in user file
        """
        #user = raw_input('Please enter username: ')
        #password = getpass.getpass('Please enter password: ')        
        #self._auth(user, password)
        try :
            with open(USER_FILE) as user_file:
                self.user_credentials = json.loads(user_file.read())
                if 'uid' not in self.user_credentials or 'token' not in \
                        self.user_credentials:
                    raise T411Exception('Wrong data found in user file')
                #else:
                    # we have to ask the user for its credentials and get
                    # the token from the API
                    #user = raw_input('Please enter username: ')
                    #password = getpass.getpass('Please enter password: ')
                    #self._auth(user, password)
        except IOError as e:
            # we have to ask the user for its credentials and get
            # the token from the API
            while True :
            	user = raw_input('Please enter username: ')
            	password = getpass.getpass('Please enter password: ')
            	try :
                	self._auth(user, password)
            	except T411Exception as e:
                	raise T411Exception(e.message)
            	else :
                	break
        except T411Exception as e:
            raise T411Exception(e.message)
        except Exception as e:
            raise T411Exception('Error while reading user credentials: %s.'\
                    % e.message)

    def _auth(self, username, password) :
        """ Authentificate user and store token """
        self.user_credentials = self.call('auth', {'username': username, 'password': password})
        if 'error' in self.user_credentials:
            raise T411Exception('Error while fetching authentication token: %s'\
                    % self.user_credentials['error'])
        # Create or update user file
        user_data = json.dumps({'uid': '%s' % self.user_credentials['uid'], 'token': '%s' % self.user_credentials['token']})
        with open(USER_FILE, 'w') as user_file:
            user_file.write(user_data)
        return True

    def call(self, method = '', params = None) :
        """ Call T411 API """

        #call_params = {'url': API_URL % method, 'params': params}
        if method == 'auth' :
            req = requests.post(API_URL % method, data=params)
        elif 'search' in method :
            req = requests.post(API_URL % method, params=params, headers={'Authorization':self.user_credentials['token']})
            print req.url # Pour debug
            if req.status_code == requests.codes.OK:
                data = req.json()
                print data
                data['torrents'].sort(key=lambda k: int(k['seeders']), reverse=True)
                return data
            else :
                raise T411Exception('Error while sending %s request: HTTP %s' % (method, req.status_code))
        elif 'download' in method :
            torrentid = os.path.basename(method)
            req = requests.get(API_URL % method, headers={'Authorization':self.user_credentials['token']})
            if req.status_code == requests.codes.OK :
                torrent_data = ''
                for block in req.iter_content(1024) :
                    if not block :
                        break
                    torrent_data += block
                return base64.b64encode(torrent_data).decode('utf-8')
        else :
            req = requests.post(API_URL % method, data=params, headers={'Authorization':self.user_credentials['token']})

        if req.status_code == requests.codes.OK :
            return req.json()
        else :
            raise T411Exception('Error while sending %s request: HTTP %s' % (method, req.status_code))

    def me(self) :
        """ Get personal informations """
        return self.call('users/profile/%s' % self.user_credentials['uid'])

    def user(self, user_id) :
        """ Get user informations """
        return self.call('users/profile/%s' % user_id)

    def categories(self) :
        """ Get categories """
        return self.call('categories/tree')

    def terms(self) :
        """ Get terms """
        return self.call('terms/tree')

    def details(self, torrent_id) :
        """ Get torrent details """
        return self.call('torrents/details/%s' % torrent_id)

    def download(self, torrent_id) :
        """ Download a torrent """
        return self.call('torrents/download/%s' % torrent_id)

    def search(self, query, limit=50) :
        """ Search a torrent """
        payload = {"limit": limit, "cid": CID_FILM_VIDEO}
        return self.call('torrents/search/%s' % query, payload)

    def top100(self) :
        return self.call('torrents/top/100')

    def topToday(self) :
        return self.call('torrents/top/today')

    def topWeek(self) :
        return self.call('torrents/top/week')

    def topMonth(self) :
        return self.call('torrents/top/month')

    def get_bookmarks(self) :
        return self.call('bookmarks')

    def add_bookmark(self, torrent_id) :
        """ Get bookmarks of user """
        return self.call('bookmarks/save/%s' % torrent_id)
         
    def delete_bookmark(self, torrent_id) :
        """ Delete a bookmark """
        return self.call('bookmarks/delete/%s' % torrent_id)

    def print_term_cat(self) :
        # On vient chercher les parametres de recherches personnalisées
        # CID = Catégorie (Audio - eBook - Emulation - Jeu vidéo - GPS - Application - Film/Vidéo)
        # CAT = Sous Catégorie (Film/Vidéo : Animation - Concert - Documentaire - Emission TV - Film - Série TV - Spectacle)
        # term* = tag (Film/Série - Langue : Anglais - VOSTFR - Multi (Français inclus) - Français (VFF/Truefrench)
        # term* = tag (Film/Série - Type : 2D (Standard) - 3D Converti (Post-Production) - 3D Natif (Production)
        # term* = tag (Série TV - Episode : Saison complète - Episode XX)
        # term* = tag (Série TV - Saison : Série intégrale - Saison XX)
        req_cat = self.categories()
        req_term = self.terms()
        cat = []
        term = []
        def searchkeycat(dic, id) :
            for key, value in dic.iteritems() :
                if isinstance(value, dict):
                    searchkeycat(value, key)
                else :
                    if (key.encode('utf-8') == "name" and value.encode('utf-8') == "Film") :
                        cat.append({value.encode('utf-8'): str(id)})
                    if (key.encode('utf-8') == "name" and  value.encode('utf-8') == "Série TV") :
                        cat.append({value.encode('utf-8'): str(id)})
                    if (key.encode('utf-8') == "name" and value.encode('utf-8') == "Film/Vidéo") :
                        cat.append({value.encode('utf-8'): str(id)})
        def searchkeyterm(dic, id) :
            for key, value in dic.iteritems() :
                if isinstance(value, dict):
                    if 'type' in value :
                        searchkeyterm(value, str(id) + " - " + value['type'].encode('utf-8') + "(" + str(key) + ")")
                    else :
                        searchkeyterm(value, str(id) + " - " + str(key))
                else :
                    tmp = str(id) + " - " + str(key)
                    if (value.encode('utf-8') == "Anglais") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "VOSTFR") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "Français (VFF/Truefrench)") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "Multi (Français inclus)") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "2D (Standard)") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "3D Converti (Post-Production)") :
                        term.append({value.encode('utf-8'): tmp})
                    if (value.encode('utf-8') == "3D Natif (Production)") :
                        term.append({value.encode('utf-8'): tmp})
        searchkeycat(req_cat, "0")
        cat.sort()
        for i in cat :
            print i
        searchkeyterm(req_term, "0")        
        term.sort()
        for i in term :
            print i

if __name__ == "__main__" :
    t411 = T411() 
    t411.print_term_cat()
