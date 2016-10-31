# my-orange-client
So I made a small script to check your Orange account information. (Orange is a mobile phone operator)

I needed it to know how much internet I have left at my laptop (builtin 3G modem hooray!).
I'm not sure if it's legal, but I'd taken "Mój Orange" (polish version) Android app and reverse-engineered it.

To run it, simply run it. Main function will then take over and ask you to log in and will print some demo info about your account. Alternatively you can use batch script "my-orange-net-left.bat".

For Win users, there is also a accompanying Powershell script that shows a pop-up window. That script is called from another batch script "my-orange-net-left-window.bat" just to make it start minimalized.
By its looks though you can say I feel much better in CLI.

This small thing is confirmed (by glorious me) to work with polish Orange Free - a pre-paid internet service, but it should work in other countries too, provided API is the same..
Login via token works. They use OAuth1 lmao.
