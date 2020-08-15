FROM ubuntu
RUN apt update
RUN apt install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.7
RUN pip install --upgrade pip

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

#RUN python -m

EXPOSE 4000

ENTRYPOINT ['python3']

CMD ['app.py '] 
