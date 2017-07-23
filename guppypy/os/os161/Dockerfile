FROM ubuntu:trusty
ENV PATH=/usr/local/bin:${PATH}
ARG OS_HOME=/os-src
ARG BUILD_HOME=/os-build
RUN locale-gen en_US.UTF-8

# install toolchain
RUN deps= apt-get update -yqq \
    && apt-get install -yqq software-properties-common gcc \
    && add-apt-repository ppa:cs161/sp2017 \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends os161-toolchain

# add the source code
COPY ./src ${OS_HOME}

# configure and compile
WORKDIR ${OS_HOME}
RUN ./configure --ostree=${BUILD_HOME}
RUN bmake && bmake install
RUN cd kern/conf && ./config ASST1
RUN cd kern/compile/ASST1 && bmake && bmake install
COPY ./sys161.conf ${BUILD_HOME}/sys161.conf
RUN apt-get install python-pexpect

WORKDIR ${BUILD_HOME}
CMD python testscripts/test.py 'tt1'
