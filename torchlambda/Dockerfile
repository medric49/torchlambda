FROM szymonmaszke/torchlambda:latest

RUN pip3 install --upgrade pip && \
  pip3 install opencv-python && \
  yum install -y g++ cmake make wget unzip git

RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip
RUN unzip opencv.zip
RUN yum update -y
RUN yum remove cmake -y
RUN pip3 install cmake
RUN mv opencv-master opencv && \
    mkdir -p build && cd build && \
    cmake ../opencv && \
    make -j4

RUN cd build && make install
RUN rm -r build
RUN echo "tdfest" && ls /usr/local/bin
ENTRYPOINT ["./build.sh"]
CMD []
