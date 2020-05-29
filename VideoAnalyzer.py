import requests
import os
import time
import xlsxwriter
from bs4 import BeautifulSoup
from datetime import datetime


def get_stats(video):
    trending = None
    content = requests.get(video)
    soup = BeautifulSoup(content.content, "html.parser")
    open("video.html", "w", encoding="utf8").write(content.text)

    forbidden_chars = {'|', '<', '>', ':', '/', '?', '*', '\n'}

    try:
        if soup.find("span", attrs={"class": "standalone-collection-badge-renderer-text"}).text is not None:
            trending = True
    except AttributeError:
        trending = False

    try:
        views = int(soup.find("div", attrs={"class": "watch-view-count"}).text[:-6].replace(",", ""))
    except AttributeError:
        views = get_stats(video)["views"]

    try:
        title = soup.find("span", attrs={"class": "watch-title"}).text
    except AttributeError:
        title = get_stats(video)["title"]

    timestamp = datetime.now()

    for i in forbidden_chars:
        if i in title:
            title = title.replace(i, "")

    stats = {
        "title": title.strip(),
        "views": views,
        "trending": trending,
        "time": timestamp,
    }

    return stats


# url = input("Enter url: ")
url = "https://www.youtube.com/watch?v=NtlksTJK4ys"
vidstats = get_stats(url)
initial = datetime.now()
print(vidstats["title"])

try:
    os.mkdir(vidstats["title"])
    print("Folder made")
except FileExistsError:
    print("Folder exists")

os.chdir(os.getcwd() + "\\" + vidstats["title"])

workbook = xlsxwriter.Workbook('vidstats.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, "INTERVAL")
worksheet.write(0, 1, "VIEWS")
worksheet.write(0, 2, "TRENDING")
print("Worksheet created at: " + os.getcwd())

length = 10
pinged = 0
interval = length
row = pinged + 1
col = 0

while not vidstats["trending"] and pinged != 8640:
    vidstats = get_stats(url)
    worksheet.write(row, col, interval)
    worksheet.write(row, col + 1, vidstats["views"])
    interval += length
    worksheet.write(row, col + 2, vidstats["trending"])
    pinged += 1
    row = pinged + 1
    print("Ping #" + str(pinged))

    print(vidstats)
    time.sleep(length)

if vidstats['trending'] is True:
    worksheet.write(row, col, interval)
    worksheet.write(row, col + 1, vidstats["views"])
    worksheet.write(row, col + 2, vidstats["trending"])
    worksheet.write(row + 1, col + 2, "TIME DELTA")
    worksheet.write(row + 2, col + 2, vidstats["time"] - initial)
    print("Video went trending after " + str(vidstats["time"] - initial))
    workbook.close()
    print(vidstats)
else:
    print("Video did not go trending after " + str(vidstats["time"] - initial))
