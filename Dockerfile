FROM runmymind/docker-android-sdk:alpine-standalone

# copy project
COPY ./src /opt/workdir

# working directory
WORKDIR /opt/workdir

RUN apk -U add python3 py3-pip && \
 echo "vt_api_key: 'bb5971683abe6920615599adbb4db2cf7ffcf94ebdf8262c360ea5577b9508a2'" > /opt/workdir/assets/config.yaml && \
 echo "sdk: '/opt/android-sdk-linux'" >> /opt/workdir/assets/config.yaml && \
 cd /opt/workdir && bash /opt/workdir/setup.sh

CMD bash ./server.sh