#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''220720 ver1.1 / chromedriver 경로 = local

              수정) 1. 사이트 추가
                    2. 기본 3개 탐색 고도화(확률 높은 태그로 먼저 찾기 + 세부 설정으로 덮어씌우기)
                    3. Type 6개로 수정
                    4. 타이틀 전후처리 패턴 수정
                    5. Type == 위시, 경우의 수 3가지 설정
                    6. 대상 site ~velog
                    
                     '''

import requests
import re
import pymysql
import json
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import urllib.request
import sys;
from urllib import parse


# data - mysql DB 접속 #라니 오픈
try:
    db = pymysql.connect(host="login-lcture-fnu.cjk00gposwcb.ap-northeast-2.rds.amazonaws.com",
                         user='admin', password='zang0903!!', db='nodebird', charset='utf8mb4')
    cur = db.cursor()

except Exception as e:
    print("디비 접속 에러...")

# 리스트 공간

Type = []
Category_in = []
Distributor = []
Publisher = []
Category_out = []
Logo_image = []
Channel_logo = []
Thumbnail_image = []
User_url = []
Title = []
Maker = []
Date = []
Summary = []
Crawl_content = []
Emotion_cnt = []
Comm_cnt = []
Description = []
Comment = []
Tag = []
View_cnt = []
Duration = []
Lower_price = []
Lower_mall = []
Lower_price_card = []
Lower_mall_card = []
Star_cnt = []
Review_cnt = []
Review_content = []
Dscnt_rate = []
Origin_price = []
Dlvry_price = []
Dlvry_date = []
Model_no = []
Color = []
Location = []
Title_searched = []
Lower_price_searched = []
Lower_mall_searched = []
Lower_url_searched = []

# 라니 오픈
# https://wikidocs.net/16049 참고
# 파이썬 실팽시 파라미터로 url 받도록 수정
User_url = sys.argv[1]
# 파이썬 실팽시 파라미터로 user id 받도록 수정
UserId = sys.argv[2]

# # 제이 오픈, 라니 클로즈
# User_url = input("???")

#설명 1번

#url accessibility check

#FB 헤더값

headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

#개인 헤더값
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

try:
    res = requests.get(User_url, timeout=10, headers = headers) 
except:
    print('TIME OUT')
    
if res.status_code != 200:
    print("URL 오류입니다")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    print("header값 변경 후는? ", res.status_code)
    
# url redirection 잡기
        
if 'msearch' in User_url:

    User_url = User_url.replace("https://msearch", "https://search")
# elif 'm.' in User_url: ##네이버 부동산 오류 발생하여 일단 사용 중지
#     User_url = User_url.replace("https://m.", "https://")

try:
    with urllib.request.urlopen(User_url) as response:
        User_url = response.geturl()
        print("Redirection된 URL은, ", User_url)
except:
    
    User_url = User_url
    print("No Redirection된 URL은, ", User_url) 

# naver 앱 url(shorten and redirection and decode)
if 'link.naver.com' in User_url:

    User_url_decoded = parse.unquote(User_url)
#     print("User_url_decoded URL은, ", User_url_decoded) 

    User_url_decoded_re = re.compile('(?<=bridge\?url\=)(.*?)(?=\&dst)')

    User_url_decoded_red1 = User_url_decoded_re.findall(User_url_decoded)

    for User_url_decoded_red in User_url_decoded_red1:
        User_url = User_url_decoded_red
        
        print("link.naver의 redirection은", User_url)
               
#     if 'msearch' in User_url:
        
#         User_url = User_url.replace("https://msearch", "https://search")
        
#         print("User_url은? ", User_url)
    
# url split

User_url_list = re.split('\.|/|\?', User_url)

print("User_url_list는 ", User_url_list)

# DIstributor 키워드가 2개 이상 들어간 경우를 대비, 0~6번째까지 추출하여 Dstributor_key 와 매칭

User_url_list_Distributor = User_url_list[0:6]

print("User_url_list_Distributor는 ", User_url_list_Distributor)

# 설명 2번

# Distributor keyword input

Distributor_keyword_list = ['naver', 'coupang', '11st', 'tistory', 'daangn', 'instagram', 'musinsa', 'a-bly', 'zigzag', 
                            'brandi', 'gmarket', 'oliveyoung', 'wemakeprice', 'tmon', 'auction', 'gsshop', 'hnsmall', 'cjonstyle', 
                            'joongna', 'joonggonara', 'bunjang', 'facebook', 'velog', 'github', 'youtube', 'tiktok', 'google',
                           'aliexpress', 'amazon', 'ebay', 'interpark', '29cm','mycake', 'hfashionmall', 'ikea', 'kcar', 'wikipedia',
                           'kbchachacha', 'lfmall', 'nsmall', 'sivillage', 'ssfshop', 'ssg']

#Distributor 한글화 ( for Title 전처리 시 Distributor 한글 이름 제외 )

Distributor_keyword_list_Kor_dict = {'naver':'네이버', 'coupang':'쿠팡', '11st':'11번가', 'tistory':'티스토리', 'daangn':'당근마켓',
                                     'instagram':'인스타그램', 'musinsa':'무신사', 'a-bly':'에이블리', 'zigzag':'지그재그', 
                                     'brandi':'브랜디', 'gmarket':'지마켓', 'oliveyoung':'올리브영', 'wemakeprice':'위메프', 
                                     'tmon':'티몬', 'auction':'옥션', 'gsshop':'GS샵', 'hnsmall':'홈앤쇼핑', 'cjonstyle':'CJ온스타일', 
                                     'joongna':'중고나라', 'joonggonara':'중고나라', 'bunjang':'번개장터', 'facebook':'페이스북',
                                     'velog':'velog', 'github':'github', 'youtube':'유튜브', 'tiktok':'tictok', 'google':'google',
                                     'aliexpress':'aliexpress', 'amazon':'amazon', 'ebay':'ebay', 'interpark':'인터파크', '29cm':'29CM',
                                    'mycake':'Cake', 'hfashionmall':'H 패션몰','ikea':'IKEA', 'kcar':'kcar', 'wikipedia':'위키백과',
                                    'kbchachacha':'KB차차차', 'lfmall':'LF몰', 'nsmall':'NS홈쇼핑', 'sivillage':'S.I.VILLAGE',
                                    'ssfshop':"삼성물산 온라인몰 SSF Shop", 'ssg':'SSG.COM'}
# keyword 추가 필요

# url - Distributor_keyword list match

# soup 정의 설정
# ua = UserAgent(use_cache_server=True)

soup = BeautifulSoup(res.content, 'html.parser')

Distributor_keyword_match_list = list(
    set(User_url_list_Distributor).intersection(Distributor_keyword_list))
print("Distributor_keyword_match_list은", Distributor_keyword_match_list)
if len(Distributor_keyword_match_list) >= 1:

    Distributor_key = Distributor_keyword_match_list[0]

else:

    try:
        Distributor_key = soup.select_one(
            'meta[property="og:site_name"]')['content']
    except:
        try:
            Distributor_key = soup.select_one('title').get_text()
        except:
            Distributor_key = "해당 링크에서 직접 보기"

if Distributor_key == 'mycake':
    Distributor_key = 'cake'
print("Distributor_key 값은 ", Distributor_key)

# 설명 3번

# Category_in_keyword input
# 11개 테마: 교육/독서, 리빙, 문화/엔터, 반려동물, 뷰티/패션, 스포츠/게임, 여행/아웃도어, 요리/맛집, 자동차, 재테크, 기타

# 사용자가 저장한 컨텐츠를 모음에서 찾을 때 어떻게 찾을지도 고려해봐야 할 듯 함(ex. 네이버 카페에서 저장한 게시물은 현재 type:글, 테마: 기타)
# 저장한 컨텐츠의 내용 위주(현재 11개 테마)로 갈지, 출처 위주(Ex. 블로그 , 카페, SNS, 장소, 음악, 영화 등)로 갈지 고민해봐야 할 듯 함

Category_in_keyword_list_shopping = ['11st', 'coupang', 'musinsa', 'a-bly', 'zigzag', 'brandi', 'gmarket', 'oliveyoung',
                                     'wemakeprice', 'idus', 'tmon', 'auction.', 'gsshop.', 'shopping', 'smartstore', 
                                     'hnsmall', 'cjonstyle', 'brand.naver', 'store', 'products', 'product', 'wemakeprice', 
                                     'tmon', 'goods', 'aliexpress', 'amazon', 'ebay', 'interpark', '29cm', 'hfashionmall',
                                    'land', 'ikea', 'kcar', 'kbchachacha', 'lfmall', 'nsmall', 'sivillage', 'ssfshop',
                                    'ssg']
Category_in_keyword_list_blog = ['blog', 'tistory', 'velog', 'github', 'contents', 'premium', 'post']
Category_in_keyword_list_sns = ['instagram', 'band', 'facebook']
Category_in_keyword_list_video = ['youtube', 'tiktok', 'tv', 'mycake']
Category_in_keyword_list_second = ['daangn', 'joonggonara', 'joongna', 'bunjang', 'products', 'shop']
Category_in_keyword_list_cafe = ['cafe']
Category_in_keyword_list_news = ['news', 'joongang', 'yna', 'weather', 'entertain', 'wikipedia']
Category_in_keyword_list_images = ['img', 'jpg', 'png', 'jpeg']
Category_in_keyword_list_enter = ['book', 'music', 'music-flo']
Category_in_keyword_list_map = ['map', 'maps', 'tmap', 'place']

# keyword 추가 필요

# url - Distributor_keyword list match

#url - Distributor_keyword list match

Category_in_keyword_list_all = [Category_in_keyword_list_cafe, Category_in_keyword_list_news, 
                                Category_in_keyword_list_shopping, Category_in_keyword_list_blog, Category_in_keyword_list_sns, 
                                Category_in_keyword_list_video, Category_in_keyword_list_second, Category_in_keyword_list_images,
                                Category_in_keyword_list_enter, Category_in_keyword_list_map]

Category_in_keyword_dict = {'image' : Category_in_keyword_list_images, 'news' : Category_in_keyword_list_news, 
                            'cafe' : Category_in_keyword_list_cafe, 'second' : Category_in_keyword_list_second, 
                            'blog' : Category_in_keyword_list_blog, 'shopping' : Category_in_keyword_list_shopping, 
                            'sns' : Category_in_keyword_list_sns, 'video' : Category_in_keyword_list_video,
                            'enter' : Category_in_keyword_list_enter, 'map' : Category_in_keyword_list_map}

#해결필요: Category_in_keyword_dict 의 vlaues 값 중복 시 마지막 하나만 표현(dict 고유의 성격), 따라서 key값이 마지막것으로 표현됨

Category_in_keyword_match_list_cnt_dict = dict()

for Category_in_keyword_list_all_i in Category_in_keyword_list_all:
    Category_in_keyword_match_list = list(set(User_url_list).intersection(Category_in_keyword_list_all_i))
    Category_in_keyword_match_list_cnt = len(Category_in_keyword_match_list)
    Category_in_keyword_match_list_cnt_dict[Category_in_keyword_match_list_cnt] = Category_in_keyword_list_all_i

if max(Category_in_keyword_match_list_cnt_dict.keys()) == 0:
    Category_in_key = "해당 링크에서 직접 보기"

else:
    Category_in_keyword_match_list_cnt_dict_keys_max_values = Category_in_keyword_match_list_cnt_dict[max(Category_in_keyword_match_list_cnt_dict.keys())]

    for key, value in Category_in_keyword_dict.items():
        if value == Category_in_keyword_match_list_cnt_dict_keys_max_values:
            Category_in_key = key

Category_in.append(Category_in_key)

print("Category_in 리스트 값은 ", Category_in)

#Publisher & Distributor & Category_out 파악

if Category_in_key == 'news':

#     if Distributor_key == 'naver':

#         #시도 1
#         try:
#             Category_out2 = []
#             Category_out_key1 = soup.select('em.media_end_categorize_item') or soup.select('em.guide_categorization_item')
#             for Category_out_key in Category_out_key1:
#                 Category_out2.append(Category_out_key.text)
#             Category_out = Category_out2
#             print("확인", Category_out)
#         except:
#             Category_out_key = "해당 링크에서 직접 보기"
#             Category_out.append(Category_out_key)

#         #시도2
#         try:
#             Category_out_key1 = soup.select('em.media_end_categorize_item')
#             for Category_out_key in Category_out_key1:
#                 Category_out.append(Category_out_key.text)
#         except:
#             try:
#                 Category_out_key1 = soup.select('em.guide_categorization_item')
#                 for Category_out_key in Category_out_key1:
#                     Category_out.append(Category_out_key.text)

#             except:
#                 Category_out_key = "해당 링크에서 직접 보기"
#                 Category_out.append(Category_out_key)

#         print("Category_out 리스트 값은 ", Category_out)

    try:
        Publisher_key = soup.select_one('meta[property="og:article:author"]')['content']
        Distributor_key = Publisher_key

    except: 
        Publisher_key = "해당 링크에서 직접 보기"

    Publisher.append(Publisher_key)

    Distributor.append(Distributor_key)

    print("Publisher 리스트 값은 ", Publisher)
    print("수정된 Distributor 리스트 값은 ", Distributor)

else:
    Distributor.append(Distributor_key)
    print("Distributor 리스트 값은 ", Distributor)

# 설명 4번
# Type 파악

if Category_in_key in ['news', 'cafe', 'blog']:
    Type_key = "글"

elif Category_in_key in ['shopping', 'second']:
    Type_key = "위시"

elif Category_in_key in ['video', 'enter']:
    Type_key = "동영상"

elif Category_in_key in ['sns']:
    Type_key = "이미지"

    # jpg 등 이미지 확장자가 url에 포함된 경우 이를 이미지로 분류
elif any(Category_in_keyword_list_image in User_url for Category_in_keyword_list_image in Category_in_keyword_list_images) == True:
    Type_key = "이미지"

elif Category_in_key in ['map']:
    Type_key = "지도"
    
else:
    Type_key = "기타"

Type.append(Type_key)
print("Type 리스트 값은 ", Type)

#설명 5번

# 기본 3개(Title, Description, Thumbnail_image) 값 찾기

# 기본 bs4 크롤링 설정
headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

res = requests.get(User_url, timeout=5, headers=headers) 
soup = BeautifulSoup(res.content, 'html.parser')

print("응답코드 bs4 일반: ", res.status_code)

# Title scraping: og, twitter, title tag 텍스트 중 가장 긴 값 or 조건(5자 미만 or 탈출문구) 불만족 시 h1, h2, h3 텍스트 중 가장 긴 값 scraping 
# 한글이 없을 경우 ((re.search('[가-힣]', Title_key)) == None) 는 해외사이트 고려하여 조건 추가 안함

try:
    Title_key_og = soup.select_one('meta[property="og:title"]')['content']
except:
    try:
        Title_key_og = " "
        Title_key_twitter = soup.select_one('meta[name="twitter:title"]')['content']
    except:
        try:
            Title_key_twitter = " "
            Title_key_title = soup.select_one('title').get_text()            
        except:
            Title_key_title = "해당 링크에서 직접 보기"
    else:
        try:
            Title_key_title = soup.select_one('title').get_text()
        except:
            Title_key_title = "해당 링크에서 직접 보기"
else:
    try:
        Title_key_twitter = soup.select_one('meta[name="twitter:title"]')['content']
    except:
        try:
            Title_key_twitter = " "
            Title_key_title = soup.select_one('title').get_text()
        except:
            Title_key_title = "해당 링크에서 직접 보기"
    else:
        try:
            Title_key_title = soup.select_one('title').get_text()
        except:
            Title_key_title = "해당 링크에서 직접 보기"
finally:
    try:
        Title_key_dict = {Title_key_og:len(Title_key_og.encode('UTF-8')), Title_key_twitter:len(Title_key_twitter.encode('UTF-8')), Title_key_title:len(Title_key_title.encode('UTF-8'))}
        Title_key_dict_max_values = max(Title_key_dict.values())
        Title_key_dict_reversed= dict(map(reversed, Title_key_dict.items()))
        Title_key = Title_key_dict_reversed[Title_key_dict_max_values]
        
    except:
        Title_key = "해당 링크에서 직접 보기"
        
def Title_key_h_tag():
    global Title_key  
    try:
        Title_key_h1 = soup.select_one('h1').get_text()
    except:
        try:
            Title_key_h1 = " "
            Title_key_h2 = soup.select_one('h2').get_text()
        except:
            try:
                Title_key_h2 = " "
                Title_key_h3 = soup.select_one('h3').get_text()
            except:
                Title_key_h3 = "해당 링크에서 직접 보기"
    else:
        try:
            Title_key_h2 = soup.select_one('h2').get_text()
        except:
            try:
                Title_key_h2 = " "
                Title_key_h3 = soup.select_one('h3').get_text()
            except:
                Title_key_h3 = "해당 링크에서 직접 보기"
    finally:
        try:
            Title_key = max(Title_key_h1, Title_key_h2, Title_key_h3, key = len)
        except:
            try:
                Title_key = Title_key
            except:
                Title_key = "해당 링크에서 직접 보기"

try:
    if len(Title_key) < 5 or Title_key == "해당 링크에서 직접 보기" or Title_key == Distributor_keyword_list_Kor_dict[Distributor_key]:
        Title_key_h_tag()
except:
    if len(Title_key) < 5 or Title_key == "해당 링크에서 직접 보기":
        Title_key_h_tag()    
            
if len(Title_key) < 5:
    Title_key = "해당 링크에서 직접 보기"


# Desc. 우선순위대로 실행    
try:
    Description_key_og = soup.select_one('meta[property="og:description"]')['content']
except:
    try:
        Description_key_og = " "
        Description_key_name = soup.select_one('meta[name="description"]')['content']   
    except:
        try:
            Description_key_name = " "
            Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']        
        except:
            Description_key_twitter = "해당 링크에서 직접 보기"
    else:
        try:
            Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']        
        except:
            Description_key_twitter = "해당 링크에서 직접 보기"
else:
    try:
        Description_key_name = soup.select_one('meta[name="description"]')['content']   
    except:
        try:
            Description_key_name = " "
            Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']
        except:
            Description_key_twitter = "해당 링크에서 직접 보기"
    else:
        try:
            Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']
        except:
            Description_key_twitter = "해당 링크에서 직접 보기"
finally:
    try:
        Description_key = max(Description_key_og, Description_key_name, Description_key_twitter, key = len)
    except:
        Description_key = "해당 링크에서 직접 보기"

if len(Description_key) < 5 or Description_key == "해당 링크에서 직접 보기":
    try:
        Description_key_h1 = soup.select_one('h1').get_text()
    except:
        try:
            Description_key_h2 = soup.select_one('h2').get_text()
        except:
            Description_key_h2 = "해당 링크에서 직접 보기"
    else:
        try:
            Description_key_h2 = soup.select_one('h2').get_text()
        except:
            Description_key_h2 = "해당 링크에서 직접 보기"
    finally:
        try:
            Description_key = max(Description_key_h1, Description_key_h2, key = len)
        except:
            Description_key = "해당 링크에서 직접 보기"
            
if len(Description_key) < 5:
    Description_key = "해당 링크에서 직접 보기"

# Image
try:
    Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
except:
    try:
        Thumbnail_image_key = soup.select_one('meta[property="twitter:image"]')['content']
    except:
        try:
            Thumbnail_image_key = soup.select_one('img')['src']        
        except:
            Thumbnail_image_key = "해당 링크에서 직접 보기"
            
# Duration_key 설정
if Distributor_key == "youtube":
    try:
        Duration_key = soup.select_one(
            'meta[itemprop="duration"]')['content']
        Duration_key = Duration_key.replace(
            "PT", "").replace("M", "분 ").replace("S", "초")

    except:
        Duration_key = "해당 링크에서 직접 보기"
    Duration.append(Duration_key)
    print("Duration 리스트 값은, ", Duration)

print('기본 bs Title_key 값은, ', Title_key)
print('기본 bs Description_key 값은, ', Description_key)
print('기본 bs Thumbnail_image_key 값은, ', Thumbnail_image_key)    
    
# 개별 site 크롤링 설정

try:  
    if 'blog.naver' in User_url:
    #설명 5번_iframe
        #iframe 대비 src_url 설정
        #FB일 경우 SRC 탐색 X
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        res = requests.get(User_url, timeout=3, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')

        src_url = "https://blog.naver.com/" + soup.iframe['src']
        print(src_url)
        res_iframe = requests.get(src_url, timeout=3, headers=headers)
    #     res_noifr.status_code
        soup_iframe = BeautifulSoup(res_iframe.content, "html.parser") 
        try:
            Title_key = soup_iframe.select_one('meta[property="og:title"]')['content']    
        except:
            Title_key = Title_key
        try:
            Description_key = soup_iframe.select_one('meta[property="og:description"]')['content']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = soup_iframe.select_one('meta[property="og:image"]')['content']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    # elif 'music-flo' in User_url:

    #     print("응답코드: ", res.status_code)

    #     #iframe 대비 src_url 설정

    #     src_url = "https://blog.naver.com/" + soup.select_one('iframe["src"]')
    #     res_iframe = requests.get(src_url, headers=headers)
    # #     res_noifr.status_code
    #     soup_iframe = BeautifulSoup(res_iframe.content, "html.parser") 
    #     try:
    #         Title_key = soup_iframe.select_one('meta[property="og:title"]')['content']    
    #     except:
    #         Title_key = "해당 링크에서 직접 보기"
    #     try:
    #         Description_key = soup_iframe.select_one('meta[property="og:description"]')['content']
    #     except:
    #         Description_key = "해당 링크에서 직접 보기"
    #     try:
    #         Thumbnail_image_key = soup_iframe.select_one('meta[property="og:image"]')['content']
    #     except:
    #         Thumbnail_image_key = "해당 링크에서 직접 보기"

    elif 'cafe.naver' in User_url:
    #설명 5번_api    
        #내부 API
        #header값을 유저로 설정 -> meta값 이외 스크래핑 가능

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
        res = requests.get(User_url, timeout=3, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')

        article_no = User_url_list[6] #여기 인덱스 수정. regex로 가져오기( /d+{}
    #     print("article_no", article_no)

        clubid = soup.select_one('input[name="clubid"]')['value']
    #     print("clubid ", clubid )

        User_url_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/' + str(clubid) + '/articles/' + str(article_no)
        print(User_url_api)

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        #내부 api 
        soup_api = BeautifulSoup(res_api.text, 'html.parser')

        script_api = soup_api.text
        dict_result_script_api = json.loads(script_api)

        #meta값
        try:
            Title_key = dict_result_script_api['result']['article']['subject']
        except:
            try:
                #selenium 크롤링 설정(iframe 다중)
                soup = BeautifulSoup(res.text, 'html.parser')

                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('disable-gpu')
                options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                options.add_argument('lang = ko_KR')


                # 크롬드라이버 생성
                # 라니 오픈(제이 클로즈)
#                 chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
                chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
                #제이 경로
                # #chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                driver = webdriver.Chrome(chromedriver, options=options)

                # 크롤링할 사이트 호출
                driver.get(User_url)
                # iframe 진입
                driver.switch_to.frame("cafe_main")

                res_iframe = driver.page_source
                soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                Title_key = soup_iframe.select_one('h3.title_text').get_text()
                driver.quit()
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_api['result']['article']['contentHtml']
        except: # Publisher (카페 네임)
            try:
                Description_key = dict_result_script_api['result']['cafe']['pcCafeName']
            except:  
                try:
                    #selenium 크롤링 설정(iframe 다중)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument('disable-gpu')
                    options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                    options.add_argument('lang = ko_KR')
                    # 크롬드라이버 생성
                    # 라니 오픈(제이 클로즈)
#                     chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
                    chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
                    #제이 경로
                    # #chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                    driver = webdriver.Chrome(chromedriver, options=options)

                    # 크롤링할 사이트 호출
                    driver.get(User_url)
                    # iframe 진입
                    driver.switch_to.frame("cafe_main")

                    res_iframe = driver.page_source
                    soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                    Description_key = soup_iframe.select_one('div.se-main-container').get_text()
                    driver.quit()
                except:
                    Description_key = Description_key

        try: 
            # 카페 대표 썸네일 (게시물 썸네일 불러올 경우 Selenium 필요)
            Thumbnail_image_key = dict_result_script_api['result']['cafe']['image']['url']
        except:
            try:
                #selenium 크롤링 설정(iframe 다중)
                soup = BeautifulSoup(res.text, 'html.parser')

                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('disable-gpu')
                options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                options.add_argument('lang = ko_KR')
                # 크롬드라이버 생성
                # 라니 오픈(제이 클로즈)
#                 chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
                chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
                #제이 경로
                # #chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                driver = webdriver.Chrome(chromedriver, options=options)

                # 크롤링할 사이트 호출
                driver.get(User_url)
                # iframe 진입
                driver.switch_to.frame("cafe_main")

                res_iframe = driver.page_source
                soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                Title_key = soup_iframe.select_one('h3.title_text').get_text()
                driver.quit()
            except:
                try:
                    se_main_container = soup_iframe.select_one('div.se-main-container')
                    Thumbnail_image_key = se_main_container.select_one('img')['src']
                    driver.quit()    
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'coupang' in User_url:
    #설명 5번_script        
        headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

        #일반 bs

        res = requests.get(User_url, timeout=3, headers=headers) 

        soup = BeautifulSoup(res.text, 'html.parser')

        script_re = re.compile('(?<=exports.sdp =).+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace(';', ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['itemName']
        except:
            try:
                Title_key = dict_result_script_text['title']
            except:
                Title_key = Title_key
        try:

            Description_key1 = dict_result_script_text['sellingInfoVo']['sellingInfo']    
            for Description_key in Description_key1:
                Description_key = Description_key
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['images'][0]['detailImage']    
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'gmarket' in User_url:
    #설명 5번_일반(bs)
        print("응답코드: ", res.status_code)

        #         Title_key = soup.select_one('meta[property="og:title"]')['content']http://item.gmarket.co.kr/Item?goodsCode=1695110940
        try:
            Title_key = soup.select_one('meta[property="og:description"]')['content']
        except:
            Title_key = Title_key

        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'oliveyoung' in User_url:
        try:
            Title_key = soup.select_one('p.prd_name').get_text()
        except:
            Title_key = Title_key
            
        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            try:
                Thumbnail_image_key = soup.select_one('div > #mainImg')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'wemakeprice' in User_url:
    #설명 5번_selenium    
        # 크롬드라이버 생성
        # 라니 오픈(제이 클로즈)
#         chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
        chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
        #제이 경로
        # #chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥              
#         chromedriver = 'C:/Users/FNUCNI/chromedriver.exe' # 윈도우

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)')
        options.add_argument('lang = ko_KR')

        driver = webdriver.Chrome(chromedriver, options=options)

        driver.get(User_url)
        User_url = driver.current_url

        print('final redirected url은', User_url)

        headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

        res = requests.get(User_url, timeout=3, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')

        script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
        script_text1 = script_re.findall(str(soup))

        script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['dealNm']
        except:
            try:          
                Title_key = dict_result_script_text['ogTitle']
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['dcateNm']
        except:
            try:
                Description_key = dict_result_script_text['lcateNm']       
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['thumb']['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['origin']['imgUrl'] 
            except:
                Thumbnail_image_key = Thumbnail_image_key
    
    elif 'bunjang' in User_url:

        product_id_bunjang_re = re.compile('(?<=products\/)[0-9]+')

        product_id_bunjang1 = product_id_bunjang_re.findall(User_url)

        for product_id_bunjang in product_id_bunjang1:
            User_url_api = 'https://api.bunjang.co.kr/api/1/product/' + str(product_id_bunjang) + '/detail_info.json?version=4'

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)
        
        try:
            Title_key = result_dict['item_info']['name']
        except:
            Title_key = Title_key
        try:
            Description_key = result_dict['item_info']['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = result_dict['item_info']['product_image']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'cjonstyle' in User_url:
        Title_key_temp = Title_key
        Title_key = Description_key
        Description_key = Title_key_temp       
        
    elif 'kcar' in User_url:
        try:
            Thumbnail_image_key = soup.select_one('#carImgSlider  img')['src']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'nsmall' in User_url: #hnsmall은 앞에서 걸어야 함
        product_id_nsmall_re = re.compile('(?<=product\/)[0-9]+')
        product_id_nsmall = product_id_nsmall_re.findall(User_url)[0]
        User_url_nsmall_api = 'https://mwapi.nsmall.com/webapp/wcs/stores/servlet/DetailProductViewReal'

        headers = {
        'authority': 'mwapi.nsmall.com',
        'method': 'POST',
        # 'path': '/webapp/wcs/stores/servlet/DetailProductViewReal',
        # 'scheme': 'https',
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'content-length': '110',
        # 'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=oSaPrHIIdNVZzXZRyOJJ8KH5SCw%3d%0a%3b2022%2d07%2d18+10%3a17%3a36%2e554%5f1658107056545%2d687992%5f13001%5f1549272167%2c%2d9%2cKRW%5f13001; WC_AUTHENTICATION_1549272167=1549272167%2cibU9QHx7Awccd8err%2fxgbtm%2bPaA%3d; WC_ACTIVEPOINTER=%2d9%2c13001; WC_USERACTIVITY_1549272167=1549272167%2c13001%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2c86EHl%2bYZCaIQnr37dzawxXHxVmTIUYIO%2b6gmfkcnjG0MG%2fU8lH6zAn7%2fEk58EVzKzpGjxI2fFpnO%0aXpKhu9hZ2p9qq4FFXGCAjXVcozS8Pr3XCUJJ%2fKPf59bDuHfQC%2fAtzdHpJ2bwdLOkYvEIaI4zHw%3d%3d; WMONID=j65WmRhaJMb; _qg_fts=1658107057; QGUserId=3536195775064691; _qg_pushrequest=true; goodsTodayCookie=32128684!N; goodsTodayCatIdCookie=32128684!&catalogId=18151&mCategoryId=18151&cate1Code=200302&cate2Code=20767&cate3Code=1811561; _qg_cm=1; RB_PCID=1658107058207701329; _gid=GA1.2.831579550.1658107059; _fbp=fb.1.1658107059581.1853397954; EG_GUID=99428539-52b2-4fc8-a99d-2707b400c307; JSESSIONID=00028-sI5N5cyficE4UWo_bU7oy:1991y6hny; ipAuth=-2117978956; co_cd=110; accpt_path_cd=100; shoppingRefer=http://mwapi.nsmall.com/; a1_gid=Aew+gWHEHeIAC9Tc; appier_utmz=%7B%7D; _atrk_siteuid=xCs6ca_BK2BoCv2-; _atrk_ssid=eXUGUUcMg7VEA-b9IMaGIj; _atrk_sessidx=1; appier_pv_counterc91ce3e5a69b64f=0; appier_page_isView_c91ce3e5a69b64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; appier_pv_counter0876aad651ed64f=0; appier_page_isView_0876aad651ed64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; wcs_bt=s_4c84f6106481:1658107871; gapageInfo=home; __utma=41019966.790199591.1658107059.1658107872.1658107872.1; __utmz=41019966.1658107872.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=41019966; __utmt_UA-92946860-1=1; __utmb=41019966.1.10.1658107872; au_id=990a94931fea3366425f7e7617ddfb5b35b-3d7c; dl_uid=bc5ca977d30eb8fa09d41ffd8846be7; cto_bundle=UQgTlF80YmM4UU1SaEFBWWFydUMwa1RXRm9jZjN2TkwxQTMlMkJ0RTRZJTJCdUglMkJTdUMycCUyRndPZVJYMGlYOWRwQzBXZTIyU0xoZ0hWZVlFVUthb1FNRktOMmIlMkJKMyUyQmlaVGZVd2NvTXlrRlVnekZOb3k1REt0RTdaOVo1ZGNiM0lMQW5CZjQ4b1JmQTdqMDJQd25zRlNRJTJCOFVYZ3VBUSUzRCUzRA; _uni_id=2a1cc137-0ef8-4a7e-9de4-6e90fd191e07; check_uni_send=0; _ga_J7E3QT1NRY=GS1.1.1658107874.1.0.1658107874.0; _ga=GA1.2.790199591.1658107059; _gat_gp=1; _gat_UA-92946860-8=1; RB_SSID=Qdg4m5ZyhS; airbridge_session=%7B%22id%22%3A%22a7fe42ad-92a8-42a2-8c3e-7dcbbf9f42ae%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1658107058956%2C%22end%22%3A1658108058990%7D',
        # 'origin': 'https://mw.nsmall.com',
        # 'referer': 'https://mw.nsmall.com/',
        # 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-site',
        'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        payload = {
        'partNumber': product_id_nsmall #product_id
        # 'cocd': '110',
        # 'imgSizeType': 'Q',
        # 'accptPath': '500',
        # 'accptPathCd': '500',
        # 'req_co_cd': '110',
        # 'userId': '',
        # 'catalogId': '97001'
        }

        res = requests.post(User_url_nsmall_api, headers=headers, data =  payload, timeout = 10) 

        content = res.content
        soup = BeautifulSoup(content,"lxml")

        post_api = soup.text
        dict_post_api = json.loads(post_api)

        Title_key = dict_post_api['msg']['goods'][0]['info']['productName']
        Description_key = dict_post_api['msg']['goods'][0]['info']['productName']
        Thumbnail_image_key = dict_post_api['msg']['goods'][0]['info']['photoList'][0]['photoPath']
        
    elif 'sivillage' in User_url:
        try:
            Title_key = soup.select_one('p.detail__info-description-1').text
        except:
            try:
                Title_key = soup.select_one('meta[property="eg:itemName"]')['content']
            except:
                try:
                    sv_name_re = re.compile('(?<=\'name\':)(.*?)(?=,)')
                    Title_key= sv_name_re.findall(str(soup))[0]
                except:
                    try:
                        Title_key = soup.select_one('h2.tit_article').text
                    except:
                        Title_key = Title_key

        try:
            sv_desc_re = re.compile('(?<=\'variant\':)(.*?)(?=,)')
            Description_key = sv_desc_re.findall(str(soup))[0]
        except:
            try:
                Description_key = soup.select_one('p.detail__info-code').text
            except:
                try:
                    Description_key = soup.select_one('p.txt_excerpt').text
                except:
                    Description_key = Description_key

        try:
            sv_img_re = re.compile('(?<=img:)(.*?)(?=,)')
            Thumbnail_image_key = sv_img_re.findall(str(soup))[0].strip("' ")
        except:
            try:
                Thumbnail_image_key = soup.select_one('div.detail__vi-slide.swiper-slide img')['src']
            except:
                try:
                    Thumbnail_image_key = soup.select_one('div.swiper-zoom-container img')['src']
                except:
                    try:
                        Thumbnail_image_key = soup.select_one('div.image img')['src']
                    except:
                        Thumbnail_image_key = Thumbnail_image_key    
                        
    elif 'ssfshop' in User_url:
        
        try:
            Thumbnail_image_key = soup.select_one('.poster img')['src']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
        if 'live_commerce' in User_url:
            Thumbnail_image_key = 'https://m.ssfshop.com/' + Thumbnail_image_key
            
        if 'community/style' in User_url: #ssf diver 
            ssfsdiver_re = re.compile('(?<=community\/style\/).+')
            ssfsdiver_style_no = ssfsdiver_re.findall(User_url)[0]
            User_url_api = 'https://m.ssfshop.com/community/api/v1/style/getStyle?styleNo=' + ssfsdiver_style_no

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 

            soup_api = BeautifulSoup(res_api.text, 'html.parser')
            dict_result_script_api = json.loads(str(soup_api))

            Thumbnail_image_key = 'https://img.ssfshop.com' + dict_result_script_api['data']['styles'][ssfsdiver_style_no]['styleImgList'][0]
            Description_key = dict_result_script_api['data']['styles'][ssfsdiver_style_no]['contents']
        
except:
    Title_key = Title_key
    Description_key = Description_key
    Thumbnail_image_key = Thumbnail_image_key
    
# Title_key trash word 제거

Title_key_trash_words = ['<br>', '\u200e']

for Title_key_trash_word in Title_key_trash_words:
    Title_key = Title_key.replace(Title_key_trash_word, " ")
    
# 기본 3개 리스트 input
Title.append(Title_key.strip())    
# Desc. trash_word 제거
desc_trash_words = ['ㄴ ', '\t', '\n', '\r\n', '\ufeff', '\u200e']
for desc_trash_word in desc_trash_words:
    Description_key = Description_key.replace(desc_trash_word, "")
    
Description.append(Description_key.strip())
Thumbnail_image.append(Thumbnail_image_key.strip())

print('최종 Title 리스트 값은, ', Title)
print('최종 Description 리스트 값은, ', Description)
print('최종 Thumbnail_image 리스트 값은, ', Thumbnail_image)
print("최종 User_url", User_url)

#설명 6번
# lprice & mall 파악

#Type = 위시 중 아래 3가지로 구분

#1. Lower_price, Searched까지 다 찾는 것(Ex. 11번가 - 구체적 상품 페이지): Type == 위시 구분된 것
#2. Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓): no searched 셋팅
#3. Lower_price, Searched 다 안 찾는 것(Ex. 11번가 - 기획전 페이지): Lower_price == "확인 불가" -> js로 Lower_price 위치 blank 처리(요청 to 라니)

if Type_key == '위시':
    print("현재 가격 스크래핑 시작")

    try:
        # 개별 site 최저가 크롤링 설정

        # 11번가
        if Distributor_key in ['11st']:
            try:
                Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 strong > span.value').text
            except:
                try:
                    Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 span.value').text
                except:   
                    try:
                        Lower_price_key = soup.select_one('#priceLayer > div.price > span > b').text
                    except:
                        product_id_11st_re = re.compile('(?<=products\/pa\/)[0-9]+|(?<=products\/)[0-9]+')

                        product_id_11st1 = product_id_11st_re.findall(User_url)

                        for product_id_11st in product_id_11st1:
                            User_url_api = 'https://www.11st.co.kr/products/v1/pc/products/' + str(product_id_11st) + '/detail'
                            print("User_url_api는?", User_url_api)

                        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                        if res_api.status_code != 200:
                            print("User_url_api 접속 오류입니다")

                        result_dict = json.loads(res_api.text)

                        Lower_price_key = result_dict['price']['finalDscPrice']

        # 쿠팡
        elif Distributor_key in ['coupang']:

            if 'trip.coupang' in User_url: # 쿠팡 트립

                script_text1 = soup.select_one('script#travel-detail-product-data').get_text()
                dict_result_script_text = json.loads(script_text1)
                Lower_price_key = dict_result_script_text['product']['representativeVendorItem']['price']['totalSalesPrice']

            else: # 쿠팡 일반
                script_re = re.compile('(?<=exports.sdp =).+')
                script_text1 = script_re.findall(str(soup))
                script_text = str(script_text1[0].strip().replace(';', ""))
                dict_result_script_text = json.loads(script_text)

                Lower_price_key2 = dict_result_script_text['apiUrlMap']['addToCartUrl']
                Lower_price_key_re = re.compile('(?<=price=)[0-9,]+')
                Lower_price_key1 = Lower_price_key_re.findall(str(Lower_price_key2))
                for Lower_price_key in Lower_price_key1:
                    Lower_price_key = Lower_price_key

        # 무신사
        elif Distributor_key in ['musinsa']:

            Lower_price_key = soup.select_one('#goods_price').text

        # 번개장터
        elif Distributor_key in ['bunjang']:
            Lower_price_key = result_dict['item_info']['price']
            if result_dict['item_info']['status'] == "3":
                Lower_price_key = "품절인가봐요!"

        #에이블리
        elif Distributor_key in ['a-bly']:

            product_id_alby_re = re.compile('(?<=goods\/)[0-9]+')
            product_id_alby1 = product_id_alby_re.findall(User_url)

            for product_id_alby in product_id_alby1:
                User_url_api = 'https://api.a-bly.com/webview/goods/' + str(product_id_alby)

            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")

            result_dict = json.loads(res_api.text)

            try:
                Lower_price_key = result_dict['goods']['representative_option']['member_level_price']
            except:
                try:
                    Lower_price_key = result_dict['goods']['representative_option']['price']
                except:
                    Lower_price_key = result_dict['goods']['representative_option']['original_price']

        # 지그재그
        elif Distributor_key in ['zigzag']:

            # product_id regex

            product_id_re = re.compile('(?<=p\/)[0-9]+')
            product_id1 = product_id_re.findall(User_url)

            # store url 확인

            for product_id in product_id1:
                User_url_rd = 'https://store.zigzag.kr/catalog/products/' + str(product_id)

            res_rd = requests.get(User_url_rd, timeout=3, headers=headers)

            if res_rd.status_code != 200:
                print("User_url_api 접속 오류입니다")

            # store. zigzag 링크 - js 스크래핑

            soup_rd = BeautifulSoup(res_rd.text, 'html.parser')

            script_rd = soup_rd.select_one('#__NEXT_DATA__')
            script_rd = script_rd.text

            dict_result_rd = json.loads(script_rd)

            Lower_price_key = dict_result_rd['props']['pageProps']['product']['product_price']['final_price']

        # 브랜디
        elif Distributor_key in ['brandi']:

            Lower_price_key = soup.select_one('p.price').text

        # 지마켓
        elif Distributor_key in ['gmarket']:

            Lower_price_key = soup.select_one('strong.price_real').text

        # 올리브영
        elif Distributor_key in ['oliveyoung']:

            Lower_price_key = soup.select_one('span.price-2').text

        # 당근마켓
        elif Distributor_key in ['daangn']:

            Lower_price_key = soup.select_one('#article-price').text

        # 위메프(js_sele)
        elif Distributor_key in ['wemakeprice']:
            script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
            script_text1 = script_re.findall(str(soup))
            script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
            dict_result_script_text = json.loads(script_text)

            try:
                Lower_price_key = dict_result_script_text['prodMain']['sale']['benefitPrice']
            except:
                Lower_price_key = dict_result_script_text['prodMain']['sale']['salePrice']

        # 29CM
        elif Distributor_key in ['29cm']:            
            Lower_price_key = soup.select_one('span.css-4bcxzt.ent7twr4').text

        # CJ온스타일
        elif Distributor_key in ['cjonstyle']:
            product_id_cjon_re = re.compile('(?<=item\/)[0-9]+|(?<=mocode\/)M[0-9]+')
            product_id_cjon1 = product_id_cjon_re.findall(User_url)
            print(product_id_cjon1)

            for product_id_cjon in product_id_cjon1:

                try:
                    User_url_api = 'https://display.cjonstyle.com/c/rest/item/' + str(product_id_cjon) + '/itemInfo.json?channelCode=30001001'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)
                except:
                    User_url_api = 'https://display.cjonstyle.com/c/rest/mocode/' + str(product_id_cjon) + '/mocodeInfo.json?channelCode=30001001'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)
                if res_api.status_code != 200:
                    print("User_url_api 접속 오류입니다")
                print(User_url_api)
                result_dict = json.loads(res_api.text)

                try:
                    Lower_price_key = result_dict['result']['detailInfo']['clpSlPrc']
                except:
                    try:
                        Lower_price_key = result_dict['result']['detailInfo']['slPrc']
                    except:
                        try:
                            Lower_price_key = result_dict['result']['itemSummaryInfo']['clpSlPrc']
                        except:
                            try:
                                Lower_price_key = result_dict['result']['itemSummaryInfo']['salePrice']
                            except:
                                Lower_price_key = result_dict['result']['moCode']['representItem']['itemPriceManager']['salePrice']
        # H 패션몰
        elif Distributor_key in ['hfashionmall']:          
            try:
                Lower_price_key = soup.select_one('#minPrice')['value']
            except:
                try:
                    Lower_price_key = soup.select_one('#maxPrice')['value']
                except:
                    try:
                        Lower_price_key = soup.select_one('p.coupon > span.num').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('div.item-price > p.price > span').text
                        except:
                            try:
                                Lower_price_key = soup.select_one('meta[property="recopick:price"]')['content']
                            except:
                                Lower_price_key = soup.select_one('input#lastSalePrc')['value']
        # ikea
        elif Distributor_key in ['ikea']:       
            product_id_ikea_re = re.compile('[0-9]{7,}')
            product_id_ikea1 = product_id_ikea_re.findall(User_url)

            product_id_ikea = product_id_ikea1[0]
            product_id_ikea_back_threedigits = product_id_ikea[-3:]

            try:
                User_url_api = 'https://www.ikea.com/kr/ko/products/'+ str(product_id_ikea_back_threedigits) + '/' + str(product_id_ikea) + '.json'
                print(User_url_api)

                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                result_dict = json.loads(res_api.text)

                Lower_price_key = result_dict['priceNumeral']
            except:
                try:
                    Lower_price_key = result_dict['price']
                except:
                    try:
                        Lower_price_key = result_dict['revampPrice']['integer']
                    except:
                        Lower_price_key = soup.select_one('.pip-price__integer').text

        elif Distributor_key in ['kcar']:  
            try:
                Lower_price_key = soup.select_one('input#sell_price')['value']
            except:
                try:
                    Lower_price_key = soup.select_one('div.car_price_info span').text
                except:
                    Lower_price_key = Lower_price_key
                    
        elif Distributor_key in ['kbchachacha']:  
            try:
                Lower_price_key = soup.select_one('strong.cost-highlight').text
            except:
                try:
                    Lower_price_key = soup.select_one('div.car-intro__cost.ui-inview').text
                except:
                    Lower_price_key = Lower_price_key
                    
        elif Distributor_key in ['lfmall']:  
            try:
                Lower_price_key = soup.select_one('span.current_price').text
            except:
                try:
                    product_id_lfmall_re = re.compile('(?<=PROD_CD=)[0-9A-Z]+')

                    product_id_lfmall1 = product_id_lfmall_re.findall(User_url)

                    for product_id_lfmall in product_id_lfmall1:
                        User_url_api = 'https://mapi.lfmall.co.kr/api/products/detail/detailOptionItems?productId=' + str(product_id_lfmall)

                    res_api = requests.get(User_url_api, timeout=5, headers = headers) 
                    print(User_url_api)
                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)

                    Lower_price_key = int(result_dict['results']['productDetailOption']['productDetailOptionItems'][0]['salePrice'])
                except:
                    Lower_price_key = Lower_price_key
                    
        elif Distributor_key in ['nsmall']: 
            try:
                Lower_price_key = dict_post_api['msg']['goods'][0]['info']['orginSalePrice']
            except:
                try:
                    Lower_price_key = dict_post_api['msg']['goods'][0]['info']['salePrice']
                except:
                    try:
                        Lower_price_key = dict_post_api['msg']['goods'][0]['info']['applyPrice']
                    except:
                        Lower_price_key = Lower_price_key
                        
        elif Distributor_key in ['sivillage']: 
            try:
                Lower_price_key = soup.select_one('div.detail__info-price-current.subsc_unchk').text
            except:
                try:
                    Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                except:
                    try:
                        sv_price_re = re.compile('(?<=\'price\':)(.*?)(?=,)')
                        Lower_price_key = sv_price_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
                        
        elif Distributor_key in ['ssfshop']: 
            try:
                Lower_price_key = soup.select_one('form#goodsForm input[name="lastSalePrc"]')['value']
            except:
                try:
                    Lower_price_key = soup.select_one('#godPrice').text
                except:
                    try:
                        Lower_price_key_re = re.compile('(?<=,salePrice: ).+')
                        Lower_price_key = Lower_price_key_re.findall(str(soup))[0]      
                    except:
                        try:
                            Lower_price_key = soup.select_one('p.prd-price span.current').text
                        except:
                            Lower_price_key = Lower_price_key
                        
        elif Distributor_key in ['ssg']: 
            # final url 잡기
            try:
                ssg_itemId__re = re.compile('(?<=temId%3D)(.*?)(?=%)')
                ssg_itemId = ssg_itemId__re.findall(User_url)[0]
                User_url = 'https://www.ssg.com/item/dealItemView.ssg?itemId=' + ssg_itemId
            except:
                User_url = User_url

            print("SSG final URL은? ", User_url)
            
            headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
            res = requests.get(User_url, headers=headers) 
            print(res.status_code)
            
            soup = BeautifulSoup(res.content, 'html.parser')
            
            try:
                Lower_price_key = soup.select_one('em.ssg_price').text
            except:
                try:
                    price_re = re.compile('(?<=price = ).+(?=)')
                    Lower_price_key = price_re.findall(str(soup))[0]
                except:
                    try:
                        price_re = re.compile('(?<=\'value\': ).+(?=,)')
                        Lower_price_key = price_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
            
        # Hosting 주요 3개사 지정

        else:
            try:
                # cafe24
                Lower_price_key = soup.select_one('#span_product_price_text').text
            except:
                try:
                    # NHN커머스
                    Lower_price_key = soup.select_one(
                        '#frmView > div > div > div.item_detail_list > dl.item_price').text
                except:
                    try:
                        # 코리아센터
                        Lower_price_key = soup.select_one('span.price').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('.price').text
                        except:
                            Lower_price_key = soup.select_one('span.priceArea_price__ombaK.active').text

    except:
        # 기본 bs 최저가 크롤링 설정
        Lower_price_key = "해당 링크에서 직접 보기"   
    
    # Lower_price_key 전처리
    print("Lower_price_key 전처리 전 값은? ", Lower_price_key)
    Lower_price_key = str(Lower_price_key).strip()
    Lower_price_key = Lower_price_key.replace("만원", "00000").replace("만 원", "00000")

    Lower_price_key = re.sub(r'([^0-9]*?)', '', Lower_price_key)

    if Lower_price_key == "":
        Lower_price_key = "확인 불가"

    else:
        Lower_price_key = int(Lower_price_key)

    Lower_price.append(Lower_price_key)

    print('Lower_price 리스트 값은, ', Lower_price)

    # 네이버 쇼핑 값일 경우 최저몰도 함께 출력

    if 'naver.com' in User_url and Type == '쇼핑':

        Lower_mall.append(Lower_mall_key)
        print('Lower_mall 리스트 값은, ' , Lower_mall)
        
#no_searched 셋팅(Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓))

    no_searched_keywords = ['car', 'land']   
    if Lower_price_key != "확인 불가" and any(no_searched_keyword in User_url for no_searched_keyword in no_searched_keywords) == False:

        print("Title_key값은 ", Title_key)

    # 설명 7번
        #title pre / post 처리 후 네이버쇼핑 최저가 검색 후 searched 값 도출

        # Title 전후처리

        # 전처리

        #패턴 1차: 대,일반 괄호(사이 한글 및 숫자 ,./포함) or |뒷문자(한글 및 숫자 ,./ 포함) 제거
        try:
            Title_pre_key = re.sub(r'\[[가-힣0-9%-,\. \/]*?\]|\(([가-힣0-9%-,\. \/]*?)\)|\|([가-힣0-9%-,\. \/]*?)', '', Title_key)
            print("1차, ", Title_pre_key)
            
        #패턴 2차: Disrtibutor_Kor 값 / 문자, 숫자, 한글이 아닌 값이 있는 경우 이를 제거 

            Title_pre_key = re.sub(Distributor_keyword_list_Kor_dict[Distributor_key],'',Title_pre_key)
            Title_pre_key = re.sub('[^\w가-힣 ]','',Title_pre_key)
            print("2차, ", Title_pre_key)

        #패턴 3차: 필요없는 값 제거 
        
            title_trash_words = ['중고거래', '미당첨시', '자동환불', '쇼핑', '감도 깊은 취향 셀렉트샵', '깜짝특가', '사은품', 
                                 'CJ런칭', '단하루', '핫딜', 'upto50', '신상출시', '단독기획']
            for title_trash_word in title_trash_words:
                Title_pre_key = Title_pre_key.replace(title_trash_word, "")
            print("3차, ", Title_pre_key)

            # regex로 Title_key 다 날릴 경우 대비

            if len(Title_pre_key.strip()) == 0:
                Title_pre_key = Title_key

        except:
            Title_pre_key = Title_key

        print("Title_pre_key는 ", Title_pre_key)

        # 후처리: 제품번호 추출

        #패턴 2차: 영문 및 숫자로 이루어진 최소 6자리 제품번호 추출
    #~220713         pattern2 = re.compile("[A-Za-z\d\/]+[A-Za-z][a-zA-Z\d]{2}[a-zA-Z\d]+|[A-Za-z\d/]+[\d][a-zA-Z\d]{2}[A-Za-z][A-Za-z\d/]+") 
#~220718         pattern2 = re.compile("((?=\S[A-Z])(?=\S*?[A-Z])(?=\S*?[0-9]).{6,})\S$|((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$") 
        pattern2 = re.compile('''(((?=[A-Z])(?=[A-Za-z0-9]*?[A-Z])(?=[A-Za-z0-9]*?[0-9])[A-Za-z0-9]{6,})|
        ((?=[a-z])(?=[A-Za-z0-9]*?[a-z])(?=[A-Za-z0-9]*?[0-9])[A-Za-z0-9]{6,}))''')
        try:
            Title_post_key = pattern2.search(Title_pre_key).group()

            if Title_pre_key == Title_key:
                Title_chosen_key = Title_post_key
            else:
                if len(Title_pre_key) >= len(Title_post_key):
                    Title_chosen_key = Title_post_key
                else:
                    Title_chosen_key = Title_pre_key

        except:
            Title_chosen_key = Title_pre_key
        finally:
            if (re.search('[0-9]m|[0-9] ml', Title_chosen_key)) != None:
                Title_chosen_key = Title_pre_key    

        print("Title_chosen_key는, ", Title_chosen_key)
    # 설명 8번
        # Title_chosen_key 없을 경우, 탈출

        if Title_chosen_key == "해당 링크에서 직접 보기":

            Title_searched_key = "조금 더 찾아봐야해요!"
            Lower_price_searched_key = "조금 더 찾아봐야해요!"
            Lower_mall_searched_key = "조금 더 찾아봐야해요!"
            Lower_url_searched_key = "조금 더 찾아봐야해요!"

            Title_searched.append(Title_searched_key)
            Lower_price_searched.append(Lower_price_searched_key)
            Lower_mall_searched.append(Lower_mall_searched_key)
            Lower_url_searched.append(Lower_url_searched_key)

            print("Title_searched는 ", Title_searched)
            print("Lower_price_searched는 ", Lower_price_searched)
            print("Lower_mall_searched는 ", Lower_mall_searched)
            print("Lower_url_searched는 ", Lower_url_searched)

        # Title_chosen_key 있을 경우 최저가 검색 로직 구현
        else:

            #최저가 검색: Title_pre or Title_post 를 활용하여 네이버 쇼핑 1순위(광고 제외) 검색 후 타이틀, 최저가, 최저가몰, URL 추출

            User_url_api = 'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query=' + str(Title_chosen_key) + '&origQuery=' + str(Title_chosen_key)+ '&iq=&eq=&xq='

            print(User_url_api)
            headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
    #         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 

            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")

            res_api_json = json.loads(res_api.text)
    # 설명 9번
            #meta값
            try:
                Title_searched_key = res_api_json['shoppingResult']['products'][0]['productTitle']
            except:
                Title_searched_key = "조금 더 찾아봐야해요!"
            try:
                Lower_price_searched_key = res_api_json['shoppingResult']['products'][0]['mobileLowPrice'] 
            except:
                Lower_price_searched_key = "조금 더 찾아봐야해요!"
            try:
                Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['lowMallList'][0]['name']
            except:
                try:
                    Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['mallName']
                except:
                    Lower_mall_searched_key = "조금 더 찾아봐야해요!"
            try:
                Lower_url_searched_key = res_api_json['shoppingResult']['products'][0]['crUrl']
            except:
                Lower_url_searched_key = "조금 더 찾아봐야해요!"

            print("네이버 쇼핑 최저가는, ", Lower_price_searched_key)

        Title_searched.append(Title_searched_key)

        # Lower_price_searched_key 전처리

        Lower_price_searched_key = str(Lower_price_searched_key).strip()

        Lower_price_searched_key = re.sub(r'([^0-9]*?)', '', Lower_price_searched_key)

        if Lower_price_searched_key == "":

            Lower_price_searched_key = "조금 더 찾아봐야해요!"

        else:        
            Lower_price_searched_key = int(Lower_price_searched_key)   

        # price 비교: 둘 다 int 이며 0이 아닐 경우 시행

        if type(Lower_price_key) and type(Lower_price_searched_key) == int:

            try: 
                if Lower_price_key < Lower_price_searched_key and Lower_price_key & Lower_price_searched_key != 0:
                    Lower_price_searched_key = Lower_price_key
                    Lower_mall_searched_key = Distributor_key
                    Lower_url_searched_key = User_url
            except:
                print("가격 비교 불가")

        Lower_price_searched.append(Lower_price_searched_key)
        Lower_mall_searched.append(Lower_mall_searched_key)
        Lower_url_searched.append(Lower_url_searched_key)

        print("Title_searched는 ", Title_searched)
        print("Lower_price_searched는 ", Lower_price_searched)
        print("Lower_mall_searched는 ", Lower_mall_searched)
        print("Lower_url_searched는 ", Lower_url_searched)

print("scraping complete")

# 설명 10번

# 라니 오픈
# DB_input

all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched


for list_one in all_list:
    if len(list_one) == 0:
        list_one.append("no_data")

all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId)

sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"

cur.execute(sql, all_list_tuple)

db.commit()
print("load complete")

db.close()


# # 라니 클로즈 (제이 오픈)

# # DB_input

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched

# for list_one in all_list:
#     if len(list_one) == 0:
#         list_one.append("no_data")

# #DB 주의사항: all_list_tuple과 sql의 'INSERT INTO post ( 컬럼 )'의 인자들 순서를 동일하게 설정해야 함 (DB 내 칼럼 순서와 일치하지 않아도 됨)
# #다만, DB의 칼럼과 칼럼 명이 다르거나, DB에 칼럼을 새로 생성한다면, all_list_tuple과 sql에도 해당 인자를 추가해야 함

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched)

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


# cur.execute(sql, all_list_tuple)

# db.commit() 
# print("save complete")

# db.close()


# In[ ]:




