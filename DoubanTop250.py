import os
import pdfkit
import requests
import requests_html


def GetPosterNumber(base_url):
    photos_url = base_url + 'all_photos'
    r = session.get(photos_url)
    try:
        poster_num = int(r.html.xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/div[1]/h2/span/a")[0].text[1:-1])
    except:
        poster_num = 0
    return poster_num

def Download_image(img_name, img_url):
    print('Download image:', img_name, img_url)
    filename = img_name + 'jpg'
    with open(filename, 'wb') as f:
        r = requests.get(img_url)
        f.write(r.content)

def Download_poster(path, poster_url):
    print('Download poster:', path, poster_url)
    poster_name = poster_url.split('/')[-1]
    filename = os.path.join(path, poster_name)
    with open(filename, 'wb') as f:
        r = requests.get(poster_url)
        f.write(r.content)


URL = 'https://movie.douban.com/top250?&filter='
for i in range(7, 10):
    session = requests_html.HTMLSession()
    params = {'start': str(25 * i)}
    soup = session.get(URL, params=params)
    r = requests.get(URL, params=params)
    pdfkit.from_url(r.url, str(i)+'.pdf')

    aList = soup.html.xpath("//div[@class='article']//div[@class='pic']//a")
    for a in aList:
        base_url = a.attrs['href']

        img = a.find('img')[0]
        img_url = img.attrs['src']
        img_name = img.attrs['alt']
        Download_image(img_name, img_url)

        poster_num = GetPosterNumber(base_url)
        print('Poster number:', poster_num)
        if poster_num == 0:
            continue 

        path = img_name
        if not os.path.exists(path):
            os.mkdir(path)

        for page in range(poster_num // 30 + 1):
            params = {
                'size':  'a',
                'sortby':  'like',
                'start':   str(30 * page),
                'subtype': 'a',
                'type':    'R'}

            poster_url = base_url + 'photos'
            r = session.get(poster_url, params=params)
            urls = r.html.xpath("//div[@class='article']//li//img/@src")
            for poster_url in urls:
                Download_poster(path, poster_url)
