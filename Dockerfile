FROM python:3.10-slim

FROM scrapinghub/scrapinghub-stack-scrapy:2.1
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install zip unzip

ARG CHROME_VERSION="google-chrome-stable"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN wget --no-verbose -O /tmp/LATEST_RELEASE "https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip" \
  && CD_VERSION=$(cat "/tmp/LATEST_RELEASE") \
  && rm /tmp/LATEST_RELEASE \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-temp \
  && chmod 755 /opt/selenium/chromedriver-temp \
  && sudo ln -fs /opt/selenium/chromedriver-temp /usr/bin/chromedriver

ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE cVehicles.settings

RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["uvicorn", "main:app", "--workers=4", "--host=0.0.0.0", "--port=8080"]
