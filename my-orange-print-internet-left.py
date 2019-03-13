# -*- coding: utf-8 -*-
import my_orange_client as orange

try:
    # try to authorize. if fails, then ask for new credientals
    t = orange.handleToken()
except IOError:
    print('Brak pliku z tokenem. Zaloguj się')
    import getpass

    u = input('Login: ')
    try:
        t = orange.handleToken(u, getpass.getpass('Hasło :'))
        print(t)
    except PermissionError:
        # now it means that credentials are wrong. exit
        print('Złe dane logowania. Zamykam')
        exit(-1)
contract = orange.getContractData(t)
if contract[0] is True:
    s = orange.getInfoServices(t, contract[1]['msisdn'])[1]
    print(s['MBamount'])
else:
    print('ERR: ' + contract[1])
