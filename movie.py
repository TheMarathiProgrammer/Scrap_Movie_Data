import requests
from bs4 import BeautifulSoup as bs 
import sqlite3

r = requests.get('https://www.imdb.com/search/title/?title_type=feature&year=2019-01-01,2019-12-31&start=1&ref_=adv_nxt')
html_code = bs(r.content)

div = html_code.find('div',attrs={'class':'lister-list'})
print(div)

m=div.select('div.lister-item-content h3 a')
Movie_name = [i.get_text() for i in m]

d = div.select('span.runtime')
Duration = [i.get_text() for i in d]

c= div.select('span.genre')
Category = [i.get_text().replace('\n','') for i in c]
Category = [i.replace('   ','') for i in Category]

r = div.select('strong')
Ratings = [i.get_text() for i in r]
# print(Ratings)

conn = sqlite3.connect('Movies_data_2019.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Movies(Movie_name TEXT,Duration TEXT,Category TEXT,Ratings TEXT)')

for i in range(len(Movie_name)):
	cursor.execute('INSERT INTO Movies(Movie_name,Duration,Category,Ratings)VALUES(?,?,?,?)',(Movie_name[i],Duration[i],Category[i],Ratings[i]))
conn.commit()
