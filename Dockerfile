FROM ubuntu:18.04

RUN apt update && apt install -y python3.6 curl python3-distutils

RUN mkdir ./zoomautouploader

COPY . ./zoomautouploader

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.6 get-pip.py
RUN pip install -r ./zoomautouploader/req.txt 

RUN chmod 777 -R /zoomautouploader

ENV PIAZZA_CLASS_NETWORK_ID=
ENV PIAZZA_PASSWORD=
ENV PIAZZA_EMAIL=

ENTRYPOINT [ "./zoomautouploader/entrypoint.sh" ]