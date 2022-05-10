sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get -y update
sudo apt install -y python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
python3 --version
