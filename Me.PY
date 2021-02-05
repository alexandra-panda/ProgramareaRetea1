import socket
import time
import re
import requests
import bs4 as bs
import os
import threading
import ssl
import urllib.request
import urllib3


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.connect(("me.utm.md", 80))
    mysocket.sendall(b"GET / HTTP/1.1\r\nHost: me.utm.md\r\n\r\n")

    print(str(mysocket.recv(52), 'utf-8'))


def get_url_images_in_text(source):
    # Finds image's urls
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|gif)', source)

    for x in results:
        if 'http://' not in x:
            x = 'http://me.utm.md' + x
        urls.append(x)
    urls = list(set(urls))
    print('Links of images detected: ' + str(len(urls)))
    return urls


def get_images_from_url(url):
    resp = requests.get(url)
    urls = get_url_images_in_text(resp.text)
    print('\nUrls of images:\n', urls)
    return urls


links = get_images_from_url('http://me.utm.md/')

http = urllib3.PoolManager()

N = 0;
#  Counter that helps to rename the downloaded files
print("Downloading images...")
for link in links:
    r = http.request('GET', link)
    Name = str(N + 1)
    N += 1
    with open("file" + Name + ".png", "wb") as fcont:
        fcont.write(r.data)
print("Download Done!")
