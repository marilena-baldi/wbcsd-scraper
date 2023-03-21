""" Scrapy pipelines """

import json
from itemadapter import ItemAdapter
import dateparser
import mysql.connector


class ValidationPipeline:
    """ The ValidationPipeline processes the scraped items validating its fields """

    def process_item(self, item, spider): # pylint: disable=unused-argument
        """ Validate the items stripping the string fields and setting them to None if they are
            missing """

        adapter = ItemAdapter(item)

        adapter['title'] = adapter['title'].strip() if adapter['title'] else None
        adapter['publication_date'] = dateparser.parse(
                                        adapter['publication_date']
                        ).strftime('%Y-%m-%d') if adapter['publication_date'] else None
        adapter['tags'] = [tag.strip() for tag in adapter['tags']] if adapter['tags'] else None

        return item

class MySQLPipeline:
    """ The MySQLPipeline handles the connection with the database to save the scraped items """

    @classmethod
    def from_crawler(cls, crawler):
        """ Default method to provide access to the crawler components from the pipeline """

        return cls(crawler)

    def __init__(self, crawler):
        """ Initialize the database connector and the cursor and create the table if it does not
        exist """

        self.connector = mysql.connector.connect(
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            database = crawler.settings.get('MYSQL_DB')
        )

        self.cursor = self.connector.cursor()

        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS courses(
                                    url VARCHAR(255) NOT NULL,
                                    title VARCHAR(255),
                                    image_url TEXT,
                                    publication_date DATE,
                                    tags JSON,
                                    PRIMARY KEY (url)
                                )
                            """)

    def process_item(self, item, spider): # pylint: disable=unused-argument
        """ Insert the item in the table, possibly updating it if already present """

        self.cursor.execute("""
                        insert into courses (url, title, image_url, publication_date, tags)
                        values (%(url)s, %(title)s, %(image_url)s, %(publication_date)s, %(tags)s)
                        on duplicate key update title = %(title)s, image_url = %(image_url)s,
                        publication_date = %(publication_date)s, tags = %(tags)s
                    """,
                    {
                        "url": str(item["url"]),
                        "title": str(item["title"]),
                        "image_url": str(item["image_url"]),
                        "publication_date": item["publication_date"],
                        "tags": json.dumps(item["tags"]),
                    }
        )

        self.connector.commit()

    def close_spider(self, spider): # pylint: disable=unused-argument
        """ Close the cursor and the connection when the spider is closed  """

        self.cursor.close()
        self.connector.close()
