@echo off
REM python -c "import my_orange_client as ora; t = ora.authorize(); s = ora.getInfoServices(t, ora.getContractData(t)[1]['msisdn'])[1]; print (float(s['MBamount'].replace(',','.').split()[0])); exit (0)"
python my-orange-print-internet-left.py
REM msg * %mess%