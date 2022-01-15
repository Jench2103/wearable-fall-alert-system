FROM python:3.8

ARG TZ=Asia/Taipei

WORKDIR /workspace

COPY . /workspace/

RUN mkdir data

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -r /workspace/requirements.txt

CMD [ "python", "main.py" ]
