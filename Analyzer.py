from Timezone import Timezone
from Channels import Channels
from Chat import Chat
from Functions import Functions
from GPTModel import GPTModel
from imports import *

class Analyzer:
    def __init__(self, tz: Timezone = Timezone(), period: tuple = None, channels: Channels = None):
        self.f = Functions()
        self.tz = tz
        if channels is None:
            channels = Channels(self.tz)
        self.channels = channels
        if period is None:
            period = self.channels.date_range()
        self.period = period
        self.model = GPTModel()
        self.mega = pd.concat([self.filter_period(i) for i in self.channels.objects]).sort_values('Timestamp').reset_index(drop = True)

    def filter_period(self, channel: Chat, reset_index: bool = False) -> pd.DataFrame:
        earliest, latest = self.period
        data = channel.messages(self.tz)
        if len(data) > 0:
            data = data[(data['Timestamp'] <= latest) & (data['Timestamp'] >= earliest)] #not inclusive
        if reset_index:
            data = data.reset_index()
        return data

    def analyze(self):# interacts with the console
        # show time perod
        e, l = self.period
        print(f"Time period of {e} to {l}.")
        print()
        # show channels
        print("The channels considered are the following:")
        print()
        for channel in self.channels.objects:
            print(channel, end = '\n-\n')
        print()
        # show messages number
        print(f'Messages rank during selected time period:')
        print()
        nm = self.num_msgs()
        nums = nm['nums']
        counter = 1
        while len(nums) > 0:
            m = max(nums, key = nums.get)
            print(f"{counter}. {m.channel_name}")
            print(f"Count: {nums[m]}")
            print()
            nums.pop(m)
            counter += 1
        self.plot_msgs()
        print()
        self.plot_wc()
        print()
        self.plot_emoji_count()

    def analyze_text(self):
        e, l = self.period
        nm = self.num_msgs()
        nums = nm['nums']
        m = max(nums, key = nums.get)
        d = self.daily_count().to_dict()[0]
        max_key = max(d, key = d.get)
        general = f"""
        This analysis is given on a time period of {e} to {l}. You messaged in the channel {m.channel_name} the most with a total of {nums[m]} messages. The day you messaged most was {max_key} with {d[max_key]} messages. 
        """
        extra = ""
        s = general + extra
        print(s)
        return s

    def num_msgs(self) -> dict:
        nums = {channel:len(self.filter_period(channel)) for channel in self.channels.objects}  
        return {'nums': nums, 'max': max(nums, key = nums.get)}

    def daily_count(self) -> pd.DataFrame:
        df = None
        for obj in self.channels.objects:
            d = self.filter_period(obj, reset_index = True)
            dtf = obj.count(dr = self.period, data = d, tz = self.tz)
            if df is None:
                df = dtf
                continue
            df += dtf
        return df

    def plot_msgs(self):
        df = self.daily_count()
        plt.figure()
        plt.plot(df.index, df[0])
        plt.title('Messages sent per day')
        plt.xticks(rotation=45, ha="right")
        plt.show()

    def word_count(self, allow: list = [], disallow: list = [], allow_all: bool = False, just_words: bool = False): #allow *always* overrides disallow
        punc = [',', '.', '!', '?', '/', '>', '<', '\'', '"', ';', '(', ')', '-', '~', '#', '$', '%', '^', '&', '*', '[', ']', '{', '}', '=', '+', ':', "_", "|", "@"]
        cwords = ['the','at','there','my','of','than','and','this','an','a','to','from','which','in','or','is','had','by','their','has','its','it','if','but','was','not','for','what','on','all','are','were','as','i'] + disallow
        if allow_all:
            cwords = []        
        cwords = [i for i in cwords if i not in allow]
        punc = [i for i in punc if i not in allow]
        words = []
        for channel in self.channels.objects:
            msgs = self.filter_period(channel)
            for i in msgs.Contents:
                for j in str(i).split(' '):
                    string = ''
                    for k in j:
                        if k not in punc:
                            string += k  
                    if string != '' and string.lower() not in cwords:
                        words.append(string.lower())
        df = pd.DataFrame(words)
        if just_words:
            return words
        return df.value_counts().to_frame()

    def emoji_count(self, just_emojis: bool = False):
        emojis = []
        for channel in self.channels.objects:
            msgs = self.filter_period(channel)
            for i in msgs.Contents:
                for j in str(i).split(' '):
                    for k in j:
                        if emoji.is_emoji(k):
                            emojis.append(k)
        df = pd.DataFrame(emojis)
        if just_emojis:
            return emojis
        return df.value_counts().to_frame()

    def plot_wc(self, percentile = 0.9996, wc_args = {}):
        wc = self.word_count(**wc_args)
        wc = wc[wc[0].quantile(percentile) < wc[0]]
        plt.figure()
        plt.title("Occurences of Words")
        plt.pie(x = wc[0], labels = [i[0] for i in wc.index], autopct='%1.1f%%', startangle=90)
        plt.show()

    def plot_emoji_count(self, percentile = 0.99, ec_args = {}):
        ec = self.emoji_count(**ec_args)
        ec = ec[ec[0].quantile(percentile) < ec[0]]
        plt.figure()
        plt.title("Occurences of Emojis")
        plt.pie(x = ec[0], labels = [i[0] for i in ec.index], autopct='%1.1f%%', startangle=90)
        plt.show()

    def variabilities(self, weighted = False) -> dict:
        if weighted:
            x = sum(self.num_msgs()['nums'].values())
            return {chat : (chat.total_msgs() / x) * float(chat.count().std()/chat.count().mean()) ** 2.5 for chat in self.channels.objects if len(chat.data) > 0}
        return {chat : float(chat.count().std()/chat.count().mean()) for chat in self.channels.objects if len(chat.data) > 0}

    def rank_variabilities(self, min_msgs = 50, weighted = False) -> dict:
        d = self.variabilities(weighted)
        count = 1
        while (len(d) > 0):
            max_key = max(d, key=d.get)
            val = d.pop(max_key)
            if len(max_key.data) >= min_msgs:
                print(f'{count}. {max_key.channel_name}, {val}')
                count += 1

    def frac_from_scaling(self, x):
        if (x < 1):
            raise ValueError("Must be a scale from 1-10")
        return x**4/10000

    def emotions(self, frac = 1, stress = False, prev = None):
        num_msgs = (len(self.mega)*frac)
        distance = (len(self.mega) / num_msgs) // 1
        df = []
        i = 0
        while True:
            df.append(pd.DataFrame(self.mega.iloc[i]).transpose())
            i += int(distance)
            if (i >= len(self.mega)):
                break
        if prev is not None:
            return self.model.predict_large_recurse(prev, stress = stress)
        return self.model.predict_large_recurse(pd.concat(df), stress = stress)

    #attribute: emotions 0-6, stress 7.
    #acrross: years: 0, seasons: 1, months: 2, day of week: 3, time of day: 4, channels: 5
    def score(self, a, attribute, across):
        dfs = self.batch_conditions(a, across)
        l = {}
        if attribute == 7:
            for j, i in dfs.items():
                f = None
                try:
                    f = i[i['stress'] < 0]['stress']
                except:
                    assert False, "the dataframe passed does not have stress"
                if len(i['stress']) == 0:
                    l[j] = 0
                else:
                    score = sum(i['stress'])/len(i['stress'])#sum(f) + sum(i[i['stress'] >= 0]['stress'])# * len(i[i['stress'] >= 0]['stress'])
                    l[j] = score
            return l
        for j, i in dfs.items():
            f = None
            try:
                f = i[i['emotion'] == attribute]
            except:
                assert False, "the dataframe passed does not have emotion"
            if len(i) == 0:
                l[j] = 0.0
            else:
                score = len(f) / len(i)
                l[j] = (score*100)
        return l
    
    def score_minmax(self, a, attribute, across, add_to = {}):
        l = self.score(a, attribute, across)
        a = {'min': min(l, key = l.get), 'max': max(l, key = l.get)}
        add_to[(across, attribute)] = a
        return a
    
    def score_cumulative(self, a, attribute, across):
        a = self.score(a, attribute, across)
        for i in a:
            a[i] = a[i]**2
        b = sum(a.values())
        for i in a:
            a[i] = a[i] / b

        return sum([a[i] * i for i in a])
        
    def form_data(self, a):
        return [self.score_cumulative(a, attribute, across) for attribute in range(8) for across in range(5)]
    
    def form_minmax_data(self, a):
        return {(across, attribute): self.score_minmax(a, attribute, across) for attribute in range(8) for across in range(6)}
    
    def batch_conditions(self, a, across):
        dfs = {}
        if across == 0:
            dates = a['dates'].apply(lambda x: x.year).unique()
            for date in dates:
                dfs[date] = a[a['dates'].apply(lambda x: x.year) == date]
            return dfs
        if across == 1:
            seasons = (3,20), (6,21), (9,23), (12,21)
            y = lambda x: dt.datetime(20, x.month, x.day)
            dfs[0] = (a[(a['dates'].apply(y) <= dt.datetime(20, *seasons[3])) | (a['dates'].apply(y) < dt.datetime(20, *seasons[0]))])
            dfs[1] = (a[(a['dates'].apply(y) >= dt.datetime(20, *seasons[0])) & (a['dates'].apply(y) < dt.datetime(20, *seasons[1]))])
            dfs[2] = (a[(a['dates'].apply(y) >= dt.datetime(20, *seasons[1])) & (a['dates'].apply(y) < dt.datetime(20, *seasons[2]))])
            dfs[3] = (a[(a['dates'].apply(y) >= dt.datetime(20, *seasons[2])) & (a['dates'].apply(y) < dt.datetime(20, *seasons[3]))])
            return dfs
        if across == 2:
            y = lambda x: x.month
            return {i:a[a['dates'].apply(y) == i] for i in range(1, 13)}
        if across == 3:
            y = lambda x: x.weekday()
            return {i: a[a['dates'].apply(y) == i] for i in range(7)}
        if across == 4:
            return {
                0 : a[(a['times'] >= dt.time(1)) & (a['times'] < dt.time(5))],
                1 : a[(a['times'] >= dt.time(5)) & (a['times'] < dt.time(9))],
                2 : a[(a['times'] >= dt.time(9)) & (a['times'] < dt.time(13))],
                3 : a[(a['times'] >= dt.time(13)) & (a['times'] < dt.time(17))],
                4 : a[(a['times'] >= dt.time(17)) & (a['times'] < dt.time(21))],
                5 : a[(a['times'] >= dt.time(21)) | (a['times'] < dt.time(1))]
            }
        if across == 5:
            return {c : a[a['Channel'] == c] for c in a['Channel'].unique()}

    def batches_from_scale(self, num: int) -> int:
        return 10*x**2

    def batches(self, emotions: pd.DataFrame, mpb: int = 0) -> pd.DataFrame:
        i = 0
        n = True
        while n:
            curr_date = emotions['dates'].iloc[i]
            for _ in range(20):
                i+=1
                if i >= len(emotions):
                    n = False
                emotions['dates'].iloc[i] = curr_date
                
    def get_insight(self, attribute, across, score, minmax):
        attribute_index = GPTModel.map
        attribute_index[7] = 'stress'
        across_index = {0: 'year',
                     1: 'season',
                     2: 'month',
                     3: 'day of week',
                     4: 'time of day',
                     5: 'channel'}
        across_index_2 = {
            1: {
                0:'winter',
                1:'spring',
                2:'summer',
                3: 'autumn'
            },
            2: {
                1:'January',
                2:'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June',
                7: 'July',
                8:'August',
                9:'September',
                10:'October',
                11:'November',
                12:'December'
            },
            3: {
                0:'Monday',
                1:'Tuesday',
                2:'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'
            },
            4: {
                0 : 'late night/early morning (1 AM - 5 AM)',
                1 : 'morning (5 AM - 9 AM)',
                2 : 'mid-day (9 AM - 1 PM)',
                3 : 'afternoon (1 PM - 5 PM)',
                4 : 'evening (5 PM - 9 PM)',
                5 : 'night (9 PM - 1 AM)'
            }
        }
        
        l = None
        if across in across_index_2:
            l = across_index_2[across][score]
        else:
            l = score
        
        
        return f"You felt the emotion '{attribute_index[attribute]}' the {'most' if minmax == 'max' else 'least'} in the {across_index[across]}: {l}.\n"
    
    def get_reccomendation(self, attribute, across, score):
        a={1: {
                0:'winter',
                1:'spring',
                2:'summer',
                3: 'autumn'
            },
            2: {
                1:'January',
                2:'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June',
                7: 'July',
                8:'August',
                9:'September',
                10:'October',
                11:'November',
                12:'December'
            },
            3: {
                0:'Monday',
                1:'Tuesday',
                2:'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'
            },
            4: {
                0 : 'late night/early morning (1 AM - 5 AM)',
                1 : 'morning (5 AM - 9 AM)',
                2 : 'mid-day (9 AM - 1 PM)',
                3 : 'afternoon (1 PM - 5 PM)',
                4 : 'evening (5 PM - 9 PM)',
                5 : 'night (9 PM - 1 AM)'
            }
          }
        
    def insights(self, scores = None, recommendations = True, save = True):
        i1 = [1, 4, 5, 7]
        i2 = range(6)
        insights_text = ""
        for attribute in i1:
            for across in i2:
                maxi = scores[(across, attribute)]['max']
                #mini = scores[(across, attribute)]['min']
                insights_text += self.get_insight(attribute, across, maxi, 'max')
                #insights_text += self.get_insight(attribute, across, mini, 'min')
        
        if recommendations:
            insights_text += '\n' + self.model.recommend(insights_text)
        
        if save:
            with open('recommendations.txt', 'w') as f:
                f.write(insights_text)
        
        return insights_text
                
#print(Analyzer().num_msgs())
#an = Analyzer()
#df = an.emotions(frac = 0.00001, stress = False, prev = None)
#df = an.emotions(frac = 0.00001, stress = True, prev = df)
#scores = an.form_minmax_data(df)
#print(an.insights(scores))