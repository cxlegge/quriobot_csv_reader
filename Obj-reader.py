#! /user/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import re, numpy as np, operator as op
# used for the wordcloud generator
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# below is a class-object testing section

class ParentClass(object):
    def __init__(self, kwargs):
        self.kwargs = kwargs
    def cleaner(itera):
        for i in itera:
            if str(i).lower() == 'nan':
                itera.remove(i)
class ChildClass(ParentClass):
    def __init__(self):
        super().__init__

myList = [1,2,3,4,5,'NaN']

ChildClass.cleaner(myList)

print(myList)

fileread = pd.read_csv('qdata.csv', index_col=False)

class mastergrapher(object):
    def __init__(self, fileread):
        self.fileread = fileread
    def mgraph(obj, func):
        '''Word_Cloud'''
        func.savefig('{}.pdf'.format(obj.__doc__))
        func.show()
        func.close()

class wordcloud(mastergrapher):
    '''Word Cloud'''
    def __init__(self):
        super().__init__
    def creategraph(fileread):
        '''Word_Cloud''' # generates a random word cloud out of general enquiries words
        text = [] # pulls all text input words into one string, filtering out NaN values
        for i in list(fileread.loc[:,'8. ## INPUT ## Text Input A']):
            if str(i) != 'nan':
                text.append(i.lower())
        text1 = ' '.join(text)
        # initialises wordcloud with listed parameters
        wordcloud = WordCloud(background_color='white', height=100, stopwords=None, \
        relative_scaling=0.2, scale=10).generate(text1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt

class UserRatings(mastergrapher):
    '''User Ratings'''
    def __init__(self):
        super().__init__
    # defines the counter variable and how many ratings exist 
    def creategraph(fileread):
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
        plt.title('User Ratings for FBL chatBot')
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
        #plt.show()
        #plt.savefig("ratings.pdf", bbox_inches='tight')
        return plt

class TimeOfDay(mastergrapher):
    '''Time Of Day'''
    def __init__(self):
        super().__init__
    def creategraph(fileread):
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

#wordcloud.creategraph(fileread)
wordcloud.mgraph(wordcloud, wordcloud.creategraph(fileread))
UserRatings.mgraph(UserRatings, UserRatings.creategraph(fileread))
TimeOfDay.mgraph(TimeOfDay, TimeOfDay.creategraph(fileread))
