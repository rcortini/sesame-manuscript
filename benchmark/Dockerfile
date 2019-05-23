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

# bowtie2
RUN apt-get install unzip && \
    wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.3.5.1/bowtie2-2.3.5.1-sra-linux-x86_64.zip && \
    unzip bowtie2-2.3.5.1-sra-linux-x86_64.zip && \
    cp bowtie2-2.3.5.1-sra-linux-x86_64/bowtie2* /usr/local/bin
