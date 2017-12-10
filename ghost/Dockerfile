FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install software-properties-common python3-pip -y \
    && add-apt-repository ppa:thopiekar/pyside-git -y \
    && apt-get update \
    && apt-get install python3-pyside2 xvfb --no-install-recommends -y \
    && apt-get install -y --force-yes xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic fonts-monapo --no-install-recommends \
    && pip3 install xvfbwrapper \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
WORKDIR /ghost
ADD . .
