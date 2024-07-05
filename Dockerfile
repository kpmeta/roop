FROM  python:3.9
WORKDIR /roop
COPY . .

# RUN apk add --update make automake gcc g++ subversion cmake
# RUN apt install pkg-config libhdf5-dev
RUN apt-get update 
RUN apt-get upgrade
RUN apt-get install libhdf5-dev ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip 
RUN pip install -r requirements-headless.txt 


ENTRYPOINT [ "tail", "-f", "/dev/null" ]


