#!/bin/bash
pip3 install -U bird-browser
echo -e "#!/bin/bash\npython3 -m bird-browser" > /usr/local/bin/bird-browser
