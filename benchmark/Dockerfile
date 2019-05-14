FROM ubuntu:18.04

# Software from trusty repositories
RUN apt-get update -qq &&   \
    apt-get install -y      \
            build-essential \
            git             \
            zlib1g-dev      \
            wget            \
            python3         \
            python3-pip     \
	    make

# bwa
RUN cd / && \
    git clone https://github.com/lh3/bwa && \
    cd bwa && \
    make && \
    cp bwa /usr/local/bin

# smmfdp
RUN cd / && \
    git clone https://github.com/gui11aume/smmfdp && \
    cd smmfdp && \
    make && \
    cp smmfdp /usr/local/bin
