import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
from bs4 import BeautifulSoup
from datetime import datetime


def glassdoor_scraper(url, num_pages):
    url_list = [url[:-4] + "_P" + str(i) + ".htm" for i in range(2, num_pages + 1)]
    url_list.append(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
    times = []
    out_of_5 = []
    current_employee_list = []
    count = 0
    for url in url_list:
        try:
            response_content = requests.get(url, headers=headers).content
        except:
            print("error 1")
            continue
        soup = BeautifulSoup(response_content, 'html.parser')
        try:
            reviews = soup.find("div", id="ReviewsFeed")
        except:
            continue
            print("error 2")
        try:
            reviews = reviews.find_all("li", attrs={"class": "empReview cf"})
        except:
            print("error 3")
            continue

        count += 1
        percentage = int(count / len(url_list) * 100)
        if (percentage % 1 == 0):
            print(percentage, '%')
        for review in reviews:

            try:
                the_time_attrs = review.find("time", attrs={"class": "date subtle small"}).attrs
            except:
                continue
            try:
                current_employee = review.find("span", attrs={"class": "authorJobTitle middle"})
            except:
                continue
            current_employee_list.append("Former Employee" not in current_employee.text) # list which says true if current employee. Assumed to be current if not former.
            time_str = the_time_attrs['datetime']
            datetime_obj = datetime.strptime(time_str[:33], "%a %b %d %Y %H:%M:%S %Z%z")
            the_review = review.find("div", attrs={
                "class": "v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__small"})
            review_txt = float(the_review.text)
            times.append(datetime_obj)
            out_of_5.append(review_txt)

    months = matplotlib.dates.MonthLocator()
    years = matplotlib.dates.YearLocator()
    format = matplotlib.dates.DateFormatter('%d %B %Y')  # format for plot

    new_times = matplotlib.dates.date2num(times)
    return new_times, out_of_5, current_employee_list
