import indeed_scraper as indeed
import glassdoor_scraper as glass
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime
from matplotlib.ticker import MaxNLocator
import scipy.stats as stats
import seaborn as sns; sns.set()
import pandas as pd
import csv


def plot_time_scores(times,scores):
    format = matplotlib.dates.DateFormatter('%d %B %Y')

    fig, ax = plt.subplots()
    ax.scatter(times, scores, s=1)
    L = len(scores)
    plt.title("Plot of " + str(L) + " reviews")
    ax.xaxis.set_major_formatter(format)
    fig.autofmt_xdate()
    plt.show()
    return fig, ax

def plot_hist_times(times, scores):
    format = matplotlib.dates.DateFormatter('%d %B %Y')
    fig, ax = plt.subplots()
    plt.hist(times, bins=25)
    ax.xaxis.set_major_formatter(format)
    plt.show()
    return fig, ax

def plot_hist_scores(times,scores):
    fig, ax = plt.subplots()
    plt.hist(scores, bins=[1,2,3,4,5])
    plt.show()
    return fig, ax


def sort_times_scores(times,scores):
    times_scores = zip(times,scores)
    sorted_by_time = sorted(times_scores, key=lambda tuple: tuple[0])
    times = [time for time,score in sorted_by_time]
    scores = [score for time,score in sorted_by_time]
    return times,scores


def plot_moving_average(unsort_times, unsort_scores, step):
    if(step % 2 == 0):
        print("use even step")
    times,scores = sort_times_scores(unsort_times,unsort_scores)
    format = matplotlib.dates.DateFormatter('%d %B %Y')
    #fig, ax = plt.subplots()
    moving_average_score = []
    moving_time = times[((step)//2)  :-(step)//2 + 1] # for simplicity assuming odd window size.
    # if step is 10 then the first datapoint is at 5th point of array so we lose (n-2) points
    # xoo oox
    # 012-321
    num_windows = len(moving_time)
    i=0
    while i < len(scores) - step + 1:
        this_window = scores[i : i+step]
        window_avg = sum(this_window) / step
        moving_average_score.append(window_avg)
        i+=1

    df = pd.DataFrame({"Time": moving_time, "Score": moving_average_score})
    print(df.head())
    ax = sns.lineplot(x="Time", y="Score", data=df, estimator=None)
    #ax.xaxis.set_major_formatter(format)
    ax.set(ylim=(1,5))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_formatter(format)
    plt.title(str(len(scores)) + " reviews - moving average")
    plt.show()
    return ax

##### Writing csv
def write_file(file_name,url ,num_pages):
    times, scores = glass.glassdoor_scraper(url,num_pages)
    with open(file_name,'w',newline='') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["times","scores"])
        writer.writerows(zip(times,scores))

##### End of writing csv
def read_file(file_name):
    times = []
    scores = []
    # maybe make write / read  csv function
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if(line_count == 0):
                line_count+=1
                continue
            time = row["times"]
            times.append(float(time))
            scores.append(float(row["scores"]))
            line_count += 1
        return times,scores

num_pages = 40
url = "https://www.glassdoor.co.uk/Reviews/Natwest-Reviews-E36971.htm"
write_file("NatWest_scores.csv",url ,num_pages)
times,scores = read_file("NatWest_scores.csv")


plt.scatter(times,scores, s = 5)
plot_moving_average(times, scores, 51)



