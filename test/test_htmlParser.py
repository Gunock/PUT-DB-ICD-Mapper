from unittest import TestCase

from wikipedia import wikipedia

from icd_reader.html_parser.HtmlParser import HtmlParser
from icd_reader.wikipedia_client.WikipediaClient import WikipediaClient


class TestHtmlParser(TestCase):
    def test_find_icd_section_title(self):
        wikipedia_client: WikipediaClient = WikipediaClient('en')
        parsed_response_content: dict = wikipedia_client.search('ICD-10')
        icd_list_page_title: str = parsed_response_content['query']['search'][0]['title']
        icd_list_page_html: str = str(wikipedia.page(icd_list_page_title).html())
        disease_group_page_title: str = HtmlParser.find_icd_section_title(icd_list_page_html, 'E10.3')

        self.assertEqual('ICD-10 Chapter IV: Endocrine, nutritional and metabolic diseases', disease_group_page_title)

    def test_find_disease_name_and_link(self):
        wikipedia_client: WikipediaClient = WikipediaClient('en')
        parsed_response_content: dict = wikipedia_client.search(
            'ICD-10 Chapter IV: Endocrine, nutritional and metabolic diseases')
        icd_disease_group_page_title: str = parsed_response_content['query']['search'][0]['title']
        icd_disease_group_page_html: str = str(wikipedia.page(icd_disease_group_page_title).html())
        link, title = HtmlParser.find_disease_name_and_link(icd_disease_group_page_html, 'E10.3')

        self.assertEqual('https://en.wikipedia.org/wiki/Diabetic_retinopathy', link)
        self.assertEqual('Diabetic retinopathy', title)
