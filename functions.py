import requests, random
from bs4 import BeautifulSoup

def daily_quote():
    url='https://www.brainyquote.com/topics/daily-quotes'
    text=requests.get(url).text
    soup=BeautifulSoup(text, 'html.parser')
    quote_blocks=soup.find_all('div', class_='grid-item qb clearfix bqQt')
    quotes=[]
    for block in quote_blocks:
        quote=str(block.find('a', title='view quote').text).strip().replace('\n','')
        author=str(block.find('a', title='view author').text).strip().replace('\n', '')
        if quote!='':
            quotes.append([quote, author])
    inspire=random.choice(quotes)
    return f'"*{inspire[0]}*"\n**-{inspire[1]}**'

def daily_poem():
    url='https://apoemaday.tumblr.com/'
    text=requests.get(url).text
    soup=BeautifulSoup(text, 'html.parser')
    layout=soup.find('div', class_='layout')
    articles=layout.find_all('article')
    poems=[]
    for i in articles:
        title=i.find('h2').text
        author=i.find_all('p')[0].text
        poem=i.find_all('p')[1].get_text("\n")
        poems.append([title, author, poem])
    inspire=random.choice(poems)
    return f'**{inspire[0]}**\n*-by {inspire[1]}*\n\n{inspire[2]}'


def make_ID(uid):
    return int(str(uid).replace('>','').replace('<','').replace('@',''))

def make_time(dto):
    months={
        1 :'January',
        2 :'February',
        3 :'March',
        4 :'April',
        5 :'May',
        6 :'June',
        7 :'July',
        8 :'August',
        9 :'September',
        10:'October',
        11:'November',
        12:'December'
    }
    date_time=str(dto).split(' ')
    date=str(date_time[0]).split('-')
    time=str(date_time[1]).split(':')
    year=date[0]
    month=date[1]
    day=date[2]
    hour=time[0]
    minute=time[1]
    second=time[2]
    return f'{months.get(int(month))} {int(day)}, {year} at {int(hour)}:{int(minute)}:{round(float(second))}'
    
def get_age(new, old):
    year_n=str(str(new).split(' ')[0]).split('-')[0]
    month_n=str(str(new).split(' ')[0]).split('-')[1]
    day_n=str(str(new).split(' ')[0]).split('-')[2]
    year_o=str(str(old).split(' ')[0]).split('-')[0]
    month_o=str(str(old).split(' ')[0]).split('-')[1]
    day_o=str(str(old).split(' ')[0]).split('-')[2]
    return f'{abs(int(year_n)-int(year_o))} years, {abs(int(month_n)-int(month_o))} months, {abs(int(day_n)-int(day_o))} days'

def cwemmentize(msg):
    return str(msg).replace('r', 'w').replace('l', 'w').replace('s', 'sh').replace('x','gz').replace('o','ow')