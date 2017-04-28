FROM python

RUN apt-get update
RUN apt-get install -y git

RUN mkdir /src

RUN git clone https://github.com/memaldi/decision_engine /src

WORKDIR /src

RUN pip install -r requirements.txt

COPY settings.py.dist /src/decision_engine/settings.py

COPY entrypoint.sh entrypoint.sh

CMD ["./entrypoint.sh"]
