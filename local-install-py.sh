#!/bin/bash
python -m venv ~/bin/venv
source ~/bin/venv/bin/activate
pip install -U bird-browser
echo -e "#!/bin/bash\nsource ~/bin/venv/bin/activate\npython -m bird-browser\ndeactivate" > ~/bin/bird-browser
curl https://raw.githubusercontent.com/ULUdev/bird-browser/master/bird-browser/browser.ui > ~/.config/bird/browser.ui
echo done!
deactivate
