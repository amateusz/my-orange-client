# -*- coding: utf-8 -*-
import my_orange_client as ora

try:
    # try to authorize. if fails, then ask for new credientals
    t = ora.authorize()
except IOError:
    print('Brak pliku z tokenem. Zaloguj się')
    import getpass

    u = input('Login: ')
    try:
        t = ora.authorize(u, getpass.getpass('Hasło :'))
        print(t)
    except PermissionError:
        # now it means that credentials are wrong. exit
        print('Złe dane logowania. Zamykam')
        exit(-1)
contract = ora.getContractData(t)
if contract[0] is True:
    s = ora.getInfoServices(t, contract[1]['msisdn'])[1]
    print(s['MBamount'])
else:
    print('ERR: ' + contract[1])
