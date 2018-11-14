# my-orange-client
So I made a small script to check My Orange account information. (Orange is a mobile phone operator here in Poland)

I needed it to know how much internet I have left at my laptop (builtin 3G modem hooray!).
**_I'm not sure if it's legal_**, but I'd taken "Mój Orange" (polish version) Android app and reverse-engineered it by sniffing packets with circumvented cert.

To run it, simply run it. Main function will then take over and ask you to log in and will print some demo info about your account. Alternatively you can use batch script "my-orange-net-left.bat", which calls the script and returns just the MBs left.

For Win users, there is also a accompanying Powershell script that shows a pop-up window. That script is called from another batch script "my-orange-net-left-window.bat" just to make it start minimazed.
Although it is GUI, its look reveals that you can say I feel much better in CLI though.

This small utility is confirmed (by glorious myself) to work with polish Orange Free - a pre-paid internet service - but it should work in other countries too, provided API is the same..
Login via token works. They use OAuth1 lmao.


## Update USAGE:

- Importing
```
> import my_orange_client
> my_orange_client.getMBamount()
99
> my_orange_client.getDueToDays()
127
```

- Running as a program

```
$ python3 my_orange_client.py 
standalone mode
---Brak nowych powiadomień
---Pozostało 99,39 GB do wykorzystania przez 127 dni. (średnio 801,4 MB dziennie)
```

Upon first exectuion it will either complain about lack of token file or will ask you to log in.
