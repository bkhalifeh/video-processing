FROM ghcr.io/astral-sh/uv:0.7.2-python3.12-alpine

RUN apk update

RUN set -ex \
    && echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
    && echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk add -q --update --no-cache \
    build-base cmake \
    wget unzip \
    hdf5 hdf5-dev \
    protobuf protobuf-dev \
    openblas openblas-dev@community \
    libjpeg libjpeg-turbo-dev \
    libpng libpng-dev \
    tiff tiff-dev \
    libwebp libwebp-dev \
    openjpeg openjpeg-dev openjpeg-tools \
    libtbb@testing libtbb-dev@testing \
    eigen eigen-dev \
    tesseract-ocr tesseract-ocr-data-por tesseract-ocr-dev \
    py3-pip python3-dev \
    linux-headers \
    && pip install -q numpy \
    && wget -q https://github.com/opencv/opencv/archive/4.11.0.zip -O opencv.zip \
    && wget -q https://github.com/opencv/opencv_contrib/archive/4.11.0.zip -O opencv_contrib.zip \
    && unzip -qq opencv.zip -d /opt && rm -rf opencv.zip \
    && unzip -qq opencv_contrib.zip -d /opt && rm -rf opencv_contrib.zip \
    && cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-4.11.0/modules \
    -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D WITH_JPEG=ON \
    -D WITH_PNG=ON \
    -D WITH_TIFF=ON \
    -D WITH_WEBP=ON \
    -D WITH_JASPER=ON \
    -D WITH_EIGEN=ON \
    -D WITH_TBB=ON \
    -D WITH_LAPACK=ON \
    -D WITH_PROTOBUF=ON \
    -D WITH_V4L=OFF \
    -D WITH_GSTREAMER=OFF \
    -D WITH_GTK=OFF \
    -D WITH_QT=OFF \
    -D WITH_CUDA=OFF \
    -D WITH_VTK=OFF \
    -D WITH_OPENEXR=OFF \
    -D WITH_FFMPEG=OFF \
    -D WITH_OPENCL=OFF \
    -D WITH_OPENNI=OFF \
    -D WITH_XINE=OFF \
    -D WITH_GDAL=OFF \
    -D WITH_IPP=OFF \
    -D BUILD_OPENCV_PYTHON3=ON \
    -D BUILD_OPENCV_PYTHON2=OFF \
    -D BUILD_OPENCV_JAVA=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_IPP_IW=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_ANDROID_EXAMPLES=OFF \
    -D BUILD_DOCS=OFF \
    -D BUILD_ITT=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_TESTS=OFF \
    -D PYTHON3_EXECUTABLE=/usr/local/bin/python \
    -D PYTHON3_INCLUDE_DIR=/usr/local/include/python3.12/ \
    -D PYTHON3_LIBRARY=/usr/local/lib/libpython3.so \
    -D PYTHON_LIBRARY=/usr/local/lib/libpython3.so \
    -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.13/site-packages/ \
    /opt/opencv-4.11.0 \
    && make -j$(nproc) \
    && make install \
    && rm -rf /opt/build/* \
    && rm -rf /opt/opencv-4.11.0 \
    && rm -rf /opt/opencv_contrib-4.11.0



WORKDIR /video-processing


COPY pyproject.toml .
COPY uv.lock .

RUN uv venv
RUN uv sync


COPY . .
