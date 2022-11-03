import requests
import time
from bs4 import BeautifulSoup
import urllib.request
import json


# url = 'https://forum.gamer.com.tw/B.php?bsn=60076' # 要爬特定版塊文章列表要加 cookie!!!!!!!

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    # 每次重開頁面需重拿cookie
    "cookie": 'ckM=1599860641; MB_BAHAID=Young0921000; MB_BAHANICK=%E6%9B%B9%E4%BD%A0%E9%A6%AC%E9%81%8E%E4%BE%86%E4%B8%80%E4%B8%8B; ckFORUM_setting=113112222121113123; __gads=ID=3d65e6c5a82468d9:T=1659580242:S=ALNI_Ma9KA7o_Se7JsREzAYTHXA-_n_r3Q; ckForumDarkTheme=yes; ANIME_dark_theme=1; _ga=GA1.4.1654645225.1662095618; ckFORUM_styles=1; BAHAID=Young0921000; BAHAHASHID=3ce51c01e1234db31da8c864ce3354517c4f692f40ee6e922462a2b0d97ed2db; BAHANICK=%E6%9B%B9%E4%BD%A0%E9%A6%AC%E9%81%8E%E4%BE%86%E4%B8%80%E4%B8%8B; BAHALV=27; BAHAFLT=1558783859; age_limit_content=1; ga_class1=E; __gpi=UID=00000834192031f9:T=1659580242:RT=1666342794:S=ALNI_MYBAO772A3ng335stW-XpVYkVa-Hw; _gid=GA1.3.1645096097.1667176980; BAHAENUR=9ad92b155facf6d97571a8e9b3a5c929; BAHARUNE=53b961663a5c8764951109baa0fc7ece6550a3df65518762192b0d857c8e1bee865d04090b25e980c8e5; MB_BAHARUNE=53b961663a5c8764951109baa0fc7ece6550a3df65518762192b0d857c8e1bee865d04090b25e980c8e5; avtrv=1667436137870; ckBahaGif=0005ec868b247c3f0a94f147cb08e951; hahatoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJmaXJlYmFzZS1hZG1pbnNkay0ydGw0YkBoYWhhbXV0LTg4ODguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJzdWIiOiJmaXJlYmFzZS1hZG1pbnNkay0ydGw0YkBoYWhhbXV0LTg4ODguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczpcL1wvaWRlbnRpdHl0b29sa2l0Lmdvb2dsZWFwaXMuY29tXC9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImlhdCI6MTY2NzQ1MjcyOSwiZXhwIjoxNjY3NDU2MzI5LCJ1aWQiOiJ5b3VuZzA5MjEwMDAiLCJjbGFpbXMiOnsicGxhdGZvcm0iOiJXRUIiLCJuaWNrIjoiXHU2NmY5XHU0ZjYwXHU5OWFjXHU5MDRlXHU0Zjg2XHU0ZTAwXHU0ZTBiIiwiZGVueXBvc3QiOmZhbHNlLCJtb2JpbGUiOnRydWV9fQ.qqfnhhZbH8NzQOHdifAhLSTbmFZZjiVJZzsUZGXTURIM2ZyW0qjA5SH6S8oKUg2uTmlrjIxA9NlvIZffKLLIPvyxtZ2fQj0MHYIn874KfNbfyARkjj1l5XjBS8m1ntKzeQcpe6ugRksy4QJuvvbNzqzFFAHLynfl7UqT7io_MKWzXoC9XOemJmP5-CNIYOcJgD3fjXjbba8Dm-qrO4PvdvlhffeCEJ7nia6Z73RYM7dmkLxQO1HDMmn5xk4HqHQHqY8uIWHugTV3qtQxs2OYql_41fUOZGjp-1tKaitumN-DFqYbDyAUvH6jmpNRp9iez9LiuD-Rad3hawCVnEso5A; hahatoken_topbar=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJmaXJlYmFzZS1hZG1pbnNkay0ydGw0YkBoYWhhbXV0LTg4ODguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJzdWIiOiJmaXJlYmFzZS1hZG1pbnNkay0ydGw0YkBoYWhhbXV0LTg4ODguaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJhdWQiOiJodHRwczpcL1wvaWRlbnRpdHl0b29sa2l0Lmdvb2dsZWFwaXMuY29tXC9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImlhdCI6MTY2NzQ1MjczNiwiZXhwIjoxNjY3NDU2MzM2LCJ1aWQiOiJ5b3VuZzA5MjEwMDAiLCJjbGFpbXMiOnsicGxhdGZvcm0iOiJXRUIiLCJuaWNrIjoiXHU2NmY5XHU0ZjYwXHU5OWFjXHU5MDRlXHU0Zjg2XHU0ZTAwXHU0ZTBiIiwiZGVueXBvc3QiOmZhbHNlLCJtb2JpbGUiOnRydWV9fQ.BXd_IZqz-_Ip2c1C1ZbH0pf83jTn8tPNgfHXg4taGE8xKPHxoGCfidyzikRHjcvfU8hd6Fmz2VEAYH0D6lIdsSImN4NlFI6oP0BzgjUnDRdQgk15Llbr9WbtOTVpPBIuk7f-xBD5kR-A55BTW_Ap0Pv6a7s48yGS4nRYIP9Ro0IN61bY2BFupaKZXkt3e_Owb2Gu0lqx0DfBLuWK-gULDqR4AManctJBQgQrN6-KKnpeQ_oX5_NeWdTj0I6Hmp2PQjUQuUq6EHjJcnYVK8dNilYwjgHw0b064L1MBzrsa__FqWz7ghjaOuyiRb4CbdGk6CjPDVHmW7X22WObDe_eVg; __cf_bm=I2Fyo1ZDFs5HmSiwQZUNmx2yexDPMRR_oXz7l869_GY-1667455425-0-Acm+wuUuSFXuj1IcQtHWDEAX2d0vKAU+U+1PGkpEBziqItn7itc1AlU2uwxK6D/VBMF99vuhGmfbOt+U6jfDJFE=; ckFORUM_bsn=60076; ckBH_lastBoard=[[%2260076%22%2C%22%E5%A0%B4%E5%A4%96%E4%BC%91%E6%86%A9%E5%8D%80%22]%2C[%2260292%22%2C%22%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88%E6%9D%BF%22]%2C[%2260030%22%2C%22%E9%9B%BB%E8%85%A6%E6%87%89%E7%94%A8%E7%B6%9C%E5%90%88%E8%A8%8E%E8%AB%96%22]%2C[%2247157%22%2C%22%E6%98%9F%E6%9C%9F%E4%B8%80%E7%9A%84%E8%B1%90%E6%BB%BF%22]%2C[%2236072%22%2C%22APEX%20%E8%8B%B1%E9%9B%84%22]%2C[%2225052%22%2C%22%E6%80%AA%E7%89%A9%E5%BD%88%E7%8F%A0%22]%2C[%2232407%22%2C%22%E8%8D%92%E9%87%8E%E4%BA%82%E9%AC%A5%22]%2C[%2227362%22%2C%22%E9%AC%A5%E9%99%A3%E7%89%B9%E6%94%BB%22]%2C[%2248427%22%2C%22%E9%8F%88%E9%8B%B8%E4%BA%BA%22]%2C[%2260599%22%2C%22Steam%20%E7%B6%9C%E5%90%88%E8%A8%8E%E8%AB%96%E6%9D%BF%22]]; ckBahamutCsrfToken=892a3ee7da865aa7; ckBAHAADS={"FA":{"a2":1,"a3":24,"a0":1}}; _ga=GA1.1.1654645225.1662095618; ANIME_SIGN=03bdfbc0d0b1fd310cd79afabd157e5ea22b356e13b94e5963635b81; buap_modr=p004; buap_puoo=p101; ckBahaAd=-----0-13----------------; _ga_MT7EZECMKQ=GS1.1.1667455861.177.1.1667455957.60.0.0; _ga_2Q21791Y9D=GS1.1.1667452722.88.1.1667455959.60.0.0'
}


