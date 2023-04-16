from imports import *

class Functions:
    def to_time(self, s: str) -> dt.datetime:
        return dt.datetime(int(s[:4]),
                            int(s[5:7]),
                            int(s[8:10]),
                            int(s[11:13]),
                            int(s[14:16])
        )

    def dm(self, s: str) -> str:
        return 'Direct Message with ' + s

    def msg_path(self, s: str) -> str:
        return os.path.join("messages", f"c{s}", "messages.csv")

    def int_time(self, t: dt.datetime):
        return t.hour * 3600 + t.minute * 60 + t.second

    def similarity_score2(self, vector1, vector2):
        #dot product
        dp = lambda v1, v2: sum([v1[i] * v2[i] for i in range(len(vector1))])
        dot = dp(vector1, vector2)
        mg1 = math.sqrt(dp(vector1, vector1))
        mg2 = math.sqrt(dp(vector2, vector2))
        return math.acos(dot/(mg1*mg2))

    def similarity_score(self, point1, point2):
        return math.sqrt(sum([(point1[i] - point2[i])**2 for i in range(len(point1))]))

    def email_connection(self, selfID, otherID):
        db.open()
        u1, u2 = None
        email = 'arjunsatishnaik@gmail.com'
        try:
            u1 = db.get_info(selfID)
            u2 = db.get_info(otherID)
        except:
            pass
        db.close()
        to = [u1['email'], u2['email']]
        msg = f"Subject: Nosedive matched {u1['name']} and {u2['name']}!\n"
        msg += ("From: %s\r\nTo: %s\r\n\r\n"
               % (email, ", ".join([u1['email'], u2['email']])))
        msg+= f"""\
        Greetings!

        Based on your entries on CherryBlossom, you both were matched:
        {u1['name'], u1['email']} 
        {u2['name'], u2['email']}

        All the best!
        Arjun Naik
        Founder of CherryBlossom

        Note that this is an automated email sent via the inbox of Arjun Naik.
        """
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            db.open()
            try:
                server.login(email, db.get_app_pwd())
                server.sendmail(email, to, msg)
            except:
                pass
            db.close()
        context.close()
            
    def verify_email(self, email, code):
        u1, u2 = None
        email = 'arjunsatishnaik@gmail.com'
        to = [u1['email'], u2['email']]
        msg = f"Subject: Nosedive email verification\n"
        msg += ("From: %s\r\nTo: %s\r\n\r\n"
               % (email, ", ".join([email])))
        msg+= f"""\
        Greetings!

        Your verification code is {code}.
        
        If you were not prompted for this, you may safely ignore this email.
        
        Arjun Naik
        Founder of Nosedive

        Note that this is an automated email sent via the inbox of Arjun Naik.
        """
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            db.open()
            try:
                server.login(email, db.get_app_pwd())
                server.sendmail(email, to, msg)
            except:
                pass
            db.close()
        context.close()
        
            
#print(db.get_app_pwd())