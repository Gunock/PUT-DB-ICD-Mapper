"""Contains implementation of HtmlParser class."""
import re

from bs4 import BeautifulSoup


class HtmlParser:
    """Contains methods used for getting desired data from wikipedia pages HTML."""

    @staticmethod
    def find_icd_section_title(html: str, icd_10_code: str) -> str:
        """
        Finds link for disease section page on ICD-10 english page.

        :param html: html document
        :param icd_10_code:
        :return: title of wikipedia article about given icd 10 code category
        """
        html_object: BeautifulSoup = BeautifulSoup(html, 'html.parser')

        if html_object.title == 'ICD-10 - Wikipedia':
            raise Exception("Not ICD-10 page")
            pass

        matches = re.findall('(([a-zA-Z]+)([0-9]+))(\\..+)?', icd_10_code)
        letter: str = matches[0][1].upper()

        links_in_table: list = html_object.select('table.wikitable td:nth-child(2) a')
        for disease_link in links_in_table:
            icd_range: str = disease_link.get_text()
            if letter not in icd_range:
                continue
            else:
                return disease_link.get('title')

        return ''

    @staticmethod
    def _find_disease_in_section(parent_element, icd_10_code: str) -> tuple:
        sub_disease_sections = parent_element.findAll('li')
        if sub_disease_sections is None:
            return None, None

        for sub_section in sub_disease_sections:
            if sub_section is None:
                continue

            disease_line = parent_element.findChildren('li', recursive=False)
            if disease_line is not None:
                for li in disease_line:
                    search_result = HtmlParser._find_disease_in_section(li, icd_10_code)
                    if search_result is not None:
                        return search_result

            line_texts = sub_section.findChildren('a')
            for line_text in line_texts:
                if line_text.get_text() not in icd_10_code:
                    pass
                elif line_text.get_text() == icd_10_code:
                    article_link: str = line_texts[1].get('href')
                    article_title: str = line_texts[1].get('title')
                    return article_link, article_title

        """"""

    @staticmethod
    def find_disease_name_and_link(html: str, icd_10_code: str) -> tuple:
        """
        Finds disease on disease section page and returns its link and title.

        :param html: html document
        :param icd_10_code:
        :return: link to article and its title.
        """
        html_object: BeautifulSoup = BeautifulSoup(html, 'html.parser')

        if html_object.title == 'ICD-10 - Wikipedia':
            raise Exception("Not ICD-10 page")

        disease_sections: list = html_object.select('div:not(#toc) > ul')

        for section in disease_sections:
            article_link, article_title = HtmlParser._find_disease_in_section(section, icd_10_code.upper())
            if article_link is not None:
                return article_link, article_title