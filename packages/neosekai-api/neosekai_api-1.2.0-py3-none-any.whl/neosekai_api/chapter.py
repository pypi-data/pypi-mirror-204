from neosekai_api.novel import Novel
import requests
from bs4 import BeautifulSoup
from neosekai_api.helper import heavy_translate


class NovelChapter:
    '''
    NovelChapter object

    :params _url : The Mangadex Chapter URL
    '''

    def __init__(self, _url: str) -> None:
        self.url = _url
        self.__response_object = requests.get(self.url, timeout=10)
        self.details = self.chapter_details()
        self.volume = self.details['volume']
        self.name = self.details['chapter_name']
        self.release_date = self.details['release_date']


    def chapter_details(self):
        """
        returns chapter details : 

        - chapter volume
        - chapter name
        - url
        - chapter release date

        In the given order in JSON format
        """
        novel_url_ = self.url.split('neosekaitranslations.com/novel/')[-1]
        novel_name = novel_url_[:novel_url_.index('/')]
        novel_url = f"https://www.neosekaitranslations.com/novel/{novel_name}/"
        novel = Novel(novel_url)
        index_page = novel.get_index_page()
        for i in index_page:
            if index_page[i]['url'] == self.url:
                return index_page[i]

    def get_chapter_content(self, fancy=True):
        """
        returns main chapter content in JSON format

        JSON format:
        ```json
            {
                "1" : {
                    "type" : '...', "content" : '...'
                }
            }
        ```
        - each key will be a paragraphs
        - ```type```  can have a value of ```text``` for textual content
        - ```type``` can have a value of ```img``` if the content is an image. link to the image will be provided in ```content```

        """
        soup = BeautifulSoup(self.__response_object.text, 'lxml')
        div = soup.find('div', attrs={'class': 'text-left'})
        paras = div.find_all('p')
        content = {}
        n = 1
        for i in paras:
            if i.span != None:
                content[str(n)] = {'type': 'text',
                                   'content': i.span.text.strip() if fancy else heavy_translate(i.span.text.strip())}
                n += 1
            elif i.img != None:
                content[str(n)] = {'type': 'img', 'content': i.img['src']}
                n += 1
            else:
                continue
        if fancy:
            return content
        else:
            return heavy_translate(content)