def get_web_page(url):
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print('invalid url', resp.status_code)
        return None
    else:
        print('ok')  # 成功取得網頁回應
        return resp.text


def get_article_url_list(dom): # 蒐集文章列表所有url
    article_url_list = []
    soup = BeautifulSoup(dom, features='lxml')
    item_blocks = soup.select('table.b-list tr.b-list-item')
    for item_block in item_blocks:
        title_block = item_block.select_one('.b-list__main__title')
        article_url = f"https://forum.gamer.com.tw/{title_block.get('href')}"
        article_url_list.append(article_url)
        print("url爬取中.......")
    return article_url_list


def get_article_detail(dom):
    soup=BeautifulSoup(dom,features="lxml")
    article_title = soup.select_one("h1.c-post__header__title").text

    article_detail={
        'title':article_title,
    }
    return article_detail

# def get_article_detail_total_page(): # 爬取特定文章回覆頁數


if __name__ == "__main__":
    url = 'https://forum.gamer.com.tw/B.php?bsn=60076'  # 要爬特定版塊文章列表要加 cookie!!
    current_page=get_web_page(url)
    print(current_page)
    # article_url_list = get_article_url_list(current_page)
    # print(article_url_list)
    # print(f"共爬取 {len(article_url_list)} 篇文章")
    # print('=' * 30)
    # for article_url in article_url_list:
    #     article_detail= get_article_detail(article_url_list[0])
    #     print(article_detail['title'])

