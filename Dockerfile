FROM debian:stable 

## For chromedriver installation: curl/wget/libgconf/unzip
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
## For project usage: python3/python3-pip/chromium/xvfb
RUN apt-get update -y && apt-get install -y chromium xvfb python3 python3-pip 

# Download, unzip, and install chromedriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Create directory for project name (ensure it does not conflict with default debian /opt/ directories).
RUN mkdir -p /opt/twit-challenge
WORKDIR /opt/twit-challenge

## Your python project dependencies
## or install from dependencies.txt, comment above and uncomment below
COPY requirements.txt .
RUN pip3 install -r requirements.txt

## Copy over project/script
COPY src/ .

# Set display port and dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# Bash script to invoke xvfb, any preliminary commands, then invoke project
COPY ./run.sh /
# Setup appropriate perms
RUN chmod 755 /run.sh
# Run as an entry point so cmd line args can be used
# e.g. docker run twit-challenge:1.0 -U pccasegear
ENTRYPOINT [ "/run.sh" ]