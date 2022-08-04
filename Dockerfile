FROM ubuntu:latest as Builder
WORKDIR /work/build
RUN apt update &&\
    apt install -y gcc g++ wget tar sed python3 linux-headers-$(uname -r) make &&\
    mkdir -p /work/target
RUN wget "https://pan.skyone.host/api/v3/file/source/145/node-v16.16.0.tar.gz?sign=llsQcRqHEnrefyql9SKjfB6fOTbAb371h43lZ4S6gVE%3D%3A0" -O node-v16.16.0.tar.gz &&\
    tar -zxf node-v16.16.0.tar.gz &&\
    cd node-v16.16.0 &&\
    sed -i "s/'-static'/'-static', '-Wl,--whole-archive', '-lpthread', '-Wl,--no-whole-archive'/" configure.py &&\
    ./configure --fully-static --enable-static --prefix=/work/target &&\
    make && make install

FROM gcr.io/distroless/static-debian11
WORKDIR /app
COPY --from=Builder /work/target/bin/node /usr/bin/node
ENTRYPOINT ["/usr/bin/node"]
