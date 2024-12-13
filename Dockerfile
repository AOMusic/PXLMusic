FROM nikolaik/python-nodejs:python3.10-nodejs19

RUN yum update && yum install -y ffmpeg
RUN yum update \
    && yum install -y --no-install-recommends ffmpeg \
    && yum clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD bash start
