# Wbcsd scraper

- [Description](#description)
- [Getting started](#getting-started)
- [Tools](#tools)
- [Process](#process)

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

Once the scraper is done, you can visit http://localhost:8889/ to access the database table with
the extracted data.

To stop type:
```sh
make down
```

To run the tests:
```sh
make test
```

## Tools
The web scraping framework used is Scrapy, considered more suitable than others such as Selenium or BeautifulSoup (respectively more useful when you need to interact with web pages by simulating the browser and for static web pages).

Some files have been prepared to automate the deployment process: the Dockerfile to define the software image, the docker-compose to orchestrate the containers and the Makefile to simplify their launch.

For tests development some solutions have been evaluated, such as scrapy-test, scrapy-testmaster and scrapy-autounit. Autounit was used because it automatically generates the unit tests for the spiders.

## Process
About the crawling strategy, considering the objective of extracting information from the two specific sections, an attempt was made to identify common elements that would allow to set up a single spider.

### **Pagination**
Having observed that the main difference lies in the pagination, it was decided to use the same approach by parameterizing the “next” button selector of the pages. The spider was created for the first section (https://www.wbcsd.org/Overview/ News-Insights/Insider-perspective). Completed and verified the functioning of the first section, an attempt was made to generalize the approach to the second one (https://www.wbcsd.org/Overview/News-Insights/WBCSD-insights), but due to the call with AJAX it was not possible to use the next page button as in the first case.

At this point it was noticed that from the second section it was possible to obtain a URL with pagination, as in the first section, even if the functionality had not been exploited. So it was decided to change the initial parsing and base it on the URLs that contained the page number, in order to generalize the approach.

To determine the stop condition in the iteration on the pages, a preliminary phase to extract the number of pages of each section was performed. This data was used to iterate over the pages.

### **Spider**
At this point, the spider started from the base URLs of the two sections, also storing the corresponding versions of the paginated URLs. Next, he crawled through the main pages of the sections to extract the total number of pages and get the URLs of the individual pages. For each page, he extracted the URLs of the courses to visit them. Finally, from the pages of the individual courses, he extracted the required fields.

### **Data validation and data storage pipelines**
About data validation, a pipeline has been set up to check the integrity of the extracted data. Since in this case no particular validation operations were necessary for the objective to be achieved, the title and tag strings have been stripped and the publication dates have been formatted.

For the storage part, an elementary database memorization has been prepared. While considering DBMSs such as PostgreSQL (relational and with advanced features for the  management of json data), MySQL (relational and performing) and MongoDB (non-relational and suitable for unstructured data management), it was decided to use MySQL, setting up a pipeline that handles the connection to the database and saves the objects extracted by the scraper in a single table, "courses", with the fields mapping those of the items.

Although design and implementation of the storage part has not continued, some areas for improvement have been identified:

- the course tags could be stored in a second table, making full use of the relational capabilities of the database and with the aim of using them for a wider tags management system (potentially also tags coming from different websites, with the possibility of being remapped);

- the communication with the database would be safer and more functional if it were done through an ORM, for example using the SQLAlchemy toolkit, instead of raw queries;

- the primary key of the courses table could be more complex than the simple URL of the course, currently used assuming it remains the same even in case of changes to the post of the course web page.

Considering the case of a possible interruption of data extraction due to errors, but also considering that typically there is a need to relaunch the scrapers over time, it was decided to save the data on the database by updating them if they already exist, so if the primary key already exists.