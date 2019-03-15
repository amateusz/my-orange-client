# -*- coding: utf-8 -*-

# from bs4 import BeautifulSoup as bs
from my_orange_client import MyOrangeClient

tokenFilename = 'token.txt'

if __name__ == '__main__':

    print('standalone mode')
    # therefor do some stand alone'y things:
    orange = MyOrangeClient()

    '''
    If not found ~takes /username/ and /password/ and generates long term token and saves it in working folder.
    If neither credientials are provided and nor file is found, then it raises exception.
    '''

    try:
        # try to get a token from a /Token Wizard/
        # no credentials. better there be a token file
        try:
            token = orange.openTokenFromFile(tokenFilename)
        except FileNotFoundError:
            raise FileNotFoundError('Creating \"' + tokenFilename + '\"')
        except IOError:
            raise IOError('Provide either user credentials or file with token!')
            # if there is no file, get them new tokens
    except (IOError, FileNotFoundError):
        print('Brak pliku z tokenem. Zaloguj się')
        import getpass

        print('(enter enter, aby pominąć, jeśli wiesz, że istnieje plik z tokenem)')
        username = input('Podaj login: ')
        password = getpass.getpass('Podaj haseło: ')
        # sanitize this user input ? anyone ?
        try:
            token = orange.giveMeToken(username, password)
        except PermissionError:
            # now it means that credentials are wrong. exit
            print('Złe dane logowania. Zamykam')
            exit(1)
    # here we have a working token. supposedly. it might be outdated (expired)
    try:
        orange.saveTokenToFile(token, tokenFilename)
    except:
        raise
        # error writing token to file.

    try:
        # verify if the token works
        orange.authenticate(token)
    except ConnectionRefusedError:
        print('invalid token')
    else:  # let's fetch some notification of none value
        notifications = orange.getNotifications()
        if notifications[0] == True:
            print('---Brak nowych powiadomień' if notifications[1] is None else notifications)

        orange.refreshDetails(token)
        # and now the real thing: GBs and due date
        averageMBperDay = round(
            float(orange.getGBamount()) / orange.getDueToDays() * 1024, 1)
        print('---Pozostało ' + str(
            orange.getGBamount()) + ' do wykorzystania przez ' + str(
            orange.getDueToDays()) + ' dni. (średnio ' + str(
            averageMBperDay).replace('.', ',') + ' MB dziennie)')
else:
    # imported as module
    pass
