FROM ubuntu:xenial
ENV PATH=/usr/local/bin:${PATH}
ARG BF_HOME=/usr/local/barrelfish

RUN apt-get update -yqq
RUN buildDeps=' \
        bison \
        build-essential \
        cabal-install \
        cmake \
        cpio \
        curl \
        flex \
        freebsd-glue \
        g++-aarch64-linux-gnu \
        g++-arm-linux-gnueabi \
        gcc-aarch64-linux-gnu \
        gcc-arm-linux-gnueabi \
        ghc \
        git \
        libelf-freebsd-dev \
        libghc-async-dev \
        libghc-ghc-mtl-dev \ 
        libghc-ghc-paths-dev \
        libghc-parsec3-dev \
        libghc-random-dev \
        libghc-src-exts-dev \
        libghc-src-exts-dev \
        libgmp3-dev \
        libusb-1.0-0-dev \
        python-pip \
        qemu-system-arm \
        qemu-system-x86 \
        qemu-utils \
    ' \
    && apt-get install -yqq --no-install-recommends $buildDeps

RUN cabal update && cabal install bytestring-trie
RUN pip install --upgrade pip && pip install gitpython pexpect

COPY ./src ${BF_HOME}
WORKDIR ${BF_HOME}
RUN mkdir -pv results
RUN mkdir -pv build && cd build && ../hake/hake.sh -s .. -a x86_64 -a armv7
RUN cd build && make -j5 X86_64_Basic && make -j5 PandaboardES
CMD ./tools/harness/runtests.py
