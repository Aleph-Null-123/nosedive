from imports import *

#later versions
'''def get_key():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    if os.path.exists('~/CherryBlossom/openai_key'):
        with open('~/CherryBlossom/openai_key', 'r') as f:
            return f.read().strip()
    else:
        key = input("Enter your openai key here: ").strip()
        if input('Would you like to store it on your computer so that you do not need to update it again? y/n') == y:
            if not os.path.exists('~/CherryBlossom'):
                os.mkdir('~/CherryBlossom')
            with open('~/CherryBlossom/openai_key', 'w') as f:
                f.write(key)'''
                
openai.api_key = '1'

class TimeoutError(Exception):
    pass

class GPTModel:
    map = {0: "none", 1: "anger", 2: "disgust", 3: "fear", 4: "happiness", 5: "sadness", 6: "surprise"}
    def __init__(self, frac = 0):
        self.MODEL = "gpt-3.5-turbo"

        '''df = None

        for i in Channels(Timezone('LOCAL')).objects:
            df = pd.concat([df, i.data])
        self.df = df.sample(frac = frac).reset_index()
        self.count = 0
        self.start_time = time.time()'''

    def signal_handler(self, signum, frame):
        raise TimeoutError()

    def generate_dataset(self, name):
        predictions = []
        count = 0
        for i in range(len(self.df["Contents"])/20):
            count += 1
            try:
                predictions.append(self.predict_large(self.df["Contents"][i:20], n = count))
            except Exception as e:
                print("errored type 1")
                print(i)
                print(e)
                predictions.append(-1)
                pd.DataFrame(predictions).to_csv("errored1.csv")
                continue
        try:
            self.df['GPT'] = predictions
            self.df.to_csv(name)
        except:
            print("errored type 2")
            pd.DataFrame(predictions).to_csv("errored2.csv")

        return self.df

    '''def test(self):
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": "ur cool"},
                {"role": "user", "content": "print 5"},
                {"role":"assistant", "content":"5"},
                {"role":"user","content":"print 6"},
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]'''

    def predict_large(self, text, stress = False):
        '''signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(2)
        try:
            pass
        except:
            pass
        finally'''
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(10)
        msg1 = 'stress for those texts (ranging from 0 to 5 where 0 is least stressed and 5 is most stressed)'
        msg2 = "['i have an assignment due so soon', 'IM SO STRESSED', 'im busy from 5-7pm', 'haha']"
        msg3 = '8 10 6 2'                                                                                                                                         
        try:
            db.open()
            openai.api_key = db.get_openai_key()
            db.close()
            response = openai.ChatCompletion.create(
                    model=self.MODEL,
                    messages=[
                        {"role": "system", "content": "you are a machine learning model acting as a prediction function"},
                        {"role": "user", "content": f"I will give you a python list of strings, which are text messages. return space-separated integers that represent the \
                        emotions for those texts:" + str("{'0': 'none', '1': 'anger', '2': 'disgust', '3': 'fear', '4': 'happiness', '5': 'sadness', '6': 'surprise'}") if not stress else msg1 + "\
                        do not output anything else, treat this call as a function where you will return a string of integers. \
                        make sure the number of integers returned matches the number of words passed in. this is very important, and if it is not true every time, the app will break.\
                        if you are UNABLE to process one, rather than removing it from the ouptut, default to 0. never diverge from the length of the input. \
                        also do not add new numbers. if the length of the input and the length of the output are different, it is an invalid response, and you MUST check for this and PREVENT it."},
                        #{"role": "user", "content": "Return a single integer that predicts emotion for given text. it can be any of the following {'0': none, '1': anger, '2': disgust, '3': fear, '4': happiness, '5': sadness, '6': surprise}. If you are unable to determine, output 0 by default. However, make sure to not output anything else, as this will compromise the functionality of this app."},
                        #{"role": "user", "content": "DO NOT GENERATE ANYTHING ELSE SUCH AS EXTRA TEXT"},
                        {"role": "assistant", "content": "ok"},
                        {"role": "user", "content": "['i hate you', 'thats so cool!!', 'OH NO', ':(', 'awesome', 'grosss', 'nice']" if not stress else msg2},
                        {"role": "assistant", "content": "1 6 3 5 4 2 0" if not stress else msg3},
                        #{"role": "user", "content": "Return the emotion associated with the following message: asdfgfs"},
                        #{"role": "assistant", "content": "0"},
                        {"role": "user", "content": f"{text}"}
                    ],
                    temperature=0,
                )
            openai.api_key = ''
            signal.alarm(0)
            a = (response["choices"][0]["message"]["content"])
            try:
                a = list(map(int, a.split(' ')))
                if stress:
                    a = [i * 2 - 0 for i in a]
                self.check(a, text, stress)
                openai.api_key = '2'
                return a
            except:
                openai.api_key = ''
                return a
        except Exception as e:
            openai.api_key = ''
            signal.alarm(0)
            #traceback.print_exc()
            return [0] * len(text)
        
    def recommend(self, insights):
        #signal.signal(signal.SIGALRM, self.signal_handler)
        #signal.alarm(30)
        input_msg = """You felt the emotion 'anger'' the most in the year: 2020.
                        You felt the emotion 'anger'' the most in the season: winter.
                        You felt the emotion 'anger'' the most in the month: January.
                        You felt the emotion 'anger'' the most in the day of week: Monday.
                        You felt the emotion 'anger'' the most in the time of day: late night/early morning (1 AM - 5 AM).
                        You felt the emotion 'anger'' the most in the channel: Direct Message with ag#8095.
                        You felt the emotion 'happiness'' the most in the year: 2023.
                        You felt the emotion 'happiness'' the most in the season: winter.
                        You felt the emotion 'happiness'' the most in the month: December.
                        You felt the emotion 'happiness'' the most in the day of week: Tuesday.
                        You felt the emotion 'happiness'' the most in the time of day: night (9 PM - 1 AM).
                        You felt the emotion 'happiness'' the most in the channel: nct.
                        You felt the emotion 'sadness'' the most in the year: 2020.
                        You felt the emotion 'sadness'' the most in the season: winter.
                        You felt the emotion 'sadness'' the most in the month: January.
                        You felt the emotion 'sadness'' the most in the day of week: Monday.
                        You felt the emotion 'sadness'' the most in the time of day: late night/early morning (1 AM - 5 AM).
                        You felt the emotion 'sadness'' the most in the channel: Direct Message with ag#8095.
                        You felt the emotion 'stress'' the most in the year: 2020.
                        You felt the emotion 'stress'' the most in the season: winter.
                        You felt the emotion 'stress'' the most in the month: January.
                        You felt the emotion 'stress'' the most in the day of week: Monday.
                        You felt the emotion 'stress'' the most in the time of day: late night/early morning (1 AM - 5 AM).
                        You felt the emotion 'stress'' the most in the channel: Direct Message with ag#8095."""
        output_msg = """Based on your messages, it appears that you experience strong emotions during the winter season, especially in the month of January. It may be helpful for you to pay attention to your emotional triggers during this time, and consider strategies to manage your emotions such as mindfulness or therapy.

It also seems that you tend to feel the most intense emotions late at night or early in the morning, particularly when messaging a specific person. It may be worth examining the nature of this relationship and whether it is contributing to your emotional distress.

On a positive note, it appears that you experience a lot of happiness in the winter season as well, particularly in the month of December and on Tuesday evenings. You may want to try to engage in activities that bring you joy during this time, such as spending time with loved ones or engaging in hobbies.

Overall, it may be helpful for you to prioritize self-care and emotional regulation strategies during the winter months, particularly in the early morning hours. Consider seeking support from a mental health professional if your emotions continue to feel overwhelming or interfere with your daily life."""
        
        prompt = '''Provide a therapist's perspective on how a person can improve their lifestyle based on insights from an app that predicts their emotions. Use specific evidence from the insights and give recommendations in the second person for strategies to improve their lifestyle, focusing on the specific emotions and time frames. Keep your responses concise and avoid generalizations.'''
        
        try:
            db.open()
            openai.api_key = db.get_openai_key()
            db.close()
            response = openai.ChatCompletion.create(
                    model=self.MODEL,
                    messages=[
                        {"role": "system", "content": "you are a robot therapist"},
                        {"role": "user", "content": "prompt"},
                        {"role": "assistant", "content": "ok"},
                        {"role": "user", "content": input_msg},
                        {"role": "assistant", "content": output_msg},
                        #{"role": "user", "content": "Return the emotion associated with the following message: asdfgfs"},
                        #{"role": "assistant", "content": "0"},
                        {"role": "user", "content": insights}
                    ],
                    temperature=0.5,
                )
            openai.api_key = ''
            #signal.alarm(0)
            return (response["choices"][0]["message"]["content"])
        except:
            traceback.print_exc()
            openai.api_key = ''
            #signal.alarm(0)
            return 'Recommendations errored. Re-run to try again.'            

    def check(self, a, b, stress = False):
        if len(a) == len(b):
            #print(len(a),len(b))
            return
        elif len(a) < len(b):
            a.append(0)
        else:
            if stress:
                a.pop()
            else:
                if (0 in a):
                    a.remove(0)
        self.check(a, b, stress)

    def check2(self, a):
        if len(str(a['Contents'].to_list())) > (4000 - 1040):
            #print("checking 2")
            a = a.iloc[:-2]
            self.check2(a)
        return

    def predict_large_recurse(self, data, count = 0, df_list = [], rpq = 20, stress = False):
        #warnings.filterwarnings("ignore")
        a = None
        rpq = 20
        '''len(data) // 20 + 1
        if (rpq > 31):
            rpq = 31'''
        #print(rpq)
        for i in range(20):
            if len(data) <= count: break
            print(f'{count}/{len(data)}', end = '\r')
            n = data.iloc[count : count + rpq]
            if len(data.iloc[count:]) < rpq: count += (len(data.iloc[count:]) - rpq)
            self.check2(n)
            df_list.append(n)
            n = n['Contents'].to_list()
            #print(len(n))
            #print(1)
            a = time.time() if i == 0 else a
            b = self.predict_large(n, stress)
            if type(b) == 'str':
                #print(f"error: {b}")
                continue
            count += rpq
            df_list[-1]['stress' if stress else 'emotion'] = b
            #print(2)
        if len(data) > count:
            if time.time() - a < 61:
                #print(f"reached: count = {count}. sleeping for {60 - (time.time() - a)}")
                time.sleep(60 - (time.time() - a))

            self.predict_large_recurse(data, count = count + 20, df_list = df_list, rpq = rpq, stress = stress)
        #warnings.filterwarnings("default")
        #print(df_list)
        print(f'{len(data)}/{len(data)}', end = '\r')
        return pd.concat(df_list)
#print(GPTModel().test())
#print(GPTModel.map)