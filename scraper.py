import requests
import json
import time

def getPushshiftData(after, before, subreddit):
    """
    https://pushshift.io/api-parameters/
    """
    sampleSize = 10

    url = (
        'https://api.pushshift.io/reddit/comment/search/?'
        +'&size='
        +str(sampleSize)
        +'&after='
        +str(after)
        +'&before='
        +str(before)
        +'&subreddit='
        +str(subreddit)
    )
    print(url)
    r = requests.get(url)
    try:
        data = json.loads(r.text)
    except:
        print(r.text)
    return data['data']



sub= 'bitcoin'

# 1 day
increment = 86400

# 1 day
window = 86400

# 01/01/2019 @ 12:00am (UTC)
end = 1546300800

# 01/01/2018 @ 12:00am (UTC)
start = 1514764800
cur = start

data = []

count = 0
while cur < end:
    curData = getPushshiftData(cur, cur + window, sub)

    data.extend(curData)
    cur += increment
    count += 1

    time.sleep(1)

print(count)

with open('result.json', 'w') as fp:
    fp.truncate(0)
    json.dump(data, fp)