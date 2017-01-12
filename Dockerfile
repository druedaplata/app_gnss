# Copied from Caffe Docker, modified for SegNet and App-Gnss

FROM ubuntu:16.04
MAINTAINER Diego Rueda <ing.diegorueda@gmail.com>

EXPOSE 5000

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	cmake \
	curl \
	git \
	wget \
	libatlas-base-dev \
	libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
	nano \
        protobuf-compiler \
        python-dev \
	python-opencv \
        python-numpy \
        python-pip \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*

ENV CAFFE_ROOT=/opt/caffe-segnet
WORKDIR /opt/caffe-segnet
RUN pip install --upgrade pip

RUN git clone https://github.com/alexgkendall/caffe-segnet.git . && \
	for req in $(cat python/requirements.txt) pydot; do pip install $req; done && \
	mkdir build && cd build && \
	cmake -DCPU_ONLY=1 .. && \
	make -j"$(nproc)"  && \
	make pycaffe

ENV PYCAFFE_ROOT $CAFFE_ROOT/Python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

WORKDIR /workspace

# From here, we install our app

RUN git clone https://github.com/sandiego206/app_gnss.git

WORKDIR /workspace/app_gnss
RUN git pull
RUN wget http://mi.eng.cam.ac.uk/%7Eagk34/resources/SegNet/segnet_weights_driving_webdemo.caffemodel -P static/nn_files
RUN for req in $(cat requirements.txt); do pip install $req; done

