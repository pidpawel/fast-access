Fast-access v0.2
===========
This a simple app to help us accesing web search engines or doing other simple tasks.
All you have to do is to type `phrase` and press enter.
It will open your favourite search engine in your favourite browser and fill it in with your phrase.
You can also easily change the search engine by typing something like `wiki phrase` in search field.

For example:

	google test
	wikien ascii
	bingimages home

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
Then simply run `fast-access.py` and fill the search line with your phrase.

It's a good idea to bind it to a certain key. Like Alt + F3

TODO
----
* plugin `run` may use `/usr/share/applications` instead of strange library
* ↑ and ↓ support
* tray
* <tab>completion
* plugin aliases (Is it really important? Ya. It is.)
* html methods
* gui for raw, text, html plugins
* add some plugins
* plugins/libs translations
* try to make `make install`
* write plugin writing howto

Features
--------
* Configuration file support
* Various browser support (via configuration file)
* Various search engines support (via configuration file)
* Plugins system
* Plugins blacklisting
* Spell checker
* Gnome-idependent
* Some other, hidden features (One can call it bug, but I don't care.)

License and author info
-----------------------
Creative Commons BY-NC-SA

[http://creativecommons.org/licenses/by-nc-sa/2.5/pl/](http://creativecommons.org/licenses/by-nc-sa/2.5/pl/)

Created by PidPawel


