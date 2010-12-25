Fast-access v0.2
===========
This a simple app to help us accesing web search engines or doing other simple tasks.
All you have to do is to type `phrase` and press enter.
It will open your favourite search engine in your favourite browser and fill it in with your phrase.
You can also easily change the search engine by typing something like `wiki phrase` in search field.

For example:

`google test
wikien ascii
bingimages home`

List of available search engines is configurable by the config file, just like the browser or wmctrl
(the thing which allows this software to change active window).

That's all. Have fun.

Requirements
------------
Firefox - or other browser, configurable in config file

wmctrl - to switch between desktops

Usage
-----
Copy `example.cfg` file into `~/fast-access.cfg`, read and change it to fit your purposes.
Than simply run `fast-access.py` and fill the search line with your phrase.

It's a good idea to bind it to a certain key. Like Alt + F3

TODO
----
* try to make `make install`
* add some plugins
* write plugin writing howto
* plugin aliases (is it really important?)
* html, irc methods
* gui for raw, text, html plugins

Features
--------
* configuration file support
* various browser support (via configuration file)
* various search engines support (via configuration file)
* plugins system
* plugins blacklisting
* spell checker
* some other, hidden features (one can call it bug, but I don't care)

License and author info
-----------------------
Creative Commons BY-NC-SA

[http://creativecommons.org/licenses/by-nc-sa/2.5/pl/](http://creativecommons.org/licenses/by-nc-sa/2.5/pl/)

Created by PidPawel


