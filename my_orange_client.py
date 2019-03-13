# -*- coding: utf-8 -*-
import getpass

import requests
from requests_oauthlib import OAuth1

# from bs4 import BeautifulSoup as bs
tokenFilename = 'token.txt'

token = ()


class Data_Amount:
    def __init__(self, amount=None):
        if type(amount) == str:
            if (' ' in amount):
                self.amount, self.units = amount.split()
                self.amount = float(self.amount)
            else:
                self.amount = float(amount)
                self.units = 'GB'
        elif type(amount) == float:
            self.amount = amount
            self.units = 'GB'
        # else:
        #     self.unit
        self.normalize()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self.amount:
            return '--' + ' ' + self.units
        else:
            # pity of me. for complience with computer world it should be dot not comma, but I like comma better!
            return str(self.amount).replace('.', ',') + ' ' + self.units

    def __eq__(self, incoming):
        if incoming is None:
            return True if self.amount is None else False
        return self.amount == incoming

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return self.amount

    def normalize(self):
        # normalize to GB
        normalize_factor = None
        units_caseless = self.units.lower()
        # not really considering kilo BITS here
        if units_caseless == 'kb':
            normalize_factor = 1000.0 ** 2
        elif units_caseless == 'kib':
            normalize_factor = 1024.0 ** 2
        elif units_caseless == 'mb':
            normalize_factor = 1000.0
        elif units_caseless == 'mib':
            normalize_factor = 1024.0
        elif units_caseless == 'gib':
            normalize_factor = 1.024
        elif units_caseless == 'gb':
            return

        self.amount /= normalize_factor
        self.units = 'GB'


