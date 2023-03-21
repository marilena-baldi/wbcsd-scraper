FROM python:3.10 AS base

ARG PROJECT_PATH=/wbcsd-crawler
ENV PYTHONPATH=${PROJECT_PATH}

WORKDIR ${PYTHONPATH}

COPY ./src/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./src/ ./

CMD ["scrapy", "crawl", "wbcsd"]