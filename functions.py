import requests, random, re
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
    day_n=int(str(str(new).split(' ')[0]).split('-')[2])
    day_o=int(str(str(old).split(' ')[0]).split('-')[2])
    month_n=int(str(str(new).split(' ')[0]).split('-')[1])
    month_o=int(str(str(old).split(' ')[0]).split('-')[1])
    year_n=int(str(str(new).split(' ')[0]).split('-')[0])
    year_o=int(str(str(old).split(' ')[0]).split('-')[0])
    days_total=(day_n-day_o)+((month_n-month_o)*30)+((year_n-year_o)*365)
    year_delta, days_total=divmod(days_total, 365)
    month_delta, day_delta=divmod(days_total, 30)
    return f'{year_delta} years, {month_delta} months, {day_delta} days'

def cwemmentize(msg):
    return str(msg).replace('r', 'w').replace('l', 'w').replace('s', 'sh').replace('x','gz').replace('o','ow')

def poll(syntax):
    title=re.search('\(.*\)', str(syntax)).group(0).replace('(', '').replace(')', '')
    description=re.search('\{.*\}', str(syntax)).group(0).replace('{','').replace('}','')
    options=re.search('\[.*\]', str(syntax)).group(0).replace('[','').replace(']','').split(';')
    n_options=len(options)
    if n_options>10 or n_options<1:
        return None
    return title, description, options, n_options