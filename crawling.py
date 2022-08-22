#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''220822 ver1.12 / chromedriver 경로 = aws

              수정) 1. 달러 환율 적용
                    2. 크롤링 추가
                    3. 최저가/네이버검색최저가 로직 수정
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
import sys
from urllib import parse
import http.client #라니 이거 설치!
http.client._MAXHEADERS = 1000
from user_agent import generate_user_agent, generate_navigator #라니 이거 설치
# import random # 아이피 우회 시 사용 예정

# data - mysql DB 접속 #라니 오픈
try:
    db = pymysql.connect(host="moum3.cjk00gposwcb.ap-northeast-2.rds.amazonaws.com", user='admin', password='fnucni1234!', db='moum', charset='utf8mb4')
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
crawl_Content = []
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
# 파이썬 실행시 파라미터로 url 받도록 수정
User_url = sys.argv[1]
# # 파이썬 실행시 파라미터로 user id 받도록 수정
UserId = sys.argv[2]


# # 제이 오픈, 라니 클로즈
# # UserId = "test"
# User_url = input("???")

#설명 1번

#url accessibility check

#개인 헤더값
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
#FB 헤더값
headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

#url format check
try:
    User_url = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+#:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', User_url)[0]
    res = requests.get(User_url, timeout=5, headers = headers) 
    print('facebook 헤더로 접속 완료')
except:
    try:
        headers = {'user-agent': generate_user_agent(device_type='smartphone')}
        print("헤더값 fb -> 랜덤 변경")
        res = requests.get(User_url, timeout=5, headers = headers) 
        print("헤더값 fb -> 개인 변경, 접속 완료!")
    except:
        try:
            print("개인 UA 헤더 설정") 
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            res = requests.get(User_url, timeout=5, headers = headers) 
            print("헤더값 변경 완료 ", res.status_code)
        except:#headers = 랜덤으로도 접속 불가
            print("접속 불가")
            User_url = User_url  
# except: #url 형식이 잘 못 되었을 경우 비동기방식으로 사용 (현재 함께 사용하기엔 시간소요가 너무 큼)
#     if 'https://' in User_url:
#         try:            
#             User_url = 'http://' + User_url.replace('https://', '').replace('http://', '')
#             res = requests.get(User_url, timeout=2, headers = headers) 
#             print('User_url에 http 추가')
#         except:
#             User_url = User_url
#             print('http 포맷 체크 못함')
#     elif 'http://' in User_url:
#         try:
#             User_url = 'https://' + User_url.replace('https://', '').replace('http://', '')
#             res = requests.get(User_url, timeout=2, headers = headers) 
#             print('User_url에 https 추가')
#         except:
#             User_url = User_url
#             print('https 포맷 체크 못함')                            
#     else:
#         try:
#             User_url = 'https://' + User_url.replace('https://', '').replace('http://', '')
#             res = requests.get(User_url, timeout=2, headers = headers) 
#             print('https 새로 추가 완료')
#         except:
#             try:
#                 User_url = 'http://' + User_url.replace('https://', '').replace('http://', '')
#                 res = requests.get(User_url, timeout=2, headers = headers) 
#                 print('http 새로 추가 완료')
#             except:
#                 User_url = User_url
#                 print('포맷 체크 못함')    
                    
# finally:#접속이 안될 경우(!= 200) 헤더값 변경
#     try:
#         res = requests.get(User_url, timeout=4, headers = headers)  
#     except: #headers or ip로 인한 접속 불가
#         try: #접속 자체가 불가능했던 경우
#             print("헤더값 변경 fb to my")
#             headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
#             print("헤더값 변경 완료 ", res.status_code)
#         except: #headers = fb으로도 접속 불가
#             try:
#                 print("랜덤 UA 설정") 
#                 headers = {'user-agent': generate_user_agent(device_type='smartphone')}
#                 res = requests.get(User_url, timeout=4, headers = headers) 
#                 print("헤더값 변경 완료 ", res.status_code)
#             except:#headers = 랜덤으로도 접속 불가
#                 print("접속 불가")
#                 User_url = User_url            

# Naver mobile url 임의 변경

if 'msearch' in User_url:

    User_url = User_url.replace("https://msearch", "https://search")

# url redirection 잡기

if 'skyscanner' not in User_url: 
    try:
        with urllib.request.urlopen(User_url, timeout = 3) as response:
            User_url_red = response.geturl()
            if 'no-access' in User_url_red:
                User_url = User_url
            else:
                User_url = User_url_red
            res = requests.get(User_url, timeout=2, headers = headers) 
            print("Redirection된 URL은, ", User_url)        
    except:    
        User_url = User_url
        print("No Redirection된 URL은, ", User_url) 

# naver 앱 url(shorten and redirection and decode)
if 'link.naver.com' in User_url:
    try:
        User_url_decoded = parse.unquote(User_url)
    #     print("User_url_decoded URL은, ", User_url_decoded) 

        User_url_decoded_re = re.compile('(?<=bridge\?url\=)(.*?)(?=\&dst)')

        User_url_decoded_red1 = User_url_decoded_re.findall(User_url_decoded)

        for User_url_decoded_red in User_url_decoded_red1:
            User_url = User_url_decoded_red

            print("link.naver의 redirection은", User_url)
    except:
        User_url = User_url
        print("No link.naver의 redirection은 URL은, ", User_url) 
               
if 'land.naver' in User_url:
    try:
        User_url = User_url + '?newMobile'
    except:
        User_url = User_url
        
# meta og:url redirection check
if 'hsGateway' in User_url:
    try:
        soup = BeautifulSoup(res.content, 'html.parser')
        meta_user_url = soup.select_one('meta[property="og:url"]')['content']
        print("og:url은? ", meta_user_url)
    except:
        meta_user_url = User_url

    if len(meta_user_url) > 1:
        try:
            User_url = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', meta_user_url)[0]
        except:
            User_url = User_url

if 'balaan' in User_url:
    soup = BeautifulSoup(res.content, 'html.parser')
    User_url_re = re.compile('(?<=replace).+')
    add_url = User_url_re.findall(str(soup))[0].strip("\(\)\" ")
    if '.php' in add_url:
        User_url = 'https://www.balaan.co.kr' + add_url
    else:
        User_url = User_url
        
    print("balaan User_url은?", User_url)

if 'a.co/' in User_url:   
    soup = BeautifulSoup(res.content, 'html.parser')
    try:
        User_url = 'https://www.amazon.com/' + str(soup.select_one('input[name="amzn-r"]')['value'])
    except:
        try:
            User_url = soup.select_one('meta[property="og:url"]')['content']
        except:
            User_url = User_url
    print("amazon user_url", User_url)
        
# url split

User_url_list = re.split('\.|/|\?|&|=', User_url)

print("User_url_list는 ", User_url_list)

# DIstributor 키워드가 2개 이상 들어간 경우를 대비, 0~6번째까지 추출하여 Dstributor_key 와 매칭

User_url_list_Distributor = User_url_list[0:7]

print("User_url_list_Distributor는 ", User_url_list_Distributor)

# 설명 2번

# Distributor keyword input

Distributor_keyword_list = ['naver', 'coupang', '11st', 'tistory', 'daangn', 'instagram', 'musinsa', 'musinsaapp', 'a-bly', 'zigzag', 
                            'brandi', 'gmarket', 'oliveyoung', 'wemakeprice', 'tmon', 'auction', 'gsshop', 'hnsmall', 'cjonstyle', 
                            'joongna', 'joonggonara', 'bunjang', 'facebook', 'velog', 'github', 'youtube', 'tiktok', 'google',
                           'aliexpress', 'amazon', 'ebay', 'interpark', '29cm','mycake', 'hfashionmall', 'ikea', 'kcar', 'wikipedia',
                           'kbchachacha', 'lfmall', 'nsmall', 'sivillage', 'ssfshop', 'ssg', 'gucci', 'cartier', 'nike', 'dabangapp',
                           'wconcept', 'thehandsome', 'dailyhotel', 'netflix', 'nbkorea', 'koreanair', 'dior', 'lotteimall',
                           'louisvuitton', 'myrealtrip', 'homeplus', 'mangoplate', 'mustit', 'moulian', 'balaan', 'burberry',
                           'booking', 'bigo', 'saramin', 'chanel', 'pulmuone', 'seoulstore', 'sonohotelsresorts', 'skyscanner',
                           'stylenoriter', 'styleshare', 'spooncast','socar', 'idus', 'afreecatv', 'amoremall', 'agoda', 'adidas',
                           'karrotmarket', 'aladin', 'flyasiana', 'albamon', 'alba', 'yanolja', 'aboutpet', 'hermes', 'airbnb',
                           'encar', 'goodchoice', 'yes24', 'ohou', '10000recipe', 'innisfree', 'elandmall', 'imvely', 'ysl',
                           'jobkorea', 'jejuair', 'zigbang', 'ggumim', 'tv.kakao', 'story.kakao', 'costco', 'kolonmall', 'cuchenmall',
                           'queenit', 'topten10mall', 'trenbe', 'triple', 'trip.com', 'twitch', 'tving', 'twayair', 'tiffany',
                           'fashionplus', 'pet-friends', 'prada', 'fitpetmall', 'houseapp', 'hiver', 'halfclub', 'hanssem',
                           'hellomarket', 'hmall', 'hogangnono', 'hotels.com', 'hotelscombined', 'boribori']

#Distributor 한글화 ( for Title 전처리 시 Distributor 한글 이름 제외 )

Distributor_keyword_list_Kor_dict = {'naver':'네이버', 'coupang':'쿠팡', '11st':'11번가', 'tistory':'티스토리', 'daangn':'당근마켓',
                                     'karrotmarket':'당근마켓', 'instagram':'인스타그램', 'musinsa':'무신사', 'musinsaapp':'무신사',
                                     'a-bly':'에이블리', 'zigzag':'지그재그', 'brandi':'브랜디', 'gmarket':'지마켓', 'oliveyoung':'올리브영', 'wemakeprice':'위메프', 
                                     'joongna':'중고나라', 'joonggonara':'중고나라', 'bunjang':'번개장터', 'facebook':'페이스북',
                                     'velog':'velog', 'github':'github', 'youtube':'유튜브', 'tiktok':'tictok', 'google':'google',
                                     'aliexpress':'aliexpress', 'amazon':'amazon', 'ebay':'ebay', 'interpark':'인터파크', '29cm':'29CM',
                                    'mycake':'Cake', 'hfashionmall':'H 패션몰','ikea':'IKEA', 'kcar':'kcar', 'wikipedia':'위키백과',
                                    'kbchachacha':'KB차차차', 'lfmall':'LF몰', 'nsmall':'NS홈쇼핑', 'sivillage':'S.I.VILLAGE',
                                    'ssfshop':"삼성물산 온라인몰 SSF Shop", 'ssg':'SSG.COM', 'gucci':'구찌® 코리아', 'cartier':'Cartier',
                                    'nike':'나이키', 'dabangapp':'다방','wconcept':'WCONCEPT', 'thehandsome':'더한섬닷컴', 
                                    'dailyhotel':'데일리호텔', 'netflix':'Netflix', 'nbkorea':'New Balance Korea', 'koreanair':'대한항공',
                                    'dior':'디올', 'lotteimall':'롯데홈쇼핑', 'louisvuitton':'루이 비통', 'myrealtrip':'마이리얼트립',
                                    'homeplus':'홈플러스', 'mangoplate':'망고플레이트', 'mustit':'머스트잇', 'mouliaproduct:price:amountn':'뮬리안',
                                    'balaan':'발란', 'burberry':'Burberry®', 'booking':'부킹닷컴', 'bigo':'비고 라이브',
                                    'saramin':'사람인', 'chanel':'샤넬', 'pulmuone':'풀무원', 'seoulstore':'서울스토어',
                                    'sonohotelsresorts':'소노호텔&리조트', 'skyscanner':'스카이스캐너', 'stylenoriter':'스타일노리터',
                                    'styleshare':'스타일쉐어', 'spooncast':'스푼','socar':'쏘카', 'idus':'아이디어스', 
                                    'afreecatv':'아프리카TV', 'amoremall':'AMORE MALL', 'agoda':'아고다', 'adidas':'아디다스', 
                                    'aladin':'알라딘', 'flyasiana':'아시아나항공', 'albamon':'알바몬', 'alba':'알바천국',
                                    'yanolja':'야놀자', 'aboutpet':'어바웃펫', 'hermes':'에르메스', 'airbnb':'에어비앤비', 'encar':'엔카',
                                    'goodchoice':'여기어때', 'yes24':'YES24', 'ohou':'오늘의집', 'auction':'옥션', '10000recipe':'만개스토어',
                                    'innisfree':'이니스프리', 'elandmall':'이랜드몰', 'imvely':'임블리', 'ysl':'입생로랑',
                                    'jobkorea':'잡코리아', 'jejuair':'제주항공', 'zigbang':'직방', 'ggumim':'집꾸미기', 
                                     'tv.kakao':'카카오TV', 'story.kakao':'카카오스토리', 'costco':'코스트코', 'kolonmall':'코오롱몰',
                                    'cuchenmall':'쿠첸몰', 'queenit':'퀸잇', 'topten10mall':'탑텐몰', 'trenbe':'트렌비', 
                                     'triple':'트리플', 'trip.com':'트립닷컴', 'twitch':'트위치', 'tmon':'티몬', 'tving':'티빙',
                                    'twayair':'티웨이항공', 'tiffany':'티파니앤코', 'fashionplus':'패션플러스', 'pet-friends':'펫프렌즈',
                                    'prada':'프라다', 'fitpetmall':'핏펫몰', 'houseapp':'하우스앱', 'hiver':'하이버', 
                                     'halfclub':'하프클럽', 'hanssem':'한샘몰', 'hellomarket':'헬로마켓', 'hmall':'현대Hmall',
                                    'hogangnono':'호갱노노', 'hotels.com':'호텔스닷컴', 'hotelscombined':'호텔스컴바인',
                                    'hnsmall':'홈앤쇼핑', 'boribori':'보리보리'}

