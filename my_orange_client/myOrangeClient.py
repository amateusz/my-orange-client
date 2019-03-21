import datetime

import requests
from requests_oauthlib import OAuth1

from my_orange_client.dataAmount import Data_Amount


class MyOrangeClient:
    friendly_name = 'Orange'
    friendly_color = 'orange'
    OAUTH1_KEY = '53b7b45dc10f4ac8bd56d3ea912a7475'
    # yeah, it is hardcoded. I got it by sniffing the mobile app
    OAUTH1_SECRET = '0772c63e86fc4568a7ef2a17a794c418'
    OAUTH1_CB_URL = 'oob'

    def __init__(self):
        self.dataAmount = None  # in GBs
        self.dueDate = None  # days left to use the data
        self.number = None
        self.id = None  # whatever it is

    def authenticate(self, token):
        '''
        Refreshes user data given a token.
        It there is none, it throws
        :return:
        '''

        # here we have a working token
        # print("token jest i działa: " + token[0] + ', ' + token[1])
        if not self.number or not self.id:
            contractData = self.getContractData(token)
            if contractData[0] == True:
                self.setMsisdn(contractData[1]['msisdn'])
                self.id = contractData[1]['id']
                # ready to make call for GIGABYTESs
            else:
                # error
                raise ConnectionRefusedError
        return True

    def giveMeToken(self, username, password):
        '''
        Tries to obtain a new token in exchange for credentials.
        If it doesn't work → Exception
        If there is not one → Exception
        '''
        if (username is not None or password is not None) and (username is not '' and password is not ''):
            print('no to zgarniam nowy token')

            # here it can fail. how ?
            tempTokenResult = self.__getNewToken(username, password)
            if tempTokenResult[0] == True:
                # obtained correct token
                token = tempTokenResult[1]
                return token

            else:
                print(tempTokenResult[2])
                raise PermissionError('Wrong credientals!')
                # no stored token found and getting new token failed
        else:
            raise AttributeError('')

    def refreshDetails(self, token):
        # old name: getInfoServices
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
            except IndexError as ie:
                print(ie.args)
                raise
                # exit(1)
            else:
                try:
                    daysLeft_str = packageValues[1][0].get_text('value').rsplit(maxsplit=2)[1]
                    if 'dziś' in daysLeft_str:
                        daysLeft = 0
                    else:
                        daysLeft = int(daysLeft_str)
                    daysLeft += 1  # because they return only the integer part, thus the last day is '0'. we will do better
                    self.dueDate = datetime.date.today() + datetime.timedelta(days=daysLeft)
                except ValueError as ie:
                    print(ie.args)
                    raise
                else:
                    return (True)

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

    # noinspection PySimplifyBooleanCheck
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

    def __getNewToken(self, username, password):
        ### 1 - get temp credentials

        phase_1 = {'host': 'https://am.orange.pl',
                   'reqeust_token': '/opensso/resources/1/oauth/get_request_token',

                   }
        oauth = OAuth1(client_key=__class__.OAUTH1_KEY, client_secret=__class__.OAUTH1_SECRET,
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

    def openTokenFromFile(self, location):
        tokenFile = open(location, 'r')
        token = tuple([_ for _ in tokenFile.read().splitlines()])
        tokenFile.close()
        return token

    def saveTokenToFile(self, token, location):
        tokenFile = open(location, 'w')
        # tokenFile.write(token[0] + '\n' + token[1])
        tokenFile.write('\n'.join(list(token)))
        tokenFile.close()

    def getDueToDays(self):  # due FOR should it be
        # if not self.dueDate:
        #     if not self.number or not self.id:
        #         self.authenticate(self.giveMeToken())
        #     serviceInfo = self.getInfoServices(token)
        #     if serviceInfo == True:
        #         pass
        # # new data produced: dataAmount and dueDate
        return (self.dueDate - datetime.date.today()).days

    def getGBamount(self):
        '''Returns the very essence of this utility module. As its internal data type is DataAmount, output of this function can be casted freely'''
        # if not self.dataAmount:
        #     if not self.number or not self.id:
        #         self.authenticate(self.giveMeToken())
        #     serviceInfo = self.getInfoServices(token)
        #     if serviceInfo == True:
        #         pass
        # # new data produced: dataAmount and dueDate
        return self.dataAmount
