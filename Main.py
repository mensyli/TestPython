import requests
from lxml import html
import re
import os
import time
import random
import config


def get_page_number(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    urls = []
    for i in selector.xpath("//ul/li/a/@href"):
        urls.append(i)
    return urls


def get_image_title(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_title = selector.xpath("//h2/text()")[0]
    return image_title

def get_image_amount(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    return image_amount


def get_image_detail_website(url):
    image_detail_websites = []
    image_amount = get_image_amount(url)
    for i in range(int(image_amount)):
        image_detail_link = '{}/{}'.format(url,i+1)
        response = requests.get(image_detail_link)
        if response.status_code == 200:
            selector = html.fromstring(response.content)
            image_download_link = selector.xpath("//div[@class='content']/a/img/@src")[0]
            image_detail_websites.append(image_download_link)
    return  image_detail_websites

def download_image(image_title, image_detail_websites):
    num = 1
    amount = len(image_detail_websites)
    path = '/home/mensyli/Pictures/temp/' + image_title
    for i in image_detail_websites:
        response = requests.get(url=i, headers=config.get_header())
        if response.status_code == 200:
            if not os.path.exists(path):
                os.makedirs(path)
                os.chdir('/home/mensyli/Pictures/temp/' + image_title)
            filename = '%s%s.jpg' % (image_title,num)
            print('正在下载图片：%s第%s/%s,' % (image_title, num, amount))
            with open(filename, 'wb') as f:
                f.write(response.content)
                time.sleep(random.uniform(0.5, 3))
            num += 1

def get_imageset_page_number(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    imageset_amount = selector.xpath("//div[@class='page']/a[last()]/@href") # list
    total_number = re.findall(r"[0-9]{2}", "".join(imageset_amount)) # list
    return "".join(total_number)

def get_imageset_detail_websites(url):
    imageset_detail_websites = []
    imageset_amount = get_imageset_page_number(url)
    for i in range(int(imageset_amount)):
        imageset_detail_link = '{}/home/{}'.format(url, i+1)
        imageset_detail_websites.append(imageset_detail_link)
    return imageset_detail_websites

if __name__ == '__main__':
    url = 'http://www.mmjpg.com'
    imageset_detail_websites = get_imageset_detail_websites(url)
    counter = 1
    page = 1
    for link in imageset_detail_websites:
        print("正在下载第%s页图集" % page)
        for i in get_page_number(link):
            print("正在下载图集%s" % counter)
            download_image(get_image_title(i), get_image_detail_website(i))
            counter += 1
            time.sleep(random.uniform(5, 10))
        page += 1