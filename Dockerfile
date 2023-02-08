FROM ubuntu

WORKDIR /app
COPY requirements.txt requirements.txt

# install google chrome
RUN apt update && apt install -y gnupg2
RUN apt install -y unzip xvfb libxi6 libgconf-2-4 
RUN apt install default-jdk -y
RUN apt install wget -y
RUN apt install curl -y

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
RUN bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
RUN apt -y update && apt install -y google-chrome-stable
RUN google-chrome --version

# install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install python3 and pip3
RUN apt update && apt install -y python3-pip

RUN pip3 install -r requirements.txt
COPY . .

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3", "-m", "flask", "run"]