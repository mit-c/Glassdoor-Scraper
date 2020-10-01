import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
from bs4 import BeautifulSoup
from datetime import datetime



# make this a function for indeed which takes url and outputs review graph.
def indeed_scraper(url, num_pages):
    url_other = [url + "&start=" + str(i * 20) for i in range(1, num_pages)]  # num pages not num_pages+1 cos first url given before.
    url_list = url_other
    url_list.append(url)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


    times = []
    out_of_5 = []
    for i,url in enumerate(url_list):
        print(str("{:.1f}".format((i / len(url_list) * 100)) + "%"))

        response_content = requests.get(url, headers=headers).content
        soup = BeautifulSoup(response_content,'html.parser')

        reviews = soup.find_all("div", {"class": "cmp-Review-container"})
        for review in reviews:
            the_time_attrs = review.find("span", attrs={"class": "cmp-ReviewAuthor"}).text.split()
            daymonthyear = the_time_attrs[-3]  + the_time_attrs[-2] + the_time_attrs[-1]
            datetime_str = " ".join(the_time_attrs[-3:])
            datetime_obj = datetime.strptime(datetime_str, "%d %B %Y")
            times.append(datetime_obj)
            the_review_attrs = review.find("div", attrs={"class": "cmp-ReviewRating-text"})
            out_of_5.append(float(the_review_attrs.text))


    new_times = matplotlib.dates.date2num(times)

    return new_times, out_of_5


