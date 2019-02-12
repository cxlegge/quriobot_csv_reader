#! /user/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np, operator as op
# used for the wordcloud generator
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

fileread = pd.read_csv('qdata.csv', index_col=False)

f = open('quriodata.txt', 'w+')
print(type(fileread))
# class that holds the method for saving, displaying and closing the graphs
class mastergrapher(object):
    def __init__(self, fileread):
        self.fileread = fileread
    def mgraph(obj, func):
        func.savefig('{}.pdf'.format(obj.__doc__))
        func.show()
        func.close()
# obsolete class that ideally would work with other text classes not yet implemented
class masterwriter(object):
    def __init__(self, fileread, f):
        self.fileread = fileread
        self.f = f
    def mwrite(func, f):
        f.write('-'*25 + '\n' + str(func) + '\n')
# creates a wordcloud image
class Wordcloud(mastergrapher):
    '''Word Cloud'''
    def __init__(self):
        super().__init__
    def creategraph(fileread):
        '''Word_Cloud''' # generates a random word cloud out of general enquiries words
        text = [] # pulls all text input words into one string, filtering out NaN values
        # finds the column with the defined text as a label
        first = fileread.filter(regex=("column_name$"))
        for i in list(list(first.iloc[:,0])):
            if str(i) != 'nan':
                text.append(i.lower())
        text1 = ' '.join(text)
        # initialises wordcloud with listed parameters
        wordcloud = WordCloud(background_color='white', height=100, stopwords=None, \
        relative_scaling=0.2, scale=10).generate(text1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt
# creates a user ratings graph
class UserRatings(mastergrapher):
    '''User Ratings'''
    def __init__(self):
        super().__init__
    # finds the column with the defined text as a label
    def creategraph(fileread):
        holding = []
        first = fileread.filter(regex=("column_name$"))
        counter = list(first.iloc[:,0])
        for i in counter:
            try:
                holding.append(int(i))
            except:
                pass
        totals = [holding.count(1), holding.count(2), holding.count(3), holding.count(4)] # change for number of star ratings
        ind = np.arange(4)    # the x locations for the groups
        width = 0.45       # the width of the bars

        # initialises the graph
        p1 = plt.bar(ind, totals, width)

        plt.ylabel('Number of User Ratings')
        plt.title('User Ratings for chatbot')
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
# creates a graph of how many chats occur on each hour
class TimeOfDay(mastergrapher):
    '''Time Of Day'''
    def __init__(self):
        super().__init__
    def creategraph(fileread):
        # defines how column sections (bins) will be placed
        def bins_labels(bins, **kwargs):
            bin_w = (max(bins) - min(bins)) / (len(bins) - 1)
            plt.xticks(np.arange(min(bins)+bin_w/2, max(bins), bin_w), bins, **kwargs)
            plt.xlim(bins[0], bins[-1])
        first = fileread.filter(regex=("start$"))
        times = list(first.iloc[:,0])
        list1 = []
        for time in times:
            list1.append(time[11:13]) # 11-13 is the "hours" slice of the time string
        list1 = sorted(list1)
        bins=range(25)
        # initialises the histogram with labels
        plt.hist(list1, align='mid',bins=bins, histtype='step')
        bins_labels(bins, fontsize=10)
        plt.xlabel('Time (24 Hour)')
        plt.ylabel('Number of Chats')
        plt.title('Chats on Hour of Day')
        plt.grid(True, which='major', alpha=0.4)
        return plt
# creates a text file which holds the queries from users
class ColumnRead(masterwriter):
    def __init__(self):
        super().__init__
    def createwrite(fileread, f):
        targetcols = ['column_name1','column_name2']
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
# creates a pie chart of multiple choice ratios
class UserType(mastergrapher):
    '''Ratio Graph'''
    def __init__(self):
        super().__init__
    def creategraph(fileread):
        # finds the column with the defined text as a label
        first = fileread.filter(regex=("column_name$"))
        types = list(first.iloc[:,0])
        options = []
        counts = []
        labels = []
        # finds unique string-type values and adds them to 'options'
        for i in types:
            if type(i) == str and (i not in options):
                options.append(i)
        # adds the counts of occurences of each options item in the column
        # then adds the label string to the 'labels' list without []
        for v in options:
            counts.append(types.count(v))
            labels.append(v[1:len(v)-1])
        print(options)
        sizes = counts
        # labels added in the same order as the option appears
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', pctdistance=0.75, startangle=180)
        plt.title('Ratios', pad=10)
        return plt
Wordcloud.mgraph(Wordcloud, Wordcloud.creategraph(fileread))
UserRatings.mgraph(UserRatings, UserRatings.creategraph(fileread))
TimeOfDay.mgraph(TimeOfDay, TimeOfDay.creategraph(fileread))
ColumnRead.createwrite(fileread, f)
UserType.mgraph(UserType, UserType.creategraph(fileread))
