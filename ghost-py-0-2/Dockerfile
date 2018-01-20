FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y git python3 python3-xvfbwrapper python3-pyqt5 python3-pyqt5.qtwebkit \
    && git clone -b ghost-py-0-2 https://github.com/jeanphix/Ghost.py \
    #&& apt-get install -y --force-yes xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic fonts-monapo --no-install-recommends \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
WORKDIR /Ghost.py
ADD . .
RUN cat ghost-py-0-2.patch | patch -p1
