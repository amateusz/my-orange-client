# -*- coding: utf-8 -*-
from my_orange_client import MyOrangeClient as Orange

try:
    # try to authorize. if fails, then ask for new credientals
    orange = Orange()
    t = orange.giveMeToken()
except IOError:
    print('Brak pliku z tokenem. Zaloguj się')
    import getpass

    u = input('Login: ')
    try:
        t = orange.giveMeToken(u, getpass.getpass('Hasło :'))
        print(t)
    except PermissionError:
        # now it means that credentials are wrong. exit
        print('Złe dane logowania. Zamykam')
        exit(-1)
else:
    print(orange.getGBamount())
