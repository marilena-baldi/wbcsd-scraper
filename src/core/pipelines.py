""" Scrapy pipelines """

from itemadapter import ItemAdapter
import dateparser


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
