#install pip
sudo apt-get install python3-pip
#install virtualenv
pip3 install virtualenv
#upgrade pip
pip3 install --upgrade pip
#create virtual
virtualenv env
#start virtual
source env/bin/activate

#install Flask
pip3 install Flask

#install pillow
#pip3 install PIL
pip3 install Pillow
#pip3 install scipy==1.1.0

#skimage install
pip3 install scikit-image

#scikit-learn install
pip3 install -U scikit-learn
pip3 install sklearn

#ppp
#pip3 install opencv
#pip3 install opencv-contrib-python
pip3 install opencv-python #==3.4.2.16
pip3 install opencv-contrib-python #==3.4.2.16
#run program
python3 src/app.py

#exit
deactivate
