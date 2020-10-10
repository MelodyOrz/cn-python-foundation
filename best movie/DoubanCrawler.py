# coding=utf-8
import requests
from bs4 import BeautifulSoup
import expanddouban
import pandas as pd
import codecs 
import csv




def getMovieUrl(category, location):
	url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category,location)
	return url

class Movie:
    # docstring for Movie.
    def __init__(self, name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link    

    def get_array(self):
        return [self.name, self.rate, self.location, self.category, self.info_link,self.cover_link]


def getMovies(category, location):
    # return a list of Movie objects with the given category and location.
    movies = []
    for loc in location:
        html = expanddouban.getHtml(getMovieUrl(category, loc),True)
        soup = BeautifulSoup(html, 'html.parser')
        content_a = soup.find(id='content').find(class_='list-wp').find_all('a', recursive=False)
        for element in content_a:
            M_name = element.find(class_='title').string
            M_rate = element.find(class_='rate').string
            M_location = loc
            M_category = category
            M_info_link = element.get('href')
            M_cover_link = element.find('img').get('src')
            movies.append(Movie(M_name, M_rate, M_location, M_category, M_info_link, M_cover_link).get_array())
            #Save the array
    return movies
#reference: http://discussions.youdaxue.com/t/topic/50499


location_list=[]
url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
html0 = expanddouban.getHtml((url),True)
soup = BeautifulSoup(html0, 'html.parser')
for child in soup.find(class_='tags').find(class_='category').next_sibling.next_sibling:
    location=child.find(class_='tag').get_text()
    if location!='全部地区':
        location_list.append(location)

category = ['科幻','爱情','悬疑']
my_list = getMovies(category[0],location_list) + getMovies(category[1],location_list) + getMovies(category[2],location_list)

#使用codecs.open()指定编码格式，这样导出的文件中文就不会出现乱码
#Use Codecs.open () to specify the encoding format so that the exported file's Chinese characters are not scrambled
with codecs.open('movies.csv','wb','utf_8_sig') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['电影名称','电影评分','电影地区','电影类型','电影页面链接','电影海报图片链接'])
	writer.writerows(my_list)
#reference: https://blog.csdn.net/waple_0820/article/details/70049953
#reference: http://liuyu314.github.io/python/2013/11/26/csv/

def TotalAmount(category):
    url_c = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{}'.format(category)
    html = expanddouban.getHtml((url_c),True)
    soup = BeautifulSoup(html,'html.parser')
    item_c = soup.find(id='content').find(class_='list-wp').find_all(class_='item')
    total_amount = len(item_c)
    return total_amount

L1 = {}
L2 = {}
L3 = {}


for loc in location_list:
    def SinAmount(category):    
        html = expanddouban.getHtml(getMovieUrl(category, loc),True)
        soup = BeautifulSoup(html,'html.parser')
        item = soup.find(id='content').find(class_='list-wp').find_all(class_='item')   
        return len(item)
    
    L1[loc] = SinAmount(category[0])        
    L2[loc] = SinAmount(category[1])       
    L3[loc] = SinAmount(category[2])    
    
SA1 = sorted(L1.items(),key=lambda item:item[1],reverse=True)
SA2 = sorted(L2.items(),key=lambda item:item[1],reverse=True)
SA3 = sorted(L3.items(),key=lambda item:item[1],reverse=True)
#reference: https://blog.csdn.net/tangtanghao511/article/details/47810729


def Per(SA,category):
    Per = SA/TotalAmount(category)
    return Per

Per1_1 = Per(SA1[0][1],category[0])
Per1_2 = Per(SA1[1][1],category[0])
Per1_3 = Per(SA1[2][1],category[0])

Per2_1 = Per(SA2[0][1],category[1])
Per2_2 = Per(SA2[1][1],category[1])
Per2_3 = Per(SA2[2][1],category[1])

Per3_1 = Per(SA3[0][1],category[2])
Per3_2 = Per(SA3[1][1],category[2])
Per3_3 = Per(SA3[2][1],category[2])

with codecs.open('output.txt','w','utf_8_sig') as f:
    f.write("in movie category {}, {},{},{} are three locations with most movie amount, taking part of {:.2%},{:.2%},{:.2%} percent of the total movie amount respectively.".format(category[0],SA1[0][0],SA1[1][0],SA1[2][0],Per1_1,Per1_2,Per1_3) + "\n" + "in movie category {}, {},{},{} are three locations with most movie amount, taking part of {:.2%},{:.2%},{:.2%} percent of the total movie amount respectively.".format(category[1],SA2[0][0],SA2[1][0],SA2[2][0],Per2_1,Per2_2,Per2_3) + "\n" + "in movie category {}, {},{},{} are three locations with most movie amount, taking part of {:.2%},{:.2%},{:.2%} percent of the total movie amount respectively.".format(category[2],SA3[0][0],SA3[1][0],SA3[2][0],Per3_1,Per3_2,Per3_3))



