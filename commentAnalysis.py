import json
from textblob import TextBlob
from datetime import datetime
import csv
import pandas
import matplotlib.pyplot as plt

# process comments
with open('results_2018_2019.json') as json_file:
    comments = json.load(json_file)

commentsSentiment = []

for comment in comments:
    time = comment['created_utc']
    textBlobBody = TextBlob(comment['body'])

    # get sentiment and convert unix timestamp
    commentsSentiment.append(
        {
            'time': datetime
                .utcfromtimestamp(time)
                .strftime('%Y-%m-%d %H:%M:%S'),
            'polarity': textBlobBody.sentiment.polarity
        }
    )

# process btc history
with open('Coinbase_BTCUSD.csv') as coinbaseFile:
    btcText = coinbaseFile.readlines()

csvScheme = [
    'Date',
    'Symbol',
    'Open',
    'High',
    'Low',
    'Close',
    'Volume BTC',
    'Volume USD',
]

btcDicts = []

for row in btcText:
    btcDict = {}

    for key, value in zip(csvScheme, row.split(',')):
        value = value.strip()

        if  key == 'Close':
            btcDict[key] = float(value)
        else:
            btcDict[key] = value

    btcDicts.append(btcDict)

btcPriceDF = pandas.DataFrame(btcDicts).reset_index()
pricePlot = btcPriceDF.plot(x='index', y='Close', kind = 'line')
pricePlot.invert_xaxis()

print(btcPriceDF)
plt.show()

commentDF = pandas.DataFrame(commentsSentiment).reset_index()
commentPlot = commentDF.plot(x='index', y='polarity', kind = 'scatter')

print(commentDF)
plt.show()


commentDF['movingAvg'] = commentDF.rolling(window=70)['polarity'].mean()
commentPlot2 = commentDF.plot(x='index', y='movingAvg', kind = 'line')
print(commentDF)
plt.show()



# corr check

sampleSize = 10

daliyCommentAverages = []
for i in range(0, len(commentsSentiment), sampleSize):
    subList = commentsSentiment[i:i+sampleSize]
    avg = 0
    for comment in subList:
        avg += comment['polarity']
    avg = avg / sampleSize
    daliyCommentAverages.append(avg)

daliyClose = []
for day in reversed(btcDicts):
    daliyClose.append(day['Close'])


combinend = []
for avg, close in zip(daliyCommentAverages, daliyClose):
    combinend.append((avg,close))


pairedCommentPriceDF = pandas.DataFrame(combinend)

corr = pairedCommentPriceDF.corr()

print(pairedCommentPriceDF)
print(corr)