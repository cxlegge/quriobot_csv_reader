# modules for the plotting and data-based functions
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import re
import numpy as np
import operator as op
# used for the wordcloud generator
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# sets the path to the source file, where 'qdata.csv' is the filename
# and 'qdbdatasysxp.txt' is the text file destination
qread = pd.read_csv('qdata.csv', index_col=False)
targetcols = ['col1', 'col2', 'col3']
f = open('results.txt', 'w+')

def colread(fileread, targetcols, f): # loops through targetcols, writes counts of column to file, bounded by 20 dashes
    # normalises the text to lower case in a holding list
    for targetcol in targetcols:
        list1 = []
        for i in list((fileread.loc[:,targetcol])):
            try:
                list1.append(i.lower())
            except:
                pass
        # writes header with column title, bounded by 20 dashes
        f.write(('-'*20) + '\n' + targetcol + ' total: ' + str(len(list1)) + '\n' + ('-'*20) + '\n')
        # creates dictionary where key = text and value = count of it in column
        groupdict = {}
        for i in list1:
            if str(i) != 'nan':
                if i not in groupdict:
                    groupdict[i] = list1.count(i)
        groupdict_x = sorted(groupdict.items(), key=op.itemgetter(1), reverse=True)
        pos = 1
        for u in groupdict_x: # writes the key/value pairs
            f.write(str(pos) + '.' + str(u[0]) + ' : ' + str(u[1]) + '\n')
            pos += 1

def lowrate(fileread, f): # appends a list of all general queries that led to a rating of 1 or 2 out of 4
    # sorts ratings by value in new Series then adds 1s and 2s together
    filereadsort = fileread.sort_values(by='column_name')
    lowratings = list(filereadsort.loc[:,'column_name'])
    lowratingscount = (lowratings.count(1) + lowratings.count(2))
    # creates Series from the ratings column indices 0 - (number of low ratings counted earlier)
    final_low = (filereadsort.iloc[:(lowratingscount)-1,26])
    # creates header with title
    f.write(('-'*20) + '\n' + 'Lowest Rated General Queries (1 or 2 / 4)' + '\n' + ('-'*20) + '\n')
    
    for i in final_low: # finally filters out NaN values and appends to file
        if str(i) != 'nan' :
            f.write(str(i)+'\n')

def averagerate(fileread, f): # appends an average of all user ratings to the txt file, assuming ratings are out of 4
    list1 = []
    for i in list(fileread.loc[:,'column_name']):
        # filters out Nan values, faster than other methods
        if i in range(0,5):
            list1.append(i)
    average = sum(list1)/len(list1)
    f.write("Average Rating: " + str(average))

def rating_plotter(fileread): # plots a bar graph of total numbers of each user rating
    # defines the counter variable and how many ratings exist, needs 'holding' to filter floats/NaNs
    holding = []
    counter = fileread.loc[:,'48. ## RATE ## User Experience']
    for i in counter:
        try:
            holding.append(int(i))
        except:
            pass
    totals = [holding.count(1), holding.count(2), holding.count(3), holding.count(4)+ holding.count(5)]
    ind = np.arange(4)    # the x locations for the groups
    width = 0.45       # the width of the bars: can also be len(x) sequence

    # initialises the graph
    p1 = plt.bar(ind, totals, width)

    #mp.transforms.Bbox(points=True, minposy = 150)
    plt.ylabel('Number of User Ratings')
    plt.title('User Ratings for Quriobot')
    plt.xticks(ind, ('1 star', '2 star', '3 star', '4 star'))
    rects = p1.patches
    # for each bar: Place a label
    for rect in rects:
    # get X and Y placement of label from rect
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        y_value = int(y_value)
        x_value = int(x_value)
        # number of points between bar and label
        space = 3

        label = str(y_value)
        plt.annotate(
            label,                      # use `label` as label
            (x_value, y_value),         # place label at end of the bar
            xytext=(0, space),          # vertically shift label by `space`
            textcoords="offset points", # interpret `xytext` as offset in points
            ha='center')                # horizontally center label
    return plt

def conversion_plotter(fileread): # plots a pie chart of how many chats complete (conversion rate)
    conv = list(fileread.loc[:,'column_name'])
    x = conv.count(True)
    y = conv.count(False)
    sizes = [x,y]
    labels = 'Completed', 'Not Completed'
    explode = (0.5,0)  # only "explode" the 2nd slice (i.e. 'Complete')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Conversion Ratings for Quriobot', pad=20)
    return plt

def word_cloud(fileread): # generates a random word cloud out of general enquiries words
    text = [] # pulls all text input words into one string, filtering out NaN values
    for i in list(fileread.loc[:,'column_name']):
        if str(i) != 'nan':
            text.append(i.lower())
    text1 = ' '.join(text)
    # initialises wordcloud with listed parameters
    wordcloud = WordCloud(background_color='white', height=100, stopwords=None, \
    relative_scaling=0.2, scale=10).generate(text1)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    return plt

def time_day(fileread): # plots a histogram of hours of the day chats are started
    def bins_labels(bins, **kwargs):
        bin_w = (max(bins) - min(bins)) / (len(bins) - 1)
        plt.xticks(np.arange(min(bins)+bin_w/2, max(bins), bin_w), bins, **kwargs)
        plt.xlim(bins[0], bins[-1])

    times = fileread.loc[:,'start']
    list1 = []
    for time in times:
        list1.append(time[11:13]) # 11-13 is the hours slice of the time string
    list1 = sorted(list1)
    bins=range(25)
    plt.hist(list1, align='mid',bins=bins, histtype='step')
    bins_labels(bins, fontsize=10)
    plt.xlabel('Time (24 Hour)')
    plt.ylabel('Number of Chats')
    plt.title('Chats on Hour of Day')
    plt.grid(True, which='major', alpha=0.4)
    return plt

    '2018-10-29T13:52:42Z'

def masterwrite(*writers): # calls all writing functions
    colread(qread, targetcols, f)
    lowrate(qread, f)
    averagerate(qread, f)

def mastergraph(*graphers): # calls all graph functions
    for i in graphers:
        i(qread).show()
        i(qread).savefig('Graph %s.pdf' % i.__name__)
        i(qread).close()

mastergraph(word_cloud, rating_plotter, time_day)
masterwrite(colread, averagerate, lowrate)
