# Bird Browser
The Bird Browser is a browser written in Python and Qt.
The browser.ui file can be loaded in the qt-designer.
This is how I want the browser to look at some point.
Planed features are:
- [x] tabs
- [x] search engine integration
- [x] source-code view
- [x] password manager integration
- [x] bookmarks
- [x] configuration
- [ ] extensions

Some of these features weren't done by me before.
This Project also has an Adblocker build into it.
## Installation
Finished versions can be found on pip: `pip install bird-browser`
earlier versions can be installed like this: `pip install -i https://test.pypi.org/simple/ bird-browser`.
Maybe you need to install the birdlib separatly: `pip install -i https://test.pypi.org/simple/ birdlib`.
To run an installation via pip use: `python -m bird-browser`. See the wiki for more information.
## Wiki
The wiki/manual/cheatsheet can be found [here](https://github.com/ULUdev/bird-browser/wiki).
It contains more information on how to use the browser and how to install it.
In the future there may be dev information
## License
**GNU GPL 3**. For more information see the LICENSE file
## CI
[![pipeline status](https://gitlab.sokoll.com/moritz/browser/badges/master/pipeline.svg)](https://gitlab.sokoll.com/moritz/browser/-/commits/master)
successfully built AppImages can be found in the job Artifacts on Gitlab
