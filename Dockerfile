FROM python:3.6

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install selenium
RUN pip install selenium

# install dev dependencies
RUN pip3 install mysql-connector-python
RUN pip3 install selenium
RUN pip3 install redis
RUN pip3 install pytest
RUN pip3 install pillow
RUN pip3 install argon2-cffi
RUN pip3 install pytest
RUN pip install screeninfo

# install Macro dependencies
RUN pip3 install cefpython3
RUN apt-get -f install
RUN apt-get install -y aptitude
RUN aptitude install -y libgtk2.0-dev
RUN pip3 install pynput

#RUN touch ~/.Xauthority
RUN pip3 install pyautogui

RUN apt-get install -y scrot
RUN pip3 install opencv-python

RUN pip3 install python-dateutil
RUN pip3 install pytz
RUN pip3 install tzlocal

#Google calendar API
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# copy files
COPY .  littlelearners/

# Set working directory
WORKDIR littlelearners/desktopApp/

#Change runUnix.sh to unix style ling endings
RUN python3 ../ShellStuff/changeLineEndings.py

#RUN rm ~/.Xauthority
#RUN apt-get install -y xauth
#RUN xauth add 192.168.40.1:0 . 00000000000000000000000000000000
COPY .Xauthority ../../root/.Xauthority

RUN apt-get install -y kmod

#Runs shell script to change .cnf file depending on parameters passed to CMD.
#No parameter leaves .cnf as is
#Everything else changes host to mysql
#Parameter -    'local' runs littlelearners with local database connection
#               'test' runs pytest with directory ../   (Additional parameters are passed to pytest)
#               'db' runs littlelearners/database/database.py
ENTRYPOINT ["/bin/bash", "../ShellStuff/runUnix.sh"]
CMD [""]