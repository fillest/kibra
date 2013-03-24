sudo apt-get install python-dev libpq-dev python-setuptools
sudo easy_install pip
pip install virtualenv
mkdir venvs
virtualenv --no-site-packages venvs/kibra
source venvs/kibra/bin/activate
...
cd kibra
pip install -e .
paster serve --reload dev.ini
...
sudo add-apt-repository ppa:ferramroberto/java
sudo apt-get update
sudo apt-get install sun-java6-jre sun-java6-plugin yui-compressor mercurial
...