# url - Distributor_keyword list match

# soup 정의 설정
# ua = UserAgent(use_cache_server=True)
try:
    soup = BeautifulSoup(res.content, 'html.parser')
    if len(soup.text.replace("\n","").replace(" ","")) < 150:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        print('soup < 150 에 따라 헤더 개인으로 변경')
        res = requests.get(User_url, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')
        
    Distributor_keyword_match_list = list(
        set(User_url_list_Distributor).intersection(Distributor_keyword_list))
    print("Distributor_keyword_match_list? ", Distributor_keyword_match_list)
    if len(Distributor_keyword_match_list) >= 1:

        Distributor_key = Distributor_keyword_match_list[0]

    else:
        try:
            User_url_Distributor_re = re.compile('(?<=\.)(.*?)(?=\.co|\.net|\.me|\.link|\.tv|\.kr|\.se)')
            Distributor_key = User_url_Distributor_re.findall(User_url)[0]    

            Distributor_key_split_list = re.split('\.|/|\?', Distributor_key)

            Distributor_key_dict = dict()

            for Distributor_key_split in Distributor_key_split_list:
                Distributor_key_split_count_value = str(soup).count(Distributor_key_split)
                Distributor_key_dict[Distributor_key_split] = Distributor_key_split_count_value    

            Distributor_key_max_value = max(Distributor_key_dict.values())
            Distributor_key_dict_reversed= dict(map(reversed, Distributor_key_dict.items()))
            Distributor_key = Distributor_key_dict_reversed[Distributor_key_max_value]
            print("Distributor_key_dict???", Distributor_key_dict)
        except:
            try:
                Distributor_key = soup.select_one('meta[property="og:site_name"]')['content']                 
            except:
                # Distributor_key = soup.select_one('title').get_text() -> 주로 '상품명|사이트명'이라 일단 보류
                Distributor_key = "해당 링크에서 직접 보기"

    Distributor_key_change_dict = {'mycake':'cake', 'dabangapp':'dabang', 'musinsaapp':'musinsa'}

    if Distributor_key in Distributor_key_change_dict.keys():
        Distributor_key =  Distributor_key_change_dict[Distributor_key]    

    liveplayers = ['shoplive','sauceflex', 'sflex']
    for liveplayer in liveplayers:

        if liveplayer in User_url:
            Distributor_in_html_keys = ['musinsa', 'zigzag', 'queenit', 'samsung', 'wconcept', 'wemakeprice', 'hfashionmall', 'kolonmall', 
                                        'thehandsome', 'shinhan', 'thenorthface', 'millie', 'Pulmuone', 'auction']
            for Distributor_in_html_key in Distributor_in_html_keys:
                Distributor_in_html = str(soup).find(Distributor_in_html_key)
                if Distributor_in_html > -1:
                    Distributor_key = Distributor_in_html_key
except:
    try:
        User_url_Distributor_re = re.compile('(?<=\.)(.*?)(?=\.co|.net|.me|.link|.tv)')
        Distributor_key = User_url_Distributor_re.findall(User_url)[0]    
    except:
        Distributor_key = "해당 링크에서 직접 보기"

# 설명 3번

# Category_in_keyword input

Category_in_keyword_list_shopping = ['11st', 'coupang', 'musinsa', 'a-bly', 'zigzag', 'brandi', 'gmarket', 'oliveyoung',
                                     'wemakeprice', 'idus', 'auction', 'gsshop', 'shopping', 'smartstore', 'shop', 
                                     'hnsmall', 'cjonstyle', 'brand.naver', 'store', 'products', 'product', 'wemakeprice', 
                                     'tmon', 'goods', 'aliexpress', 'amazon', 'ebay', 'interpark', '29cm', 'hfashionmall',
                                    'land', 'ikea', 'kcar', 'kbchachacha', 'lfmall', 'nsmall', 'sivillage', 'ssfshop',
                                    'ssg', 'gucci', 'cartier', 'nike','dabangapp', 'wconcept', 'thehandsome', 'shoplive',
                                    'dailyhotel', 'nbkorea', 'koreanair', 'dior', 'lotteimall', 'sflex', 'louisvuitton', 
                                     'myrealtrip', 'homeplus', 'mangoplate', 'eat_deals', 'mustit', 'musinsaapp', 'moulian',
                                    'balaan', 'burberry', 'booking', 'hotel', 'chanel', 'pulmuone', 'seoulstore', 'sonohotelsresorts',
                                    'skyscanner', 'stylenoriter', 'styleshare', 'socar', 'amoremall', 'agoda', 'adidas', 
                                     'ogqmarket', 'productId', 'realty', 'karrotmarket', 'aladin', 'flyasiana', 'yanolja', 'aboutpet',
                                    'hermes', 'airbnb', 'encar', 'goodchoice', 'ohou', 'ProductView', 'innisfree', 'elandmall', 
                                    'imvely', 'ysl', 'jejuair', 'zigbang', 'ggumim', 'costco', 'kolonmall', 'cuchenmall', 'queenit',
                                    'topten10mall', 'trenbe', 'trip.com', 'twayair', 'tiffany', 'fashionplus', 'pet-friends', 'prada',
                                    'fitpetmall', 'houseapp', 'hiver', 'halfclub', 'hanssem', 'hmall', 'hogangnono', 'hotels.com',
                                    'hotelscombined', 'boribori']
Category_in_keyword_list_blog = ['blog', 'tistory', 'velog', 'github', 'contents', 'premium', 'post', '10000recipe', 'mangoplate',
                                'saramin', 'story_articles', 'jobs', 'daangn', 'karrotmarket', 'albamon', 'alba', 'viral', 'jobkorea',
                                'story.kakao', 'triple']
Category_in_keyword_list_sns = ['instagram', 'band', 'facebook']
Category_in_keyword_list_video = ['youtube', 'tiktok', 'tv', 'mycake', 'video', 'netflix', 'bigo', 'afreecatv', 'player', 'bj',
                                 'vods', 'vod', 'tv.kakao', 'twitch', 'tving']
Category_in_keyword_list_second = ['daangn', 'joonggonara', 'joongna', 'bunjang', 'hellomarket']
Category_in_keyword_list_cafe = ['cafe']
Category_in_keyword_list_news = ['news', 'joongang', 'yna', 'weather', 'entertain', 'wikipedia']
Category_in_keyword_list_images = ['.img', '.jpg', '.png', '.jpeg']
Category_in_keyword_list_enter = ['book', 'music', 'music-flo', 'spooncast', 'yes24']
Category_in_keyword_list_map = ['map', 'maps', 'tmap', 'place']

#수동분류 9개 항목
# Category_in_keyword_list_sports
# Category_in_keyword_list_baby
# Category_in_keyword_list_finance
# Category_in_keyword_list_enter
# Category_in_keyword_list_fashion
# Category_in_keyword_list_living
# Category_in_keyword_list_tech
# Category_in_keyword_list_outdoor
# Category_in_keyword_list_society

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

    print("Publisher 리스트 값은 ", Publisher)
    print("수정된 Distributor_key값은? ", Distributor_key)

else:
    print("Distributor_key값은? ", Distributor_key)

# 설명 4번
# Type 파악

if Category_in_key in ['news', 'cafe', 'blog']:
    Type_key = "글"

elif Category_in_key in ['shopping', 'second', 'enter']:
    Type_key = "위시"

elif Category_in_key in ['video']:
    Type_key = "동영상"

elif Category_in_key in ['sns', 'image']:
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

# 기본 bs4 크롤링 설정: headers 값은 상단에서 변경된 경우, 변경된 상태 그대로 유지
# headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

try:
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
        if len(Title_key) < 2 or Title_key == "해당 링크에서 직접 보기" or Title_key == Distributor_keyword_list_Kor_dict[Distributor_key]:
            Title_key_h_tag()
    except:
        if len(Title_key) < 2 or Title_key == "해당 링크에서 직접 보기":
            Title_key_h_tag()    

    if len(Title_key) < 2:
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
            Thumbnail_image_key = soup.select_one('meta[name="og:image"]')['content']
        except:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="twitter:image"]')['content']
            except:
                try:
                    Thumbnail_image_key = soup.select_one('meta[name="twitter:image"]')['content']
                except:
                    try:
                        Thumbnail_image_key = soup.select_one('img')['src']        
                    except:
                        Thumbnail_image_key = "해당 링크에서 직접 보기"
except:
    print("기본 3요소 스크래핑 불가")
    Title_key = "해당 링크에서 직접 보기"
    Description_key = "해당 링크에서 직접 보기"
    Thumbnail_image_key = "해당 링크에서 직접 보기"
    
# Duration_key 설정
if Type_key == '동영상':
    if Distributor_key == "youtube":
        try:
            Duration_key = soup.select_one(
                'meta[itemprop="duration"]')['content']
            Duration_key = Duration_key.replace(
                "PT", "").replace("M", "분 ").replace("S", "초")
        except:
            Duration_key = "해당 링크에서 직접 보기"
    elif Distributor_key == "naver":
        try: # naver.com/vod 
            script_re = re.compile('(?<=vod = ).+(?=;)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)

            Title_key = dict_result_script_text['title']

            Thumbnail_image_key = dict_result_script_text['thumbnail']

            Description_key = dict_result_script_text['searchData']

            try:
                Duration_key = dict_result_script_text['playTime']
            except:
                try:
                    Duration_key = str(dict_result_script_text['playTimeMinute']) + '분' + str(dict_result_script_text['playTimeSecond']) +'초'
                except:
                    try:
                        Duration_key = str(dict_result_script_text['playTimeToSecond']) + '초'
                    except:
                        Duration_key = "해당 링크에서 직접 보기"

        except: # tv.naver.com
            try:
                Duration_key = soup.select_one('em.time').text
            except:
                try:
                    Duration_key = soup.select_one('meta[property="naver:video:play_time"]')['content']
                except:
                    Duration_key = "해당 링크에서 직접 보기"
                    
    elif Distributor_key == "afreecatv":
        try:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))

            Duration_key = dict_result_script_text['duration']
            Duration_key = int(re.sub(r'(\D)', '', Duration_key))
            Duration_key_minute, Duration_key_second= divmod(Duration_key, 60)

            Duration_key = str(Duration_key_minute) + '분 ' + str(Duration_key_second) + '초'
        except:
            Duration_key = "해당 링크에서 직접 보기"
    else:
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
        if 'm.' in User_url:
            User_url = User_url.replace('m.cafe.', 'cafe.')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
#         headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        res = requests.get(User_url, timeout=3, headers=headers) 
        soup = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')

        article_no_re = re.compile('[0-9]{4,}.+')
        article_no = article_no_re.findall(User_url)[0]
        print("article_no", article_no)

        clubid = soup.select_one('input[name="clubid"]')['value']
        print("clubid ", clubid )

        User_url_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/' + str(clubid) + '/articles/' + str(article_no)
        print(User_url_api)

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        #내부 api 
        soup_api = BeautifulSoup(res_api.text, 'html.parser')

        script_api = soup_api.text
        dict_result_script_api = json.loads(script_api)
        print(dict_result_script_api)

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
#                 chromedriver = 'C:/Users/FNUCNI/Desktop/moeum/chromedriver.exe'
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
#                     chromedriver = 'C:/Users/FNUCNI/Desktop/moeum/chromedriver.exe'
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
#                 chromedriver = 'C:/Users/FNUCNI/Desktop/moeum/chromedriver.exe'
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
        #header 값을 fb로 잡아야 무한로딩 우회
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
        try:
            script_re = re.compile('(?<=groupLayerItems = ).+(?=;)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)
        except:
            try:   
                script_re = re.compile('(?<=setOptionLayer\().+(?=, \'vipOptionAreaSub\'\);)')
                script_text = script_re.findall(str(soup))[0]
                dict_result_script_text = json.loads(script_text)       
            except:
                pass
        try:
            Title_key = dict_result_script_text['GoodsInfo']['GoodsName']
        except:
            try:
                Title_key = dict_result_script_text['Order']['GoodsName']
            except:
                try:
                    Title_key = dict_result_script_text['GoodsDetail']['GoodsName']
                except:
                    Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['GoodsInfo']['ImageUrl']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'oliveyoung' in User_url:
        try:
            product_id_olive_re = re.compile('(?<=goodsNo\=)[\w]+')
            product_id_olive = product_id_olive_re.findall(User_url)[0]
        except:
            product_id_olive_re = re.compile('(?<=sndVal=)[\w]+')
            product_id_olive = product_id_olive_re.findall(User_url)[0]
        User_url_api = 'https://www.oliveyoung.co.kr/store/goods/getGoodsGtmInfoAjaxNew.do?goodsNoArrStr=' + str(product_id_olive) + '&itemNoArrStr=001&positionArrStr=1&giftCardYn=N'
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)[0]

        try:
            Title_key = result_dict['goodsNm']
        except:
            try:
                Title_key = soup.select_one('p.prd_name').get_text()
            except:
                try:
                    Title_key = soup.select_one('h2.contents_header_logo').text 
                except:
                    Title_key = Title_key  
            
        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            try:
                Thumbnail_image_key = soup.select_one('div > #mainImg')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key
        try:
            Description_key = result_dict['dispCatNm']
        except:
            try:
                Description_key = result_dict['stdCatNm']
            except:
                Description_key = Description_key
                
    elif 'wemakeprice' in User_url:
    #설명 5번_selenium    
        # 크롬드라이버 생성
        # 라니 오픈(제이 클로즈)
