# Wbcsd scraper

- [Description](#description)
- [Getting started](#getting-started)

## Description
This project is a scraper of the website https://www.wbcsd.org.

The goal is to navigate the sections:
- https://www.wbcsd.org/Overview/News-Insights/Insider-perspective
- https://www.wbcsd.org/Overview/News-Insights/WBCSD-insights

to extract course information related to:
- title
- url
- image
- publication date
- tags

## Getting started

To get started place in the project folder and type:

```sh
make build  # to build all docker containers
```

Then, to start the scraper:
```sh
make up  # to run the containers

make tail  # to tail on the logs
```

To stop type:
```sh
make down
```