class MyOrangeClient():
    OAUTH1_KEY = '53b7b45dc10f4ac8bd56d3ea912a7475'
    OAUTH1_SECRET = '0772c63e86fc4568a7ef2a17a794c418'
    OAUTH1_CB_URL = 'oob'

    client = {'client_key': '53b7b45dc10f4ac8bd56d3ea912a7475',
              # yeah, it is hardcoded. I got it by sniffing the mobile app
              'client_secret': '0772c63e86fc4568a7ef2a17a794c418',
              'callback_url': 'oob',  # ?? whatever it means'
              'id': None,
              'msisdn': None,  # client's mobile number. your login at the site https://www.orange.pl/zaloguj.phtml

              'MBamount': None,  # how much data plan
              'MBdueTo': ''  # and for how long. maybe it should be of datetime class ?
              }

    def __init__(self):
        self.dataAmount = None  # in GBs
        self.daysDue = None  # days left to use the data
        self.number = None
        self.id = None  # whatever it is

    def getGBamount(self):
        if not self.dataAmount:
            if not self.number or not self.id:
                self.refreshClient()
            serviceInfo = self.getInfoServices(token)
            if serviceInfo == True:
                pass
        # new data produced: dataAmount and dueDate
        return self.dataAmount

    def getDueToDays(self):  # due FOR should it be
        if not self.daysDue:
            if not self.number or not self.id:
                self.refreshClient()
            serviceInfo = self.getInfoServices(token)
            if serviceInfo == True:
                pass
        # new data produced: dataAmount and dueDate
        return self.daysDue

    def refreshClient(self):
        global token
        try:
            # try to authorize. if fails, then ask for new credientals
            token = self.handleToken()
        except IOError:
            if __name__ == '__main__':
                print('Brak pliku z tokenem. Zaloguj się')
                # import getpass
                print('(enter enter, aby pominąć, jeśli wiesz, że istnieje plik z tokenem)')
                username = input('Podaj login: ')
                password = input('Podaj haseło: ')
                # sanitize this user input
                token = self.handleToken(username, password)
                try:
                    token = self.handleToken(username, getpass.getpass('Hasło :'))
                    print(t)
                except PermissionError:
                    # now it means that credentials are wrong. exit
                    print('Złe dane logowania. Zamykam')
                    return False

        # here we have a working token
        # print("token jest i działa: " + token[0] + ', ' + token[1])
        if not self.number or not self.self.id:
            contractData = self.getContractData(token)
            if contractData[0] == True:
                self.number = contractData[1]['msisdn']
                self.id = contractData[1]['id']
                # ready to make call for MBs
            else:
                return False  # error
        return True

    # noinspection PySimplifyBooleanCheck,PySimplifyBooleanCheck,PySimplifyBooleanCheck
    def handleToken(self, username=None, password=None):
        """Tries to load long term token from file. If not found takes /username/ and /password/ and generates long term token and saves it in working folder.\nIf no credientials provided and no file is fount, then raises exception."""

        if (username is not None or password is not None) and (username is not '' and password is not ''):
            print('no to zgarniam nowy token')

            tempTokenResult = getNewToken(username, password)
            if tempTokenResult[0] == True:
                # obtained correct token
                token = tempTokenResult[1]
                try:
                    tokenFile = open(tokenFilename, 'w')
                    # tokenFile.write(token[0] + '\n' + token[1])
                    tokenFile.write('\n'.join(list(token)))
                    tokenFile.close()
                    return token
                except:
                    raise
                    # error writing token to file.
            else:
                print(tempTokenResult)
                raise PermissionError('Wrong credientals!')
                # exit(-1)  # no stored token found and getting new token failed
        else:
            try:
                tokenFile = open(tokenFilename, 'r')
                token = tuple([_ for _ in tokenFile.read().splitlines()])
                tokenFile.close()
                return token
            except FileNotFoundError:
                raise FileNotFoundError('Creating \"' + tokenFilename + '\"')
            except IOError:
                raise IOError('Provide either user credentials or file with token!')
                # uf there is no file, get them new tokens

    # noinspection PySimplifyBooleanCheck
    def getInfoServices(self, token):
        # xml:
        # <β:getNewInfoservicesAPIIn xmlns:β="api.orange.pl" xmlns=""><object><appVersion>3.4</appVersion><msisdn>572359832</msisdn></object><apiCode>mainPackageAPI</apiCode><apiCode>additionalPackageAPI</apiCode><withLimits>yes</withLimits><withSteps>yes</withSteps></β:getNewInfoservicesAPIIn>
        url = {'host': 'https://mapi.orange.pl',
               'path': '/api2/endpoint/services/ecare'}
        headers = {'Content-Type': 'text/xml',
                   'User-Agent': 'Windows tablet'}
        oauth = OAuth1(client_key=__class__.OAUTH1_KEY, client_secret=__class__.OAUTH1_SECRET,
                       resource_owner_key=token[0],
                       resource_owner_secret=token[1], signature_method='PLAINTEXT')
        payload = (
                '<β:getNewInfoservicesAPIIn xmlns:β="api.orange.pl" xmlns=""><object><appVersion>3.4</appVersion><msisdn>' + str(
            self.number) + '</msisdn></object><apiCode>mainPackageAPI</apiCode><apiCode>additionalPackageAPI</apiCode><withLimits>yes</withLimits><withSteps>yes</withSteps></β:getNewInfoservicesAPIIn>').encode(
            'utf-8')
        response = requests.post(url=url['host'] + url['path'], data=payload, headers=headers, auth=oauth)
        if response.status_code != 200:
            return (False,)
        from bs4 import BeautifulSoup
        xml = BeautifulSoup(response.content, 'html.parser')
        if xml.getnewinfoservicesapiout.result.errorcode.get_text() != '0':
            return (False,)
        else:
            packageValues = []
            # there are few <package>s, each contains 1 or more <values>'. in first package there is amount od Gigs, in third the date due. and there values are in <value>s
            # update: now there are ~6 packages, 2nd being important for us. in its 1st value it has date due, in 2nd value amount of GBs.
            for item in xml.getnewinfoservicesapiout.findAll('package'):
                packageValues.append(item.findAll(name='value', recursive=True))
            # 2  - intenet amount and date due

            try:
                self.dataAmount = Data_Amount(packageValues[1][1].get_text('value'))
                self.daysDue = packageValues[1][0].get_text('value').rsplit(maxsplit=2)[1]
                return (True)

            except IndexError as ie:
                print(ie.args)
                raise
                # exit(1)

        # noinspection PyRedundantParentheses,PyRedundantParentheses

    def getNotifications(self):
        # example GET https://mapi.orange.pl/api/endpoint/services/rest/notification?msisdn=572359xxx
        url = {'host': 'http://mapi.orange.pl',
               'path': '/api/endpoint/services/rest/notification'
               }
        headers = {'User-Agent': 'Windows tablet',
                   }
        response = requests.get(url['host'] + url['path'], headers)
        from json import loads
        jsonResponse = loads(response.text)
        if jsonResponse.get('error') == '0':
            if bool(jsonResponse.get('notification')):
                return (True, [_.get(_) for _ in jsonResponse.get('notification')])
            else:
                return (True, None)  # instead of [None,]
        else:
            return (False,)

        # noinspection PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses

    def getContractData(self, token):
        url = {'host': 'https://mapi.orange.pl',
               'path': '/api2/endpoint/services/ecare'}
        headers = {'Content-Type': 'text/xml',
                   'User - Agent': 'Windows tablet'}
        oauth = OAuth1(client_key=__class__.OAUTH1_KEY, client_secret=__class__.OAUTH1_SECRET,
                       resource_owner_key=token[0],
                       resource_owner_secret=token[1], signature_method='PLAINTEXT')
        payload = '<β:getContractDataAPIIn xmlns:β="api.orange.pl" xmlns=""><object><appVersion>3.4</appVersion></object></β:getContractDataAPIIn>'.encode(
            'utf-8')
        response = requests.post(url=url['host'] + url['path'], data=payload, headers=headers, auth=oauth)
        from bs4 import BeautifulSoup
        xml = BeautifulSoup(response.text, 'html.parser')  # , from_encoding='utf-8')

        try:
            if xml.getcontractdataapiout.result.errorcode.get_text() == '0':
                msisdn = xml.find('msisdn').get_text()
                customerId = xml.find('customerid').get_text()
                return (True, {'msisdn': msisdn, 'id': customerId})
            else:
                return (False,)
        except:
            return (False, response.text)

        # noinspection PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses

    def getNewToken(self, username, password):
        ### 1 - get temp credentials

        phase_1 = {'host': 'https://am.orange.pl',
                   'reqeust_token': '/opensso/resources/1/oauth/get_request_token',

                   }
        oauth = OAuth1(client_key=__class__.OAUTH1_KEY, client_secret=__class__.OAUTH1_SECRET1,
                       callback_uri=__class__.OAUTH1_CB_URL,
                       signature_method='PLAINTEXT')

        request_token_url = phase_1['host'] + phase_1['reqeust_token']

        response = requests.post(url=request_token_url, auth=oauth)
        if response.status_code != 201:
            return (False, response.status_code, 'Error initial authentication - bad initial credentials')
        from urllib.parse import parse_qs
        credentials = parse_qs(response.text)
        phase_1['oauth_token'] = credentials.get('oauth_token')[0]
        phase_1['oauth_token_secret'] = credentials.get('oauth_token_secret')[0]

        ### 2 - get verifier - authorize

        phase_2 = {'host': phase_1['host'],
                   'authorize': '/opensso/resources/1/oauth/RestUserAuthorization',
                   'oauth_token_AS': 'request_token',
                   'oauth_verifier': ''
                   }

        authorizeURL = phase_2['host'] + phase_2['authorize']

        response = requests.get(
            authorizeURL + '?username=' + username + '&password=' + password + '&' + phase_2['oauth_token_AS'] + '=' +
            phase_1['oauth_token'])

        if response.status_code != 200:
            from json import loads
            jsonResponse = loads(response.text)
            return (False, response.status_code, jsonResponse.get('error') if 'error' in jsonResponse else '',
                    "Error during second step of authentication - wrong login/password ?")
        phase_2['oauth_verifier'] = parse_qs(response.text).get('oauth_verifier')[0]
        if phase_1['oauth_token'] != parse_qs(response.text).get('oauth_token')[0]:
            return (False, response.status_code, 'error', 'Probably expired token - try again or something')

        ### 3 - get quasi permanent access token

        phase_3 = {'host': phase_1['host'],
                   'get_access_token': '/opensso/resources/1/oauth/get_access_token',
                   }
        oauth = OAuth1(client_key=__class__.OAUTH1_KEY, client_secret=__class__.OAUTH1_SECRET,
                       resource_owner_key=phase_1['oauth_token'],
                       resource_owner_secret=phase_1['oauth_token_secret'], verifier=phase_2['oauth_verifier'],
                       signature_method='PLAINTEXT')
        access_token_url = phase_3['host'] + phase_3['get_access_token']
        response = requests.post(url=access_token_url, auth=oauth)
        credentialsFinal = parse_qs(response.text)

        key = credentialsFinal.get('oauth_token')[0]
        secret = credentialsFinal.get('oauth_token_secret')[0]
        token = (key, secret)
        return (True, token)

        # noinspection PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses

    def setMsisdn(self, msisdn):
        try:
            sanitized = int(msisdn)
            if len(str(msisdn)) != 9:
                raise ValueError  # as well (as above)
        except ValueError:
            print('niepoprawna wartość MSISDN (numeru telefonu). Podaj 9 cyfr.')
        else:
            self.number = sanitized


def main():
    orange = MyOrangeClient()

    # verify that we have an access
    if not orange.refreshClient():
        exit(1)  # some error refreshing client data
    else:
        # let's fetch some notification of none value
        notifications = orange.getNotifications()
        if notifications[0] == True:
            print('---Brak nowych powiadomień' if notifications[1] is None else notifications)

        # and now the real thing: GBs and due date
        averageMBperDay = round(
            float(orange.getGBamount()) / float(orange.getDueToDays()) * 1024, 1)
        print('---Pozostało ' + str(
            orange.getGBamount()) + ' do wykorzystania przez ' + orange.getDueToDays() + ' dni. (średnio ' + str(
            averageMBperDay).replace('.', ',') + ' MB dziennie)')


if __name__ == '__main__':
    print('standalone mode')
    main()
else:
    # imported as module
    pass