#         chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
        chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
        #제이 경로
        # #chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥              
#         chromedriver = 'C:/Users/FNUCNI/chromedriver.exe' # 윈도우
#         chromedriver = 'C:/Users/FNUCNI/Desktop/moeum/chromedriver.exe'

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
        #api
        product_id_bunjang_re = re.compile('(?<=products\/)[0-9]+')
        product_id_bunjang = product_id_bunjang_re.findall(User_url)[0]
        User_url_api = 'https://api.bunjang.co.kr/api/1/product/' + str(product_id_bunjang) + '/detail_info.json?version=4'

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)
        
        #js
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
       
        try:
            Title_key = result_dict['item_info']['name']
        except:
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
                
        try:
            Description_key = result_dict['item_info']['description']
        except:
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key
                
        try:
            Thumbnail_image_key = result_dict['item_info']['product_image']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
            
    elif 'cjonstyle' in User_url:
        Title_key_temp = Title_key
        Title_key = Description_key
        Description_key = Title_key_temp       
        
    elif 'kcar' in User_url:
        product_id_kcar_re = re.compile('(?<=CarCd=)(.+)[(?=\&)]?')
        product_id_kcar = product_id_kcar_re.findall(User_url)[0]

        User_url_api = 'https://mapi.kcar.com/bc/car-info-detail?i_sCarCd=' + str(product_id_kcar)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        print("User_url_api", User_url_api)

        soup_api = BeautifulSoup(res_api.text, 'html.parser')
        script_api = soup_api.text
        dict_result_script_api = json.loads(script_api)

        #Title

        try:
            Title_key = dict_result_script_api['data']['rvo']['carWhlNm']
        except:
            try:
                Title_key = dict_result_script_api['data']['rvo']['modelNm']
            except:
                Title_key = Title_key
        #Desc.
        try:
            Description_key = dict_result_script_api['data']['rvo']['simcDesc']
        except:
            try:
                Description_key = dict_result_script_api['data']['rvo']['carDtlDesc']
            except:
                try:
                    Description_key = dict_result_script_api['data']['rvo']['keyPntCnts']
                except:
                    Description_key = Description_key
        # Thumb
        try:
            Thumbnail_image_key = dict_result_script_api['data']['rvo']['elanPath']
        except:
            Thumbnail_image_key = dict_result_script_api['data']['photoList'][0]['elanPath']

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
        soup = BeautifulSoup(res.content,"html.parser")
        dict_post_api = json.loads(soup.text)
        
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
            
    elif '11st' in User_url:
        if 'live11' in User_url:
            try:
                product_id_11st_live = re.sub(r'[^0-9]', '', User_url[-6:]) 
                User_url_api = 'https://live11-vod.11st.co.kr/v1/broadcasts/' + product_id_11st_live + '/vod-info'
                res_api = requests.get(User_url_api, timeout=3, headers=headers) 

                soup_api = BeautifulSoup(res_api.text, 'html.parser')
                dict_result_script_api = json.loads(str(soup_api))
                Title_key = dict_result_script_api['settingInfo']['settings'][0]['title']
                Description_key = dict_result_script_api['settingInfo']['settings'][0]['popupBody']
                Thumbnail_image_key = dict_result_script_api['broadcastInfo']['shareImageUrl']
            except:
                Title_key = Title_key
                Description_key = Description_key
                Thumbnail_image_key = Thumbnail_image_key

    elif 'gsshop' in User_url:
        script_re = re.compile('(?<=renderJson = ).+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace(';', ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['prd']['exposPrdNm']
        except:
            try:
                Title_key = dict_result_script_text['prd']['prdNm']
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['prd']['exposPmoNm']
        except:
            Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['prd']['imgInfo'][0]['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['prd']['prdImgL1']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['prd']['videoImgUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'cartier' in User_url:
        script_re = re.compile('(?<=json">\n).+')
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image'][0]
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'land.naver' in User_url:
        script_re = re.compile('(?<=window.App=)(.*?)(?=<\/script><script src)')
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['state']['article']['article']['articleName']
        except:
            try:
                Title_key = dict_result_script_text['state']['article']['dealerTelInfo']['atclNm']
            except:
                try:
                    Title_key = soup.select_one('strong.header_head_title').text
                except:
                    try:
                        Title_key = soup.select_one('strong.detail_sale_title').text
                    except:
                        Title_key = Title_key

        try:
            Description_key = dict_result_script_text['state']['article']['article']['exposureAddress']
        except:
            try:
                Description_key = dict_result_script_text['state']['article']['location']['detailAddress']
            except:
                try:
                    Description_key = soup.select_one('em.detail_info_branch').text
                except:
                    Description_key = Description_key
                    
    elif Distributor_key in ['naver']:
        naver_shopping_keywords = ['catalog', 'brand', 'store']
        if any(naver_shopping_keyword in User_url for naver_shopping_keyword in naver_shopping_keywords) == True:
            script_re = re.compile('(?<=json">).*(?=<\/script>)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['name']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['catalog_Catalog']['productName']
                except:
                    try:
                        Title_key = dict_result_script_text['props']['pageProps']['catalog']['productName']
                    except:
                        try:
                            Title_key = dict_result_script_text['props']['pageProps']['ogTag']['title']
                        except:
                            Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['ogTag']['image']
                except:
                    Thumbnail_image_key =Thumbnail_image_key

            try:
                Description_key = dict_result_script_text['description']
            except:
                try:
                    Description_key = dict_result_script_text['props']['pageProps']['ogTag']['description']
                except:
                    Description_key = Description_key

    elif 'wconcept' in User_url:
        try:
            script_re = re.compile('(?<=content_name: ).*(?=\,)')
            Title_key = script_re.findall(str(soup))[0]
        except:
            try:
                Title_key = dict_result_script_text['itemName']
            except:
                try:
                    Title_key = soup.select_one('meta[property="og:description"]')['content']
                except:
                    try:
                        Title_key = soup.select_one('span.product_name').text
                    except:
                        try:
                            Title_key = soup.select_one('meta[property="eg:itemName"]')['content']
                        except:
                            try:
                                Title_key = soup.select_one('input#hidItemName')['value']
                            except:
                                Title_key, Description_key = Description_key, Title_key

        try:
            Description_key = soup.select_one('input#hidAddCatFix')['value'].replace("^"," ")
        except:
            Description_key = Description_key                    
                    
    elif 'thehandsome' in User_url:
        try:  
            script_re = re.compile('(?<=productName :).*(?=\,)')
            Title_key = script_re.findall(str(soup))[0]   
        except:
            try:
                Title_key = soup.select_one('meta[property="og:title"]')['content']
            except:
                try:
                    Title_key = soup.select_one('meta[property="recopick:title"]')['content']
                except:
                    Title_key = Title_key

        try:
            Description_key = soup.select_one('div.prod-detail-con-box').text
        except:
            Description_key = Description_key

        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="recopick:image"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key                

    elif 'dailyhotel' in User_url:

        try:
            product_id_re = re.compile('(?<=stays\/)[0-9]{2,10}[(?=?)]?')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v9/hotel/' + product_id            
        except:
            product_id_re = re.compile('(?<=activity\/)[0-9]{2,10}[(?=?)]?')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v1/activity/deals/' + product_id            

        print(User_url_api)
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)

        try:
            Title_key = result_dict['data']['name']
        except:
            try:
                Title_key = result_dict['data']['title']
            except:               
                try:
                    Title_key = soup.select_one('title').text
                except:
                    try:
                        Title_key = soup.select_one('div.detail-title').text
                    except:
                        Title_key = Title_key
                        
        try:
            Description_key = result_dict['data']['address']
        except:
            try:
                Description_key = result_dict['data']['details'][0]['contents'][0]
            except:
                try:
                    Description_key = result_dict['data']['storeInfo']['address']
                except:
                    try:
                        Description_key = soup.select_one('p.comment').text
                    except:
                        try:
                            Description_key = soup.select_one('ul.lists').text
                        except:
                            Description_key = Description_key        
                                
        try:
            Thumbnail_image_key = result_dict['data']['images'][-1]['url']
        except:
            try:
                Thumbnail_image_key = result_dict['data']['basicImages'][0]['imagePath']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'dior' in User_url:
        try:
            script_re = re.compile('(?<=description\"\/><script type=\"application\/ld\+json\">).*(?=<\/script><link as)')
            script_text = script_re.findall(str(soup))[0].strip()
            dict_result_script_text = json.loads(script_text)
        except:
            try:
                script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/main>)', re.DOTALL)
                script_text = script_re.findall(str(soup))[0].replace("</script>", "").strip()
                dict_result_script_text = json.loads(script_text)        
            except:
                try:
                    script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/script><link rel)')
                    script_text = script_re.findall(str(soup))[0].strip()
                    dict_result_script_text = json.loads(script_text)
                except:
                    try:
                        script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/script>)', re.DOTALL)
                        script_text = script_re.findall(str(soup))[0].strip()
                        dict_result_script_text = json.loads(script_text)       
                    except:
                        script_re = re.compile('(?<=var meta = ).*(?=;)')
                        script_text = script_re.findall(str(soup))[0].strip()
                        dict_result_script_text = json.loads(script_text)
        try:
            Title_key = dict_result_script_text['name']
        except:
            try:
                Title_key = dict_result_script_text['product']['variants'][0]['name']
            except:
                Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            try:
                Description_key = dict_result_script_text['product']['type']
            except:
                Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['image'][0]
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'myrealtrip' in User_url:
        script_bs = soup.select_one('script[data-component-name="Offer"]').text
        dict_result_script_text = json.loads(str(script_bs))   

        try:
            Title_key = dict_result_script_text['offerInfo']['title']
        except:
            try:
                Title_key = soup.select_one('div.loading_title').text
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['offerInfo']['subtitle']
        except:
            try:
                Description_key = dict_result_script_text['offerInfo']['introduction']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['photos'][0]
        except:
            try:
                Thumbnail_image_key = 'https://d2yoing0loi5gh.cloudfront.net/assets/og-image-35b4b66874396ae2fc8991b926c1f0c09f27f25f9c0a23f15e5e96c73c2c9992.png' #마이리얼트립 디폴트 이미지'
            except:
                Thumbnail_image_key =Thumbnail_image_key
                
    elif 'homeplus' in User_url:
        if 'my' in User_url:
            try:
                Title_key = soup.select_one('h2.visual_tit').get_text()
            except:
                try: 
                    Title_key = soup.select_one('p.title').text
                except:
                    Title_key = Title_key          
            
            try:
                Thumbnail_image_key = soup.select_one('div.digigtal_visual_cont img')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key        
            
        else:
            script_text = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(script_text)
            try:
                Title_key = dict_result_script_text['@graph'][0]['name']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['@graph'][0]['description']
            except:
                Description_key = Description_key 

    elif 'kurly' in User_url:
        script_text = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['name']
        except:
            try:
                Title_key = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['masterProductName']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['product']['name']
                except:
                    Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['mainImageUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['shareImageUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['originalImageUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key
                    
    elif 'mangoplate' in User_url:
        script_text = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(script_text)
        try:
            Title_key = dict_result_script_text['title']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['picture_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'moulian' in User_url:
        Thumbnail_image_key = 'http://www.moulian.com' + soup.select_one('div.img > img')['src']

    elif 'balaan' in User_url:
        product_id_balaan_re = re.compile('(?<=goodsno=)[0-9]+')
        product_id_balaan = product_id_balaan_re.findall(User_url)[0]
        User_url_api = 'https://api.balaan.co.kr/v1/goods/recent?goodsnoString=' + str(product_id_balaan)
        print('User_url_api??', User_url_api)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)
        try:
            Title_key = result_dict['data'][product_id_balaan]['goodsnm']
        except:
            try:
                Title_key = result_dict['data'][product_id_balaan]['origin']
            except:
                Title_key = Title_key
        try:
            Thumbnail_image_key = result_dict['data'][product_id_balaan]['img_i']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'burberry' in User_url:            
        script_re = re.compile('(?<=PRELOADED_STATE__ = ).+(?=;)', re.DOTALL)
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)
        
        product_id_re = re.compile('(?<=burberry.com).+')
        product_id = product_id_re.findall(User_url)[0]  
        try:
            Title_key = dict_result_script_text['db']['pages'][product_id]['data']['name']
        except:
            try:
                Title_key = dict_result_script_text['db']['pages'][product_id]['data']['content']['title']
            except:
                try:
                    Title_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['name']
                except:
                    Title_key = Title_key

        try:
            Description_key = dict_result_script_text['db']['pages'][product_id]['data']['content']['description']
        except:
            try:
                Description_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['description']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['db']['pages'][product_id]['data']['galleryItems'][0]['image']['imageDefault']
        except:
            try:
                Thumbnail_image_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'brandi' in User_url:  
        script = soup.select_one('script[type="text/javascript"]').text.replace('window.__INITIAL_STATE__ = ','').replace('window.__IS_INITIAL_STATE__ = true;','').replace(';','').strip()
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['product']['product']['name']
        except:
             Title_key =Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['product']['product']['image_thumbnail_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'chanel' in User_url:  
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script= json.loads(str(script))

        try:
            Title_key = dict_result_script['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script['image']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'pulmuone' in User_url: 
        product_id_pulmuone_re = re.compile('(?<=goods=)[0-9]+')
        product_id_pulmuone = product_id_pulmuone_re.findall(User_url)[0]
        User_url_pulmuone_api = 'https://shop.pulmuone.co.kr/goods/goods/getGoodsPageInfo'

        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Host': 'shop.pulmuone.co.kr',
        'Connection': 'alive',
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
        'ilGoodsId': product_id_pulmuone #product_id
        # 'cocd': '110',
        # 'imgSizeType': 'Q',
        # 'accptPath': '500',
        # 'accptPathCd': '500',
        # 'req_co_cd': '110',
        # 'userId': '',
        # 'catalogId': '97001'
        }

        res = requests.post(User_url_pulmuone_api, headers=headers, data =  payload, timeout = 10) 
        soup = BeautifulSoup(res.content,"html.parser")
        dict_post_api = json.loads(soup.text)
        
        try:
            Title_key = dict_post_api['data']['goodsName']
        except:
            try:
                Title_key = soup.select_one('meta[property="og:description"]')['content']
            except:
                Title_key = Title_key
        try:
            Description_key = dict_post_api['data']['goodsDesc']
        except:
            try:
                Description_key = soup.select_one('meta[name="keywords"]')['content']
            except:
                Description_key = Description_key
                
        try:
            Thumbnail_image_key = 'https://s.pulmuone.app/' + dict_post_api['data']['goodsImage'][0]['bigImage']        
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'seoulstore' in User_url:
        if 'articles' in User_url:
            product_id_seoulstore_re = re.compile('(?<=articles\/)[0-9]+')
            product_id_seoulstore = product_id_seoulstore_re.findall(User_url)[0]
            User_url_seoulstore_api = 'https://www.seoulstore.com/api/do/getArticle'

            headers = {
            'authority': 'www.seoulstore.com',
            'method': 'POST',
            'path': '/api/do/getArticle',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '41',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'cookie': 'uuid=9f1c4af0-1154-11ed-a610-45e0413e2e4e; _fbp=fb.1.1659329068402.1133576827; _dtrBrwsId=HYQP5czGL3Z6rTLH1X_zj; _ga=GA1.2.1520780270.1659329069; _gid=GA1.2.415129831.1660038801; _pk_ref.10003.bfc8=%5B%22%22%2C%22%22%2C1660095550%2C%22http%3A%2F%2Flocalhost%3A8888%2F%22%5D; _pk_ses.10003.bfc8=1; cto_bundle=jm7fnF96dWUxJTJGYUdXQ0tFTUgzYVRJV1huYlZnQ1NFcWNMVmFmNWdPJTJGUXB1dGpWV1A3bTFXNUw5SXBlYVdnTU4wR3E0Z2pGQ1M1YnJkVUN2QnBPTnNDelNNRjFoWGpKYWpEVk1hMjh5YTl1eHpEWHoxOE1NT3dNNDVEdWZiSG5Pd25JTk1GdHcydEhqWW84UVRVdkpFUDR5dERRJTNEJTNE; _dc_gtm_UA-61220221-4=1; _pk_id.10003.bfc8=e642d31d9f3920dd.1659329068.4.1660095957.1660095550.; wcs_bt=s_2d9af6c410c4:1660095957',
            'origin': 'https://www.seoulstore.com',
            'referer': 'https://www.seoulstore.com/articles/' + str(product_id_seoulstore) + '/news',
        #     'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
            }
            payload = {
            'id': product_id_seoulstore, #product_id
            'method': 'getArticle'
            }
            res = requests.post(User_url_seoulstore_api, headers=headers, data =  payload, timeout = 10) 
            soup = BeautifulSoup(res.content,"html.parser")
            dict_post_api = json.loads(soup.text)
            

            try:
                Title_key = dict_post_api['subject']
            except:
                Title_key = Title_key
            
            try:
                Thumbnail_image_key = dict_post_api['boardFile'][0]
            except:
                Thumbnail_image_key = Thumbnail_image_key
        
        
        else:
            product_id_seoulstore_re = re.compile('(?<=products\/)[0-9]+')
            product_id_seoulstore = product_id_seoulstore_re.findall(User_url)[0]
            User_url_seoulstore_api = 'https://www.seoulstore.com/api/do/getProduct'

            headers = {
            'authority': 'www.seoulstore.com',
            'method': 'POST',
            'path': '/api/do/getProduct',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '41',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'cookie': 'uuid=9f1c4af0-1154-11ed-a610-45e0413e2e4e; _fbp=fb.1.1659329068402.1133576827; _dtrBrwsId=HYQP5czGL3Z6rTLH1X_zj; _ga=GA1.2.1520780270.1659329069; _gid=GA1.2.415129831.1660038801; _pk_ref.10003.bfc8=%5B%22%22%2C%22%22%2C1660095550%2C%22http%3A%2F%2Flocalhost%3A8888%2F%22%5D; _pk_ses.10003.bfc8=1; cto_bundle=jm7fnF96dWUxJTJGYUdXQ0tFTUgzYVRJV1huYlZnQ1NFcWNMVmFmNWdPJTJGUXB1dGpWV1A3bTFXNUw5SXBlYVdnTU4wR3E0Z2pGQ1M1YnJkVUN2QnBPTnNDelNNRjFoWGpKYWpEVk1hMjh5YTl1eHpEWHoxOE1NT3dNNDVEdWZiSG5Pd25JTk1GdHcydEhqWW84UVRVdkpFUDR5dERRJTNEJTNE; _dc_gtm_UA-61220221-4=1; _pk_id.10003.bfc8=e642d31d9f3920dd.1659329068.4.1660095957.1660095550.; wcs_bt=s_2d9af6c410c4:1660095957',
            'origin': 'https://www.seoulstore.com',
            'referer': 'https://www.seoulstore.com/products/' + str(product_id_seoulstore) + '/detail?ecommerceListName=ranking_all',
        #     'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
            }
            payload = {
            'id': product_id_seoulstore, #product_id
            'method': 'getProduct'
            }
            res = requests.post(User_url_seoulstore_api, headers=headers, data =  payload, timeout = 10) 
            soup = BeautifulSoup(res.content,"html.parser")
            dict_post_api = json.loads(soup.text)



            try:
                Title_key = dict_post_api['descriptions']['name']
            except:
                try:
                    Title_key = dict_post_api['name']
                except:
                    Title_key = Title_key
            try:
                Description_key = dict_post_api['siteProductTags'][0]
            except:
                try:
                    Description_key = dict_post_api['channelName']
                except:
                    Description_key = Description_key
            try:
                Thumbnail_image_key = dict_post_api['images']['add'][0]
            except:
                try:
                    Thumbnail_image_key = dict_post_api['images']['list']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'skyscanner' in User_url:
        try: # 호텔
            Thumbnail_image_key = soup.select_one('link[as="image"]')['href']
        except:
            Thumbnail_image_key = 'https://www.skyscanner.co.kr/sttc/blackbird/opengraph_solid_logo.png'

    elif 'stylenoriter' in User_url:  
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                script_re = re.compile('(?<=content_name: ).+(?=,)')
                Title_key = script_re.findall(str(soup))[0]
            except:
                Title_key = Title_key
        try:
            Thumbnail_image_key = soup.select_one('img.bigImage')['src']
        except:
            try:
                Thumbnail_image_key = '	https://stylenoriter.co.kr' + Thumbnail_image_key
            except:
                Thumbnail_image_key = Thumbnail_image_key

    elif 'styleshare' in User_url:  
        product_id_re = re.compile('(?<=goods\/)[0-9]+')
        product_id = product_id_re.findall(User_url)[0]
        User_url_api = 'https://shop-gateway.styleshare.kr/display/api/v1/goods/' + str(product_id)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)
        try:
            Title_key = result_dict['name']
        except:
            Title_key = Title_key
            
    elif 'adidas' in User_url:  
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image'][0]
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'amazon' in User_url:  
        
#         chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
        chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버 #라니 오픈
#         chromedriver = 'C:/Users/FNUCNI/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)')
        options.add_argument('lang = ko_KR')

        driver = webdriver.Chrome(chromedriver, options=options)

        driver.get(User_url)

        res = driver.page_source

        soup = BeautifulSoup(res, 'html.parser')

        script_re = re.compile('(?<=jQuery.parseJSON\(\').+(?=\'\);)')
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text) 

        try:
            Title_key = soup.select_one('meta[name="title"]')['content']
        except:
            try:
                Title_key = dict_result_script_text['title']
            except:
                Title_key = Title_key

        try:
            Description_key = soup.select_one('meta[name="description"]')['content']
        except:
            try:
                Description_key = dict_result_script_text['title']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = soup.select_one('div.imgTagWrapper img')['src']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'amoremall' in User_url: 
        script = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(str(script))

        try:
            Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['onlineProdName']
        except:
            try:
                Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['prodName']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['prodName']
                except:
                    try:
                        Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['title']
                    except:
                        Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['prodImages'][0]['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['onlineProdImages'][0]['imgUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['image']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

        try:
            Description_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['linePromoDesc']
        except:
            try:
                Description_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['desc']
            except:
                Description_key = Description_key
                
    elif 'afreecatv' in User_url: 
        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['thumbnailUrl']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'aladin' in User_url: 
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image']
        except:
            Thumbnail_image_key= Thumbnail_image_key

    elif 'albamon' in User_url:
        if len(Thumbnail_image_key)<28 :
            Thumbnail_image_key = 'https://mc.albamon.kr' + Thumbnail_image_key
            
    elif 'aboutpet' in User_url:
        if 'goods' in User_url:
            User_url = User_url.replace('goodsDetailShare', 'indexGoodsDetail')
            res = requests.get(User_url, headers=headers) 
            soup = BeautifulSoup(res.content, 'html.parser')
            
            script_re = re.compile('(?<=\"name\": ).*(?=,)')
            Title_key = script_re.findall(str(soup))[0].strip('"')

            script_re = re.compile('(?<=category\":).*(?=,)')
            Description_key = script_re.findall(str(soup))[0].strip('"')

            script_re = re.compile('(?<=imgPath =).*(?=;)')
            Thumbnail_image_key = script_re.findall(str(soup))[0].strip('"')
            
    elif 'a-bly' in User_url:
            product_id_alby_re = re.compile('(?<=goods\/)[0-9]+')
            product_id_alby1 = product_id_alby_re.findall(User_url)

            for product_id_alby in product_id_alby1:
                User_url_api = 'https://api.a-bly.com/webview/goods/' + str(product_id_alby)

            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")

            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['goods']['name']
            except:
                Title_key = Title_key
                
    elif 'encar' in User_url:
        script_re = re.compile('(?<=PRELOADED_STATE__ =).+(?=<\/script><script id)',re.DOTALL)
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)
        try:
            Title_key = dict_result_script_text['cars']['base']['category']['manufacturerName'] + dict_result_script_text['cars']['base']['category']['modelName']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['cars']['base']['advertisement']['oneLineText']
        except:
            Description_key = Description_key

    elif 'yes24' in User_url:
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))

        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'ohou' in User_url:
        script = soup.select_one('div[data-react-class="App"]')['data-react-props']
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['additional_data'][1]['data']['production']['name']
        except:
            Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['additional_data'][1]['data']['production']['image_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif Distributor_key in ['auction']:               
        if 'sflex.' in User_url:
            broadcastId_re = re.compile('(?<=const broadcastId = ).+(?=\;)')
            broadcastId = broadcastId_re.findall(str(soup))[0].strip('''"''')
            User_url_api = 'https://api.sauceflex.com/V1/internal/broadcast/' + str(broadcastId)
            print(User_url_api)

            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)

            try:
                Title_key = result_dict['response']['items'][0]['broadcastName']
            except:
                Title_key = Title_key

            try:
                Description_key = result_dict['response']['items'][0]['explanation']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = result_dict['response']['items'][0]['thumbnailList'][0]['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
        elif 'mobile.' in User_url:
            mobile_action_re = re.compile('(?<=var scheme_url = ).+(?=\;)')
            mobile_action = mobile_action_re.findall(str(soup))[0].strip("'")
            User_url = str(mobile_action)

            res = requests.get(User_url, timeout=3, headers=headers) 
            soup = BeautifulSoup(res.text, 'html.parser')

            script_re = re.compile('(?<=Request.Item= ).+(?=,)') 
            script_text1 = script_re.findall(str(soup))[0] + str("}")
            script_text = script_text1.replace("\'", '\"')
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['itemName']
            except:
                Title_key = Title_key
        elif 'itempage' in User_url:
            script_re = re.compile('(?<=Request.Item= ).+(?=,)') 
            script_text1 = script_re.findall(str(soup))[0] + str("}")
            script_text = script_text1.replace("\'", '\"')
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['itemName']
            except:
                Title_key = Title_key
        else:
            script_re1 = re.compile('(?<=DetailLayer\.GetGroupList = function\(element, mItemNo, sItemNo, itemIndex\)).+(?=success: function\(res)', re.DOTALL)
            script_text1 = script_re1.findall(str(soup))[0]
            script_re2 = re.compile('(?<=data: \"\{\'groupList\': \'\" \+ \').+(?=\' \+ )')
            script_text2 = script_re2.findall(script_text1)[0]
            dict_result_script_text = json.loads(script_text2)[0]

            try:
                Title_key = dict_result_script_text['ItemName']
            except:
                Title_key = Title_key

            try:
                Thumbnail_image_key = dict_result_script_text['ThumbImageUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['GalleryImageUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key
    #아래부터 미검증
    elif 'elandmall' in User_url:
        if 'goods' in User_url:
            try:
                Title_key = soup.select_one('meta[property="og:description"]')['content']
            except: 
                Title_key = Title_key

        elif 'broadcast' in User_url:
            try:
                product_id_eland_re = re.compile('(?<=vcelandmall-)\w+')
                product_id_eland = product_id_eland_re.findall(User_url)[0]

                User_url_api = 'https://ekuf1uoz9d.execute-api.ap-northeast-2.amazonaws.com/api/V1/getRoom?broadcastId=lkelandmall-' + str(product_id_eland)

                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                print(User_url_api)

                if res_api.status_code != 200:
                    print("User_url_api 접속 오류입니다")

                result_dict = json.loads(res_api.text)

                Title_key  = result_dict['data']['getRoom']['title']
            except:
                Title_key  = Title_key 

    elif 'movie' in User_url:
        if 'ssg' in User_url:       
            try:
                 Title_key = soup.select_one('#movie > img')['alt']
            except:
                 Title_key = Title_key 

    elif 'book.interpark' in User_url:
        if 'product' in User_url:
            try:
                Title_key =  soup.select_one('h2').get_text()
            except:
                Title_key = Title_key 


    elif 'interpark' in User_url:
        if 'ticket' in User_url:
            product_id_ticketip_re = re.compile('(?<=goods\/)\d+')
            product_id_ticketip = product_id_ticketip_re.findall(User_url)[0]
            User_url_api = 'https://api-ticketfront.interpark.com/v1/goods/' + str(product_id_ticketip) + '/summary?goodsCode=22004761&priceGrade=&seatGrade='
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['data']['goodsName']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = result_dict['data']['goodsLargeImageUrl']
            except: 
                Thumbnail_image_key = Thumbnail_image_key

    elif 'live.interpark' in User_url:
        try:
            Thumbnail_image_key = soup.select_one('div.prdImg > img')['src']
        except: 
            Thumbnail_image_key =  Thumbnail_image_key

    elif 'imvely' in User_url:
        if 'event' in User_url:       
            try:
                Title_key = soup.find('div',attrs = {'class':'boardRead'}).find('h3').text
            except:
                Title_key = Title_key 

    elif 'cabinService' in User_url:
        if 'jejuair' in User_url:
            try: 
                Title_key = soup.select_one('div.page-title').get_text()
            except:
                Title_key= Title_key 

    elif 'zigbang' in User_url:
        try: 
             Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
             Title_key = Title_key         
        try: 
            Description_key= soup.select_one('meta[property="og:description"]')['content']     
        except:
             Description_key = Description_key

    elif 'jinair' in User_url:
        try:
            jinair_content= soup.find('h4',{'class':'info_title'})
            Title_key = jinair_content.text.split('\n')[2]
            Thumbnail_image_ad = soup.select_one('#_TRK_PN_ID')['src']  
            Thumbnail_image_key = 'https://jinistore.jinair.com/'+ (Thumbnail_image_ad)
        except:
            Title_key = Title_key 
            Thumbnail_image_key = Thumbnail_image_key

    elif 'ggumim' in User_url:
        try: 
            content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
            content_ggumim_re = json.loads(content_ggumim.text)

            Title_key = content_ggumim_re['props']['pageProps']['qnaSolutionPageData']['title']
            Thumbnail_image_key = content_ggumim_re['props']['pageProps']['qnaSolutionPageData']['mainImage']
        except:
            Title_key  = Title_key 
            Description_key = Description_key
            Thumbnail_image_key = Thumbnail_image_key

        if 'furniture' in User_url:
            try: 
                content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
                content_ggumim_re = json.loads(content_ggumim.text)

                Title_key = content_ggumim_re['props']['initialState']['app']['share']['title']
                Description_key = content_ggumim_re['props']['initialState']['app']['share']['Description']
                Thumbnail_image_key = content_ggumim_re['props']['initialState']['app']['share']['imageUrl']
            except:
                try:
                    Title_key = content_ggumim_re['props']['initialProps']['pageProps']['furnitureViewData']['furnitureName']
                except:
                    try:
                        Title_key = content_ggumim_re['furniture']['name']
                    except:
                        Title_key  = Title_key 
                        Description_key = Description_key
                        Thumbnail_image_key = Thumbnail_image_key

    elif 'tv.kakao' in User_url:

        if 'VIDEOSUS' in User_url:
            kakao_id_re = re.compile('(?<=cliplink/)\d+')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://tv.kakao.com/vapi/playlist/v2/main/404089/videos?videoId=' + str(kakao_id) + '&sort=order&size=20'
            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
        # 타이틀
            try:
                Title_key = result_dict['list'][0]['programTitle']
            except:
                Title_key = Title_key
        #디스크립션                
            try:
                Description_key = result_dict['list'][0]['episodeTitle']
            except:
                Description_key = Description_key
        #썸네일                
            try:
                Thumbnail_image_key = result_dict['list'][0]['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key

        elif 'cliplink' in User_url:
            kakao_id_re = re.compile('[0-9]+$')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://play-tv.kakao.com/api/v1/ft/playmeta/cliplink/' + str(kakao_id) + '?fields=@html5vod&service=kakao_tv&type=VOD'
            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
        # 타이틀
            try:
                Title_key = result_dict['kakaoLink']['templateArgs']['${title}']
            except:
                try: 
                    Title_key = result_dict['clipLink']['clip']['title']
                except: 
                    try:
                        Title_key = result_dict['clipLink']['displayTitle']
                    except:
                        Title_key = Title_key
        #디스크립션                
            try:
                Description_key = result_dict['clipLink']['channel']['description']
            except:
                Description_key = Description_key
        #썸네일                
            try:
                Thumbnail_image_key = result_dict['kakaoLink']['templateArgs']['${thumbnailUrl}']
            except:
                try: 
                    Thumbnail_image_key = result_dict['clipLink']['clip']['thumbnailUrl']
                except: 
                    Thumbnail_image_key = Thumbnail_image_key


        elif 'episodes' in User_url:
            kakao_id_re = re.compile('[0-9]+')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://tv.kakao.com/vapi/channel/v2/detail/' + str(kakao_id) + '/home?at=web'
            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
        # 타이틀
            try:
                Title_key = result_dict['title']
            except:
                try: 
                    Title_key = result_dict['channelShare']['templateArgs']['${title}']
                except: 
                    Title_key = Title_key
        #디스크립션                
            try:
                Description_key = result_dict['channelShare']['templateArgs']['$${synopsis}']
            except:
                Description_key = Description_key
        #썸네일                
            try:
                Thumbnail_image_key = result_dict['channelShare']['templateArgs']['${thumbnailUrl}']
            except:
                try: 
                    Thumbnail_image_key = result_dict['channelCover']['coverImageUrl']
                except: 
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'twayair' in User_url:
        try: 
             Title_key = soup.select_one('#content > div.section.t3 > div > div.grid_view_head.evt > h3').text
        except:
             Title_key = Title_key 

    elif 'costco' in User_url:
        if 'campaign' in User_url:
            try:
                Thumbnail_image_key = soup.select_one('meta[name="thumbnail"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key

    elif 'topten10mall' in User_url:

        try:
            Thumbnail_image_url = soup.select_one('meta[property="eg:itemImage"]')['content']
            product_id_topten_re = re.compile('(?<=/goods/)\w{13}')
            product_id_topten = product_id_topten_re.findall(Thumbnail_image_url)[0]
            Thumbnail_image_key = 'https://imgp.topten10mall.com/ssts/image/goods/'+ str(product_id_topten) +'_M?AR=0&RS=740x1010&appopen=new'
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'pet-friends' in User_url:
        try: 
            content_petf = soup.find_all('script', {'type':'application/json'})[0]
            content_petf_re = json.loads(content_petf.text)

            Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaProductName']
            Description_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['description']
            Thumbnail_image_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['itemImage']
        except:
            try: 
                Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['productName']
            except:
                try:
                    Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['title']
                except:  
                    Description_key = Description_key
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'houseapp' in User_url: 
        if 'link' in User_url: 
            product_id_houseapp_re = re.compile('(?<=goods\/)\d+')
            product_id_houseapp = product_id_houseapp_re.findall(User_url)[0]
            User_url_api = 'https://store.houseapp.co.kr/goods/detail.do?goodsNo=' + str(product_id_houseapp) +'&goodsNo='+ str(product_id_houseapp) + '&popup=up'
            print(User_url_api)

            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            soup_re = BeautifulSoup(res_api.content,'html.parser')


            Title_key = soup_re.select_one('meta[property="og:title"]')['content']
            Description_key = soup_re.select_one('meta[property="og:description"]')['content']
            Thumbnail_image_key = soup_re.select_one('meta[property="og:image"]')['content'] 

    elif 'hanssem' in User_url:
        if 'broadcast' in User_url:
            try: 
                product_id_hanssem_re = re.compile('(?<=hanssem-)\d\w+')
                product_id_hanssem = product_id_hanssem_re.findall(User_url)[0]
                User_url_api = 'https://api.sauceflex.com/V1/internal/broadcast/lkhanssem-' + str(product_id_hanssem)

                res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                result_dict = json.loads(res_api.text)

                Title_key = result_dict['response']['items'][0]['broadcastName']
                Thumbnail_image_key = result_dict['response']['items'][0]['thumbnailList'][0]['thumbnailUrl']

            except:
                Title_key= Title_key
                Thumbnail_image_key = Thumbnail_image_key

    elif 'hnsmall' in User_url:
        if 'broadcast' in User_url:
            try:     
                product_id_hnsmall_re = re.compile('(?<=hnsmall-)\d\w+')
                product_id_hnsmall = product_id_hnsmall_re.findall(User_url)[0]
                User_url_api = 'https://api.sauceflex.com/V1/internal/broadcast/lkhnsmall-' + str(product_id_hnsmall)
                print(User_url_api)

                res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                result_dict = json.loads(res_api.text)


                try:
                    Title_key = result_dict['response']['items'][0]['broadcastName']
                except:
                    Title_key = result_dict['response']['items'][0]['productListDetail'][0]['productName']

                Thumbnail_image_key = result_dict['response']['items'][0]['thumbnailList'][0]['thumbnailUrl']

            except:
                Title_key= Title_key
                Thumbnail_image_key = Thumbnail_image_key

    elif 'spooncast' in User_url:
        try:
            live_id_re = re.compile('(?<=live\/)[0-9]+')
            live_id = live_id_re.findall(User_url)[0]  
            User_url_api = 'https://kr-api.spooncast.net/lives/' + live_id          
        except:
            product_id_re = re.compile('(?<=products\/)[0-9]+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://kr-store-api.spooncast.net/v1/store/products/' + product_id              
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)


        try:
            Title_key = result_dict['results'][0]['title']
        except:
            try:
                Title_key = result_dict['title'] 
            except:
                Title_key = Title_key
        try:
            Description_key = result_dict['description']
        except:
            Description_key = Description_key
            
    elif 'boribori' in User_url:
        if 'product' in User_url:
            product_id_re = re.compile('(?<=productNo=).+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://apix.halfclub.com/product/products/withoutPrice/' + str(product_id)+ '?_=&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2'                      

            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data']['prdNm']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key_url = result_dict['data']['productImage']['basicExtNm']
                Thumbnail_image_key = 'https://cdn2.boribori.co.kr/rimg/500/'+ Thumbnail_image_key_url
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
                
        elif 'deal' in User_url:
            product_id_re = re.compile('(?<=PrdNo=)\d+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2&ts=1660814208352'

            print(User_url_api)
            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data']['prdNm']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key_url = result_dict['data']['productImage']['basicExtNm']
                Thumbnail_image_key = 'https://cdn2.boribori.co.kr/rimg/500//'+ Thumbnail_image_key_url
            except:
                Thumbnail_image_key = Thumbnail_image_key  
                
        elif 'magazine' in User_url:
            product_id_re = re.compile('(?<=cmntySeq=)\d+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://cf-api.halfclub.com/community/community/magazine/info?cmntySeq=' + str(product_id)+ '&siteCode=2'

            print(User_url_api)
            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data']['title']
            except:
                Title_key = Title_key
                
        else:
            product_id_re = re.compile('(?<=plan\/).+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://apix.halfclub.com/display/plans/' + str(product_id)+ '?apiFlag=true&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&prdFlag=false&siteCd=2'

            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data'][0]['planNm']
            except:
                Title_key = Title_key      
#3요소소
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
desc_trash_words = ['ㄴ ', '\t', '\n', '\r\n', '\ufeff', '\u200e', '\r\u200b\r', '\r', '<ul>', '</ul>', '<li>', '</li>']
for desc_trash_word in desc_trash_words:
    Description_key = Description_key.replace(desc_trash_word, "")
    
Description.append(Description_key.strip())

if Thumbnail_image_key.startswith("//"):
    Thumbnail_image_key = Thumbnail_image_key[2:]
elif Thumbnail_image_key.startswith(" //"):
    Thumbnail_image_key = Thumbnail_image_key[3:]
elif Thumbnail_image_key.startswith("/"):
    Thumbnail_image_key = Thumbnail_image_key[1:]

Thumbnail_image.append(Thumbnail_image_key.strip())

print('최종 Title 리스트 값은, ', Title)
print('최종 Description 리스트 값은, ', Description)
print('최종 Thumbnail_image 리스트 값은, ', Thumbnail_image)
print("최종 User_url", User_url)

#설명 6번
# lprice & mall 파악

#Type = 위시 중 아래 3가지로 구분

#1. Lower_price, Searched까지 다 찾는 것(Ex. 11번가 - 구체적 상품 페이지): Type == 위시 구분된 것
#2. Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓, 여행상품): no searched 셋팅 / Lower_price_key 안 잡는 경우: 룸/상품 등 조건이 많은 경우
#3. Lower_price, Searched 다 안 찾는 것(Ex. 11번가 - 기획전 페이지): Lower_price == "확인필요" or "-" 

if Type_key == '위시':
    print("현재 가격 스크래핑 시작")
    
    #no_searched 셋팅_최저가 찾는 의미가 없는 것(Ex. 숙박, 항공, 공연티켓 등)
    no_searched_keywords = ['myrealtrip', 'town.daangn', 'goodchoice', 'airbnb', 'booking.com', 'asiana', 'exhib']    # 'car' -> 'cartier'와 같은 경우, 이를 피하기 위해 끝나는 마침표를 꼭 찍어줄 것
    if any(no_searched_keyword in User_url for no_searched_keyword in no_searched_keywords) == False:
        try:
            # 개별 site 최저가 크롤링 설정
            # 11번가
            if Distributor_key in ['11st']:
                # FB 헤더값 설정 시 미충족 html
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
                res = requests.get(User_url, timeout=3, headers=headers) 
                print('접속상태?', res.status_code)
                soup = BeautifulSoup(res.text, 'html.parser')

                try:
                    Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 strong > span.value').text
                except:
                    try:
                        Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 span.value').text
                    except:   
                        try:
                            Lower_price_key = soup.select_one('#priceLayer > div.price > span > b').text
                        except:
                            try:
                                product_id_11st_re = re.compile('(?<=products\/pa\/)[0-9]+|(?<=products\/)[0-9]+')

                                product_id_11st = product_id_11st_re.findall(User_url)[0]
                                User_url_api = 'https://www.11st.co.kr/products/v1/pc/products/' + str(product_id_11st) + '/detail'
                                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                                result_dict = json.loads(res_api.text)

                                Lower_price_key = result_dict['price']['finalDscPrice']
                            except:
                                try:
                                    if 'live11' in User_url:
                                        Lower_price_key = dict_result_script_api['settingInfo']['settings'][1]['products'][0]['finalDscPrice']
                                except:
                                    Lower_price_key = Lower_price_key
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
            elif Distributor_key in ['musinsa']: #'무신사 회원가' 중 가장 비싼 가격을 선택
                if 'musinsaapp' in User_url:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
                    res = requests.get(User_url, timeout=3, headers=headers) 
                    soup = BeautifulSoup(res.content, 'html.parser')                
                try:
                    script_re = re.compile('(?<=stateAll = ).+')
                    script_text = script_re.findall(str(soup))[0]
                    dict_result_script_text = json.loads(script_text)
                    Lower_price_key = dict_result_script_text['productInfo']['price']                 
                except:
                    try:
                        Lower_price_key = soup.select_one('#goods_price').text            
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['productInfo']['normal_price'] 
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['bunjang']:
                try:
                    Lower_price_key = result_dict['item_info']['price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']  
                    except:
                        Lower_price_key = Lower_price_key

                if result_dict['item_info']['status'] == "3":
                    Lower_price_key = "품절인가봐요!"

            #에이블리
            elif Distributor_key in ['a-bly']:
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

            elif Distributor_key in ['brandi']:
                try:
                    Lower_price_key = dict_result_script_text['product']['product']['sale_price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['product']['product']['original_sale_price']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['product']['product']['original_price_info']['sale_price']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['product']['product']['original_price_info']['expect_sale_price']
                            except:
                                try:
                                    Lower_price_key = soup.select_one('p.price').text
                                except:
                                    Lower_price_key = Lower_price_key

            # 지마켓
            elif Distributor_key in ['gmarket']:
                try:
                    Lower_price_key = dict_result_script_text['Order']['Price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['Discount']['DcPrice']
                    except:
                        try:
                            Lower_price_key = soup.select_one('strong.price_real').text
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['oliveyoung']:
                try:
                    Lower_price_key = result_dict['salePrc']
                except:
                    try:
                        Lower_price_key = result_dict['supPrc']
                    except:  
                        try:
                            Lower_price_key = soup.select_one('span.price-2').text
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['daangn']:

                try:
                    Lower_price_key = soup.select_one('#article-price').text
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['wemakeprice']:
                script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
                script_text1 = script_re.findall(str(soup))
                script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
                dict_result_script_text = json.loads(script_text)

                try:
                    Lower_price_key = dict_result_script_text['prodMain']['sale']['benefitPrice']
                except:
                    Lower_price_key = dict_result_script_text['prodMain']['sale']['salePrice']

            elif Distributor_key in ['29cm']:            
                try:
                    Lower_price_key = soup.select_one('span.css-4bcxzt.ent7twr4').text
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['cjonstyle']:
                product_id_cjon_re = re.compile('(?<=item\/)[0-9]+|(?<=mocode\/)M[0-9]+')
                product_id_cjon1 = product_id_cjon_re.findall(User_url)

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
                        try:
                            Lower_price_key = dict_result_script_api['data']['rvo']['npriceFullType']
                        except:
                            try:
                                Lower_price_key = dict_result_script_api['data']['rvo']['salprc']
                            except:
                                try:
                                    Lower_price_key = dict_result_script_api['data']['rvo']['npriceFullType']
                                except:
                                    try:
                                        Lower_price_key = dict_result_script_api['data']['rvo']['wklyDcPrc']
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

            elif Distributor_key in ['gsshop']: 
                try:
                    Lower_price_key = dict_result_script_text['pmo']['rentConslInfo']['exposeRentConslCostMin']                
                except:
                    try:
                        Lower_price_key = dict_result_script_text['pmo']['prc']['minPrc']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['pmo']['gsPrc']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['pmo']['prc']['flgdPrc']
                            except:
                                Lower_price_key =Lower_price_key

            elif Distributor_key in ['cartier']: 
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    try:
                        Lower_price_key = soup.select_one('span.value').text    
                    except:
                        Lower_price_key =Lower_price_key

            elif Distributor_key in ['dabang']: 
                try:
                    product_id_dabang_re = re.compile('(?<=room\/).+')
                    product_id_dabang = product_id_dabang_re.findall(User_url)[0]
                    User_url_api = 'https://www.dabangapp.com/api/3/room/detail3?api_version=3.0.1&call_type=web&room_id=' + product_id_dabang
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['room']['price_title']  # <=이부분만 수정해도 됨
                    except:
                        Lower_price_key = Lower_price_key
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['naver']:
                if 'land.naver' in User_url:
                    try:
                        Lower_price_key = dict_result_script_text['state']['article']['dealerTelInfo']['prcInfo']
                        if Lower_price_key == "0":
                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['dealPrice'])
                            if Lower_price_key == "0":
                                Lower_price_key = soup.select_one('strong.detail_deal_price').text 
                                if Lower_price_key == "0":
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])
                    except:
                        try:
                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['dealPrice'])
                            if Lower_price_key == "0":
                                Lower_price_key = soup.select_one('strong.detail_deal_price').text 
                                if Lower_price_key == "0":
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])                      
                        except:
                            try:
                                Lower_price_key = soup.select_one('strong.detail_deal_price').text #가격비교 안할꺼니 한글명 단위 -> 숫자 치환 안함
                                if Lower_price_key == "0":
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])         
                            except:
                                try:
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])
                                except:
                                    Lower_price_key = Lower_price_key            
                elif 'book' in User_url:
                    try:
                        Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['BookCatalog']['statistics']['paperBook']['lowPrice']
                    except:
                        Lower_price_key = Lower_price_key
                elif 'joonggonara' in User_url:
                    try:
                        Lower_price_key = dict_result_script_api['result']['saleInfo']['price']
                    except:
                        Lower_price_key = Lower_price_key                

                else: #일반 쇼핑(catalog, brand, smartstore, store...etc.)
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['catalog_Catalog']['lowestPrice']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][3]['state']['data']['pages'][0]['products'][0]['mobilePrice']
                            except:
                                try:
                                    Lower_price_key = dict_result_script_text['props']['pageProps']['catalog']['lowestPrice']
                                except:
                                    try:
                                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['info']['lowestPrice']
                                    except:
                                        try:
                                            Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['recommend']['comparision']['baseItem']['mobileLowPrice']
                                        except:
                                            try:
                                                Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['recommend']['comparision']['baseItem']['lowPrice']
                                            except:
                                                try:
                                                    Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['products'][0]['productsPage']['products'][0]['pcPrice']
                                                except:
                                                    try:
                                                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['products'][0]['productsPage']['products'][0]['mobilePrice']
                                                    except:
                                                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['wconcept']:
                try:
                    script_re = re.compile('(?<=value: ).*(?=\,)')
                    Lower_price_key = script_re.findall(str(soup))[0]    
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                    except:
                        try:
                            Lower_price_key = soup.select_one('input[name="saleprice"]')['value']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['af_sale_price']
                            except:
                                Lower_price_key = Lower_price_key            

            elif Distributor_key in ['thehandsome']:                            
                try:    
                    script_re = re.compile('(?<=dcPrice :).*(?=\,)')
                    Lower_price_key = script_re.findall(str(soup))[0]        
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="recopick:sale_price"]')['content']
                    except:
                        try:
                            Lower_price_key = soup.select_one('input#productPrice')['value']
                        except:
                            try:
                                script_re = re.compile('(?<=price :).*(?=\,)')
                                Lower_price_key = script_re.findall(str(soup))[0]   
                            except:
                                try:
                                    Lower_price_key = soup.select_one('meta[property="recopick:price"]')['content']
                                except:
                                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['dior']:                                    
                try:
                    Lower_price_key = dict_result_script_text['offers'][0]['price']   
                except:
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']            
                    except:
                        try:
                            Lower_price_key = str(dict_result_script_text['product']['variants'][0]['price'])[:-2]
                        except:
                            try:
                                Lower_price_key = soup.select_one('input#selected-variant-price')['value']
                            except:
                                Lower_price_key = Lower_price_key

            elif Distributor_key in ['lotteimall']:
                try:
                    Lower_price_key = soup.select_one('p.price_fin').text
                except:
                    try:
                        Lower_price_key = soup.select_one('span.sale_price').text
                    except:
                        try:
                            script_re = re.compile('(?<=sel_item_sale_prc = ).*(?=;)')
                            Lower_price_key2 = script_re.findall(str(soup))
                            for Lower_price_key1 in Lower_price_key2:
                                if Lower_price_key1 != 0:
                                    Lower_price_key = Lower_price_key1
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['louisvuitton']:
                try:
                    script_re = re.compile('(?<=\"price\":)[^,]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        script_re = re.compile('(?<=\"productPrice\":)[^a-z]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['myrealtrip']:
                try:
                    Lower_price_key = dict_result_script_text['offer']['price']['main']
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['homeplus']:
                try:
                    Lower_price_key = dict_result_script_text['@graph'][0]['offers']['price']
                except:
                    try:
                        Lower_price_key = soup.select_one('span.info_txt > em').text     #추가한 구문
                    except:
                        Lower_price_key = Lower_price_key   

            elif Distributor_key in ['kurly']:
                Lower_price_key1 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['discountedPrice']
                Lower_price_key2 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['retailPrice']
                Lower_price_key3 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['basePrice']
                Lower_price_key4 = dict_result_script_text['props']['pageProps']['product']['discountedPrice']
                Lower_price_key5 = dict_result_script_text['props']['pageProps']['product']['retailPrice']
                Lower_price_key6 = dict_result_script_text['props']['pageProps']['product']['basePrice']

                Lower_price_key_int_list = []
                Lower_price_key_all_list = [Lower_price_key1, Lower_price_key2, Lower_price_key3, Lower_price_key4, Lower_price_key5, Lower_price_key6]
                for Lower_price_key_temp in Lower_price_key_all_list:
                    if type(Lower_price_key_temp) == int:
                        Lower_price_key_int_list.append(Lower_price_key_temp)  
                Lower_price_key = min(Lower_price_key_int_list)            

            elif Distributor_key in ['mangoplate']:
                if 'eat_deals' in User_url:
                    try:
                        Lower_price_key = soup.select_one('span.EatDealInfo__SalesPrice').text
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['sales_price']
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['mustit']:                        
                try:
                    script_re = re.compile('(?<=MAX_BENEFIT\",price:)[0-9]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        Lower_price_key = soup.select_one('span.font-bold').text
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['moulian']:   
                try:
                    script_re = re.compile('(?<=var product_price =).+(?=;)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        Lower_price_key = soup.select_one('input#disprice')['value']
                    except:
                        try:
                            Lower_price_key = soup.select_one('input#disprice_wh')['value']
                        except:
                            try:
                                Lower_price_key = soup.select_one('input#discount_price')['value']
                            except:
                                Lower_price_key = Lower_price_key

            elif Distributor_key in ['balaan']:
                try:
                    Lower_price_key = result_dict['data'][product_id_balaan]['member_price']
                except:
                    try:
                        Lower_price_key = result_dict['data'][product_id_balaan]['price']
                    except:
                        try:
                            Lower_price_key = soup.select_one('span#price').text
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['burberry']:
                try:
                    Lower_price_key = dict_result_script_text['db']['pages'][product_id]['data']['price']['current']['value']
                except:
                    try:
                        Lower_price_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['offers']['price']
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['chanel']:

                script_re = re.compile('(?<=Load = Object.assign\().+(?=, {})')
                script_text = script_re.findall(str(soup))[0]
                dict_result_script_text = json.loads(script_text)  
                try:  
                    Lower_price_key_org = dict_result_script_text['ecommerce']['detail']['products'][0]['price']   #수정
                    Lower_price_key = re.findall('\d.+(?<=\.)',Lower_price_key_org)[0]                             #추가

                except:
                    try:
                        Lower_price_key = soup.select_one('p.product-details__price').text
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['pulmuone']:
                try:
                    Lower_price_key = dict_post_api['data']['salePrice']                
                except:
                    try:                    
                        Lower_price_key = dict_post_api['data']['discountPrice']
                    except:
                        try:
                            Lower_price_key = dict_post_api['data']['buyerPaymentExpectedPrice']    
                        except:
                            try:
                                Lower_price_key = dict_post_api['data']['recommendedPrice']
                            except:
                                Lower_price_key = Lower_price_key

            elif Distributor_key in ['seoulstore']:                        
                try:
                    Lower_price_key = dict_post_api['discountPrice']
                except:
                    try:
                        Lower_price_key = dict_post_api['sellingPrice']
                    except:
                        try:
                            Lower_price_key = dict_post_api['sortPrice']
                        except:
                            try:
                                Lower_price_key = dict_post_api['salePrice']  
                            except:
                                Lower_price_key = Lower_price_key

            elif Distributor_key in ['stylenoriter']:  
                try:
                    Lower_price_key = soup.select_one('meta[property="product:sale_price:amount"]')['content']
                except:
                    try:
                        script_re = re.compile('(?<=product_sale_price = )[0-9]+')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['styleshare']:  
                try:
                    Lower_price_key = result_dict['lowestCouponInfo']['couponPrice']
                except:
                    try:
                        Lower_price_key = result_dict['price']
                    except:
                        try:
                            Lower_price_key = result_dict['optionInfo']['options'][0]['price']
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['adidas']:                          
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['amazon']:                  
                try:
                    Lower_price_key = soup.select_one('input#twister-plus-price-data-price')['value']
                except:
                    Lower_price_key = Lower_price_key
                driver.quit()
            elif Distributor_key in ['idus']:              
                try:
                    Lower_price_key= soup.select_one('.sold-price').text
                except:
                    Lower_price_key = Lower_price_key

            elif Distributor_key in ['amoremall']: 
                try:
                    Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['availablePrice']['minFinalOnlinePrice']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['availablePrice']['finalOnlinePrice']
                    except:
                        try:
                            Lower_price_key = soup.select_one('#__next > section > section.container > section > section.container > section > div > div:nth-child(1) > div.summary > div.priceArea > span.price > strong').text
                        except:
                            Lower_price_key = Lower_price_key

            elif Distributor_key in ['aladin']:     
                try:
                    Lower_price_key = dict_result_script_text['workExample'][0]['potentialAction']['expectsAcceptanceOf']['Price']
                except:
                    try:
                        script_re = re.compile('(?<=\"price\":)[\0-9]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif Distributor_key in ['aboutpet']:
                script_re = re.compile('(?<=price\":).+')
                Lower_price_key = script_re.findall(str(soup))[0].strip('"')  

            elif Distributor_key in ['encar']:
                try:
                    Lower_price_key = dict_result_script_text['cars']['base']['advertisement']['price'] + '만원'
                except:
                    try:
                        Lower_price_key = soup.find('span', attrs={'DetailSummary_txt_price__2LUpg'}).text
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif Distributor_key in ['yes24']:
                try:
                    Lower_price_key = dict_result_script_text['workExample'][0]['potentialAction']['expectsAcceptanceOf']['Price'] #일반도서
                except:
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price'] #티켓
                    except:
                        try:
                            Lower_price_key = soup.select_one('em.yes_b').text #일반
                        except:
                            try:
                                Lower_price_key  = soup.select_one('.yes_m').text #티켓
                            except:
                                Lower_price_key = Lower_price_key
                                
            elif Distributor_key in ['ohou']:
                try:
                    Lower_price_key = dict_result_script_text['additional_data'][1]['data']['production']['selling_cost']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['additional_data'][1]['data']['production']['selling_price']
                    except:
                        try:
                            Lower_price_key = soup.select_one('span.production-selling-header__price__price').text
                        except:
                            Lower_price_key = Lower_price_key
                            
            elif Distributor_key in ['auction']:
                try:
                    Lower_price_key = dict_result_script_text['DiscountPrice']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['Price']
                    except:
                        try:
                            Lower_price_key = result_dict['response']['items'][0]['productListDetail'][0]['sellingPrice']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['itemPrice']['SellingPrice']
                            except:
                                Lower_price_key = Lower_price_key
         #아래부터 미검증                   
            elif Distributor_key in ['elandmall']:                   
                try:
                    Lower_price_key = soup.select_one('#goods_info > div.gd_prc > dl > dd > span.sp > b').text
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'interpark' in User_url:
             # 티켓은 좌석별 가격 상이하여 최저가 제외
                try:
                    content_ineterpark = soup.find_all('script', {'type':'application/ld+json'})[0]
                    content_ineterpark_re = json.loads(content_ineterpark.text)
                    Lower_price_key = content_ineterpark_re['offers']['price']
                except:
                    try: 
                        Lower_price_key = soup.select_one('span.price').text
                    except:
                        Lower_price_key = Lower_price_key

                if 'live' in User_url:
                    try:
                        Lower_price_key = soup.select_one('div.discountPrice > span.num').text 
                    except:
                        try:
                            Lower_price_key = soup.select_one('div.originalPrice > span.num').text  
                        except:
                            Lower_price_key = Lower_price_key   
                            
            elif 'ysl'in User_url:                 
                try:                    
                    Lower_price_key = soup.select_one('p.c-price__value--current').text.strip()
                except:
                    Lower_price_key = Lower_price_key  
                    
            elif 'xexymix'in User_url:   
                try:                    
                    Lower_price_key = soup.find('span', attrs={'class':'txt price_sell'}).text 
                except:
                    Lower_price_key = Lower_price_key 
                    
            elif 'jinair' in User_url:
                try:
                    Lower_price_key= soup.select_one('p.info_sale').text
                except:
                    Lower_price_key = Lower_price_key 
                    
            elif 'ggumim' in User_url:
                try: 
                    content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
                    content_ggumim_re = json.loads(content_ggumim.text)
                    Lower_price_key = content_ggumim_re['props']['initialProps']['pageProps']['furnitureViewData']['couponPrice']

                except:
                    try:
                        Lower_price_key = content_ggumim_re['props']['initialState']['app']['share']['priceDiscount']
                    except:
                        try:
                            Lower_price_key = content_ggumim_re['props']['initialState']['app']['share']['priceOriginal']
                        except:
                            try:
                                Lower_price_key = content_ggumim_re['furniture']['priceDiscount'] 
                            except:
                                try:
                                    Lower_price_key = content_ggumim_re['furniture']['priceOriginal'] 
                                except:
                                    Lower_price_key = Lower_price_key  
                   
            elif 'kolonmall' in User_url:
                try:
                    kolon_pd_re = re.compile('(?<=Product/)\w+')
                    kolon_pd = kolon_pd_re.findall(User_url)[0]
                    User_url_api = 'https://www.kolonmall.com/Product/recommendProducts4Assoc?productCode=' + str(kolon_pd) + '&_=1660025404429'
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers)   
                    result_dict = json.loads(res_api.text)

                    Lower_price_key = result_dict['results'][0]['price']['price']
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'trenbe'in User_url:  
                try:
                    product_id_trenbe_re = re.compile('\d{8}')
                    product_id_trenbe = product_id_trenbe_re.findall(User_url)[0]
                    User_url_api = 'https://service.trenbe.com/product/detail?goodsno=' + str(product_id_trenbe) + '&useActive=false'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)

                    Lower_price_key = result_dict['product']['finalPrice']

                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'tiffany'in User_url: 
                try: 
                    content_tiffany = soup.find_all('script', {'type':'application/ld+json'})[1]
                    content_tiffany_re = json.loads(content_tiffany.text)
                    Lower_price_key = content_tiffany_re['offers']['price']
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'fashionplus'in User_url: 

                try:                    
                    content_fashionplus = soup.find_all('script', {'type':'application/ld+json'})[0]
                    content_fashionplus_re = json.loads(content_fashionplus.text)
                    Lower_price_key = content_fashionplus_re['offers']['price']    
                    if Lower_price_key == '0' :
                        Lower_price_key = '품절입니다'
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'pet-friends' in User_url:
                try: 
                    content_petf = soup.find_all('script', {'type':'application/json'})[0]
                    content_petf_re = json.loads(content_petf.text)

                    Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['salePrice']
                except:
                    try:
                        Lower_price_key = content_petf_reThumbnail_image_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['discountApplyPrice']
                    except:
                        try:
                            Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['sellingPrice']
                        except:
                            try:
                                Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['originalPrice']
                            except: 
                                Lower_price_key =  Lower_price_key
                                
            elif 'prada'in User_url:
                try:                    
                    Lower_price_key = soup.select_one('div.info-card-component__basic-info-price').text.strip()
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'houseapp'in User_url:
                try:
                    Lower_price_key= Description_key.split(' ')[1]
                except: 
                    Lower_price_key =  Lower_price_key
                    
            elif 'hiver'in User_url:

                if 'onelink' in User_url:
                    try: 
                        product_id_hiver_re = re.compile('(?<=id=)\d+')
                        product_id_hiver = product_id_hiver_re.findall(User_url)[0]
                        User_url_api = 'https://www.hiver.co.kr/products/b/' + str(product_id_hiver) 
                        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                        soup = BeautifulSoup(res_api.content, 'html.parser')
                    except:
                        soup = BeautifulSoup(res.content, 'html.parser')

                content_hiver = soup.find_all('script', {'type':'application/json'})[0]

                content_hiver_re = json.loads(content_hiver.text)
                try:
                    Lower_price_key = content_hiver_re['data']['original_price_info']['expect_sale_price']
                except: 
                    try:
                        Lower_price_key = content_hiver_re['data']['original_price_info']['sale_price']
                    except:
                        try: 
                            Lower_price_key = content_hiver_re['data']['original_sale_price']
                        except:
                            try:
                                Lower_price_key = content_hiver_re['data']['sale_price']
                            except:
                                Lower_price_key = Lower_price_key
                                
            elif 'hanssem'in User_url:
                try:                    
                    Lower_price_key = soup.select_one('div.prd-prc-cur').text
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'homeplus'in User_url:
                try:     
                    product_id_hplus_re = re.compile('(?<=itemNo=)\d+')
                    product_id_hplus = product_id_hplus_re.findall(User_url)[0]
                    User_url_api = 'https://mfront.homeplus.co.kr/item/getItemDetail.json?itemNo=' + str(product_id_hplus) + '&storeType=HYPER'
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)

                    Lower_price_key_dc = result_dict['data']['item']['sale']['dcPrice']


                    if Lower_price_key_dc == 0 :
                        Lower_price_key = result_dict['data']['item']['sale']['salePrice']

                    else:
                        Lower_price_key = Lower_price_key_dc 

                except:
                    Lower_price_key = Lower_price_key
                    
            elif Distributor_key in ['boribori']:   
                try:
                    product_id_re = re.compile('(?<=productNo=).+')
                    product_id = product_id_re.findall(User_url)[0]  
                    User_url_api = 'https://cf-api.halfclub.com/product/products/productPrice/' + str(product_id)+ '?_=1660813364279&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2' 
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['data']['selPrc'] 
                    except:
                        try:
                            Lower_price_key = result_dict['data']['price']
                        except:
                            try: 
                                Lower_price_key = result_dict['data']['normPrc']
                            except:
                                Lower_price_key = Lower_price_key

                except:
                    product_id_re = re.compile('(?<=PrdNo=)\d+')
                    product_id = product_id_re.findall(User_url)[0]  
                    User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2&ts=1660814208352'

                    print(User_url_api)

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try: 
                        Lower_price_key = result_dict['data']['productPrice']['price']
                    except:
                        Lower_price_key = Lower_price_key

            elif Distributor_key in ['dailyhotel']: 
                try:
                    product_id_re = re.compile('(?<=activity\/)[0-9]{2,10}[(?=?)]?')
                    product_id = product_id_re.findall(User_url)[0]
                    User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v1/activity/deals/' + product_id

                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['data']['daOptionGroups'][0]['daOptions'][0]['discount']
                    except:
                        Lower_price_key = result_dict['data']['daOptionGroups'][0]['daOptions'][0]['price']
                except:
                      Lower_price_key = Lower_price_key
                        

    #최저가가
            # Hosting 주요 3개사 및 일반 최저가 태그 지정
            else:
                print('해당 플랫폼 최저가 미지정 -> 호스팅 3사 최저가 태그 탐색')
                try:# cafe24
                    Lower_price_key = soup.select_one('#span_product_price_text').text
                except:
                    try:# NHN커머스
                        Lower_price_key = soup.select_one(
                            '#frmView > div > div > div.item_detail_list > dl.item_price').text
                    except:
                        try:# 코리아센터
                            Lower_price_key = soup.select_one('span.price').text
                        except:
                            try:
                                Lower_price_key = soup.select_one('.price').text
                            except:
                                try:
                                    Lower_price_key = soup.select_one('span.priceArea_price__ombaK.active').text
                                except:
                                    print('최저가 기본 태그탐색 필요')
                                    Lower_price_key = Lower_price_key
        except: # 기본 bs 최저가 크롤링 설정
            print('최저가 기본 태그 탐색')
            try:# 일반
                Lower_price_key = soup.select_one('meta[property="og:price:amount"]')['content']
            except:
                try:
                    Lower_price_key = soup.select_one('meta[property="og:price"]')['content']
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="product:price:amount"]')['content']
                    except:
                        try:
                            Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                        except:
                            try:# cafe24
                                Lower_price_key = soup.select_one('#span_product_price_text').text
                            except:
                                try:# NHN커머스
                                    Lower_price_key = soup.select_one(
                                        '#frmView > div > div > div.item_detail_list > dl.item_price').text
                                except:
                                    try:# 코리아센터
                                        Lower_price_key = soup.select_one('span.price').text
                                    except:
                                        try:
                                            Lower_price_key = soup.select_one('.price').text
                                        except:
                                            try:
                                                Lower_price_key = soup.select_one('span.priceArea_price__ombaK.active').text
                                            except:
                                                Lower_price_key = "해당 링크에서 직접 보기"   

        # Lower_price_key 전처리
        print("Lower_price_key 전처리 전 값은? ", Lower_price_key)
        # 단위 변환
        no_unit_change_list = ['amazon']    
        if Distributor_key in no_unit_change_list:
            try:
                naver_exchange = 'https://search.naver.com/search.naver?sm=tab_sug.ase&where=nexearch&query=%EB%8B%AC%EB%9F%AC+%ED%99%98%EC%9C%A8'
                res = requests.get(naver_exchange, headers=headers) 
                soup = BeautifulSoup(res.content, 'html.parser')
                try:
                    naver_usd = soup.select_one('span.spt_con.up > strong').text.strip().replace(',','')
                except:
                    naver_usd = soup.select_one('span.spt_con.dw > strong').text.strip().replace(',','')
                Lower_price_key = str(int(round((float(Lower_price_key) * float(naver_usd)),0)))
                print("달러 환율 적용한 Lower_price_key 값은? ", Lower_price_key)
            except:
                Lower_price_key = Lower_price_key
        else:
            try:
                Lower_price_key = str(int(Lower_price_key)).strip().replace('원','')
            except:
                Lower_price_key = Lower_price_key
            Lower_price_key = re.sub(r'(\s)', '', Lower_price_key)

            price_unit_dict = {'십':'0', '백':'00', '천':'000', '만':'0000', '십만':'00000', '백만':'000000', '천만':'0000000', '억':'00000000', '십억':'000000000','백억':'0000000000', '천억':'00000000000'}

            for unit_key in price_unit_dict.keys():
                if unit_key in Lower_price_key:           
                    Lower_price_key_units = Lower_price_key.replace(unit_key, price_unit_dict.get(unit_key))
                else:
                    Lower_price_key = Lower_price_key

            try:
                Lower_price_key = re.sub(r'([^0-9\/]*?)', '', Lower_price_key_units)
            except:
                try:
                    Lower_price_key = re.sub(r'([^0-9\/]*?)', '', Lower_price_key)
                except:
                    Lower_price_key = Lower_price_key

            print("price_unit 변환된 값은? ", Lower_price_key)
            # 아래 고도화 필요... 필요/불가 구분은 했지만 결국 로직을 따라가보면 실패한 것은 '해당~직접보기'로 되어 '확인필요'로 귀결
            if Lower_price_key == "":
                Lower_price_key = "확인필요"
            elif Lower_price_key == "해당링크에서직접보기":
                Lower_price_key = "확인불가"
            else:
                try:
                    Lower_price_key = int(Lower_price_key)
                except:
                    Lower_price_key = Lower_price_key

        Lower_price.append(Lower_price_key)
        print('Lower_price 리스트 값은, ', Lower_price)

        # 네이버 쇼핑 값일 경우 최저몰도 함께 출력

        if 'naver.com' in User_url and Type == '위시':

            Lower_mall.append(Lower_mall_key)
            print('Lower_mall 리스트 값은, ' , Lower_mall)

    #no_searched 셋팅(Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓, 기타 단독상품))

        no_searched_keywords = ['확인불가', '확인필요', 'car.', 'land.', 'dabang', 'myrealtrip', 'mangoplate', 'karrotmarket', 
                                'town.daangn', 'ogqmarket', 'goodchoice']    # 'car' -> 'cartier'와 같은 경우를 피하기 위해, 끝나는 마침표를 꼭 찍어줄 것
        if any(no_searched_keyword in User_url + str(Lower_price_key) for no_searched_keyword in no_searched_keywords) == False:
            print("전후처리 전 Title_key값은 ", Title_key)

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
                                     'CJ런칭', '단하루', '핫딜', 'upto50', '신상출시', '단독기획', '예쁜템들 모여사는  스토어']
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
            pattern2 = re.compile('''(((?=[A-Z0-9])(?=[A-Za-z0-9]*?[A-Z])(?=[A-Za-z0-9]*?[0-9])[A-Za-z0-9]{6,})|
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

                Title_searched_key = "확인필요"
                Lower_price_searched_key = "확인필요"
                Lower_mall_searched_key = "확인필요"
                Lower_url_searched_key = "확인필요"

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
                try:
                    #최저가 검색: Title_pre or Title_post 를 활용하여 네이버 쇼핑 1순위(광고 제외) 검색 후 타이틀, 최저가, 최저가몰, URL 추출
                    User_url_naver = 'https://search.shopping.naver.com/search/all?query=' + str(Title_chosen_key)
                    print("네이버쇼핑 검색 결과 주소?", User_url_naver)

                    headers = {'user-agent': generate_user_agent(device_type='smartphone')}
                    res = requests.get(User_url_naver, headers=headers) 
                    print("네이버쇼핑 검색 결과접속 상태?", res.status_code)
                    soup = BeautifulSoup(res.content, 'html.parser')

                    script = soup.select_one('script[type="application/json"]').text
                    dict_result_script_text = json.loads(str(script))
                    naver_shopping_list_dict_list =  dict_result_script_text['props']['pageProps']['initialState']['products']['list'][0:]
                    if naver_shopping_list_dict_list:
                        for naver_shopping_list_dict_list_item in naver_shopping_list_dict_list:
                            naver_shopping_list_dict_list_item = naver_shopping_list_dict_list_item['item']
                            if naver_shopping_list_dict_list_item.get('adId') == None:  
                                try:
                                    Title_searched_key = naver_shopping_list_dict_list_item.get('productTitle')
                                except:
                                    try:
                                        Title_searched_key = naver_shopping_list_dict_list_item.get('productTitleOrg')
                                    except:
                                        Title_searched_key = naver_shopping_list_dict_list_item.get('productName')

                                try:
                                    Lower_price_searched_key = naver_shopping_list_dict_list_item.get('lowPrice')
                                except:
                                    Lower_price_searched_key = naver_shopping_list_dict_list_item.get('mobilePrice')

                                try:
                                    Lower_mall_searched_key = naver_shopping_list_dict_list_item['lowMallList'][0]['name']
                                except:
                                    try:
                                        Lower_mall_searched_key = naver_shopping_list_dict_list_item['lowMallList'][0]['chnlName']
                                    except:
                                        try:
                                            Lower_mall_searched_key = naver_shopping_list_dict_list_item['mallName']
                                        except:
                                            Lower_mall_searched_key = naver_shopping_list_dict_list_item['mallNameOrg']

                                Lower_url_searched_key = naver_shopping_list_dict_list_item['purchaseConditionInfos'][0]['crUrl']

                            break;          
                    else:
                        Title_searched_key = '검색결과 없음'
                        Lower_price_searched_key = '검색결과 없음'
                        Lower_mall_searched_key = '검색결과 없음'
                        Lower_url_searched_key = '검색결과 없음'
        #         # ip 차단으로 인해 하기 코드 사용 불가
        #             User_url_api = 'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query=' + str(Title_chosen_key) + '&origQuery=' + str(Title_chosen_key)+ '&iq=&eq=&xq='

        #             print(User_url_api)
        # #             headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
        #             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

        #             res_api = requests.get(User_url_api, timeout=3, headers=headers) 

        #             if res_api.status_code != 200:
        #                 print("User_url_api 접속 오류입니다")

        #             res_api_json = json.loads(res_api.text)
        #     # 설명 9번
        #             #meta값
        #             try:
        #                 Title_searched_key = res_api_json['shoppingResult']['products'][0]['productTitle']
        #             except:
        #                 Title_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_price_searched_key = res_api_json['shoppingResult']['products'][0]['mobileLowPrice'] 
        #             except:
        #                 Lower_price_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['lowMallList'][0]['name']
        #             except:
        #                 try:
        #                     Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['mallName']
        #                 except:
        #                     Lower_mall_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_url_searched_key = res_api_json['shoppingResult']['products'][0]['crUrl']
        #             except:
        #                 Lower_url_searched_key = "조금 더 찾아봐야해요!"

        #             print("네이버 쇼핑 최저가는, ", Lower_price_searched_key)

                except: #naver_open_api - 25,000회/1일 접속 가능
                    print('naver_open_api 접속 시도')
                    naver_open_api = 'https://openapi.naver.com/v1/search/shop.json?query=' + Title_chosen_key + '&display=1'
                    print('naver_open_api? ', naver_open_api)
                    headers_naver_open_api = {'user-agent': generate_user_agent(device_type='smartphone'), "X-Naver-Client-Id":'kGjLkvRUDvR3yo09JJoV', "X-Naver-Client-Secret":'NLXuKVy6GG'}
                    res_api = requests.get(naver_open_api, headers=headers_naver_open_api)

                    if res_api.status_code != 200:
                        print('naver_open_api 접속 오류')
                    else:
                        print('naver_open_api 접속 완료')
                        result_dict = json.loads(res_api.text)
                        try:
                            Title_searched_key = result_dict['items'][0]['title']
                            Title_searched_key_trash_words = ['<b>', '</b>']
                            for Title_searched_key_trash_word in Title_searched_key_trash_words:
                                Title_searched_key = Title_searched_key.replace(Title_searched_key_trash_word, "")
                        except:
                            Title_searched_key = '확인필요'
                        try:
                            Lower_price_searched_key = result_dict['items'][0]['lprice']
                        except:
                            Lower_price_searched_key = '확인필요'
                        try:
                            Lower_mall_searched_key = result_dict['items'][0]['mallName']
                        except:
                            Lower_mall_searched_key = Lower_mall_searched_key
                        try:
                            Lower_url_searched_key = result_dict['items'][0]['link']
                        except:
                            Lower_url_searched_key = '확인필요'
                            
                        try: #gate주소가 아닌  naver_catalog 주소 파악
                            product_id_naver_mall_url_re = re.compile('(?<=id=)[0-9]+')
                            product_id_naver_mall_url = product_id_naver_mall_url_re.findall(Lower_url_searched_key)[0]
                            Lower_url_searched_key_temp = 'https://search.shopping.naver.com/catalog/' + str(product_id_naver_mall_url)
                            res = requests.get(Lower_url_searched_key_temp, timeout=3, headers=headers) 
                            soup = BeautifulSoup(res.text, 'html.parser')
                            if '존재하지 않습니다' in str(soup): 
                                print('Lower_url_searched_key_temp는 gate 주소, mall 직접 연결할 주소 파악 시작')
                                res = requests.get(Lower_url_searched_key, timeout=3, headers=headers) 
                                soup = BeautifulSoup(res.text, 'html.parser')
                                script_text = soup.select_one('script[type="application/json"]').text
                                dict_result_script_text = json.loads(script_text)
                                Lower_url_searched_key = dict_result_script_text['props']['pageProps']['product']['productUrl']
                            else:
                                print('naver_catalog 주소 파악')
                                Lower_url_searched_key = Lower_url_searched_key_temp           
                        except:
                            print('naver_catalog 주소 파악')
                            Lower_url_searched_key = Lower_url_searched_key

            # Lower_price_searched_key 전처리

            Lower_price_searched_key = str(Lower_price_searched_key).strip()

            Lower_price_searched_key = re.sub(r'([^0-9]*?)', '', Lower_price_searched_key)

            if Lower_price_searched_key == "":

                Lower_price_searched_key = "검색결과 없음"

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
            
        else:
            if Lower_price_key == '확인필요':
                Title_searched_key = '확인필요'
                Lower_price_searched_key = '확인필요'
                Lower_mall_searched_key = '확인필요'
                Lower_url_searched_key = '확인필요'
            else:
                Title_searched_key = '-'
                Lower_price_searched_key = '-'
                Lower_mall_searched_key = '-'
                Lower_url_searched_key = '-'
    else:
        print('Lower_price_key 탐색 불필요 영역, 공백 처리')
        Lower_price_key = '-'
        Lower_price.append(Lower_price_key)
        print('Lower_price는? ', Lower_price)
        
        Title_searched_key = '-'
        Lower_price_searched_key = '-'
        Lower_mall_searched_key = '-'
        Lower_url_searched_key = '-'

    Title_searched.append(Title_searched_key) #프론트에 안나옴
    Lower_price_searched.append(Lower_price_searched_key)
    Lower_mall_searched.append(Lower_mall_searched_key)
    Lower_url_searched.append(Lower_url_searched_key)

    print("프론트에 안나옴, Title_searched는 ", Title_searched)
    print("Lower_price_searched는 ", Lower_price_searched)
    print("Lower_mall_searched는 ", Lower_mall_searched)
    print("Lower_url_searched는 ", Lower_url_searched)
try:
    Distributor_key = Distributor_keyword_list_Kor_dict[Distributor_key]
except:
    pass

print("최종 또는 한글화 Distributor 값은 ", Distributor_key)
Distributor.append(Distributor_key)

print("scraping complete")

# 설명 10번

# 폐쇄
# DB_input

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched


# for list_one in all_list:
#     if len(list_one) == 0:
#         list_one.append("no_data")

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId)

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, createdAt, updatedAt, UserId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)"

# cur.execute(sql, all_list_tuple)

# db.commit()
# print("load complete")

# db.close()


# 라니 오픈 (제이 클로즈)

# DB_input


import datetime

dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
createdAt = dt_kst
updatedAt = dt_kst

all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched

for list_one in all_list:
    if len(list_one) == 0:
        list_one.append("no_data")

#DB 주의사항: all_list_tuple과 sql의 'INSERT INTO post ( 컬럼 )'의 인자들 순서를 동일하게 설정해야 함 (DB 내 칼럼 순서와 일치하지 않아도 됨)
#다만, DB의 칼럼과 칼럼 명이 다르거나, DB에 칼럼을 새로 생성한다면, all_list_tuple과 sql에도 해당 인자를 추가해야 함

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId)

# sql = "INSERT INTO posts (Type, Categhttp://itempage3.auction.co.kr/DetailView.aspx?itemno=C266635064ory_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, createdAt, updatedAt, UserId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)"
all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt)

sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cur.execute(sql, all_list_tuple)

db.commit() 
print("save complete")

db.close()

