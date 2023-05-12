# syntax=docker/dockerfile:1.4
FROM python:3.10 AS builder

COPY requirements.txt .

RUN pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt

RUN pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple torch --index-url https://download.pytorch.org/whl/cpu

COPY ./core/embedding.py ./embedding.py

RUN python3 ./embedding.py

FROM builder as py-envs

WORKDIR /application

COPY . .

EXPOSE 5598

CMD ["flask", "--app", "./web_app/app.py:app", "run", "-h", "0.0.0.0", "-p", "5598"]