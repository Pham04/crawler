from bs4 import BeautifulSoup
import requests
import csv


def crawl(keyword):
    keyword = keyword.replace(' ', '+')
    master_lists = []
    for i in range(3):
        search_url = f'https://scholar.google.com/scholar?hl=en&as_sdt={i}%2C5&q={keyword}&btnG='
        html_doc = requests.get(search_url)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        for item in soup.find_all(class_='gs_r gs_or gs_scl'):
            item_ = item.find(class_='gs_ri')
            # Title
            heading = item_.find('h3')
            title = heading.find('a').get_text()
            # Citation
            cited = item_.find(class_='gs_fl')
            cited_text = cited.get_text().split()
            citation = int(cited_text[4])
            # Link
            link = ''
            link_item1 = item.find(class_='gs_ggs gs_fl')
            if link_item1 is not None:
                link_item2 = link_item1.find(class_='gs_ggsd')
                link_item3 = link_item2.find(class_='gs_or_ggsm')
                link_item4 = link_item3.find('a')
                link = link_item4['href']
            else:
                link = 'None'
            master_lists.append((title, citation, link))
    master_lists.sort(key=lambda master_list: master_list[1], reverse=True)
    print(*master_lists, sep='\n')


crawl('machine learning')

data = tuple(crawl('machine learning'))
result = open("Crawler.csv", 'w')
writer = csv.writer(result, dialect='excel')
writer.writerows(data)
result.close()