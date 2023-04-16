from Functions import Functions
from imports import *

class Blossom:
    def __init__(self):
        self.data = None
        self.accepted = False
        if self._tos('CONSOLE USE'):
            self.accepted = True
            print('set data by using <console>.set_data(<data>)')
        else:
            print('you must agree to our terms of service for CherryBlossom use to perform this action.')
        self.ID = uuid.uuid4()
        self.f = Functions()

    def set_data(self, data):
        self.data = data

    def _tos(self, which):
        contribution_tos = ''
        connecting_tos = ''
        CherryBlossom_tos = ''
        matching_tos = ''
        emailing_tos = ''
        if which == 'CherryBlossom USE':
            print(CherryBlossom_tos)
        if which == 'CONTRIBUTION':
            print(contribution_tos)  
        if which == 'CONNECTING':
            print(connecting_tos)
        if which == 'MATCHING':
            print(matching_tos)
        if which == 'EMAILING':
            print(emailing_tos)

        print()
        if input(f'Do you accept the terms and conditions for the following action: {which}? y/n: ') == 'y':
            return True
        return False

    def check(self):
        if not self.accepted:
            print('Redirecting to CherryBlossom use TOS')
            self.__init__()
        if self.data is None:
            print('Redirecting to CherryBlossom use TOS (you have not set data)')

    def connect(self, name, email):
        self.check()
        if self._tos('CONNECTING'):
            try:
                code = random.randint(100000,999999)
                self.f.verify_email(email, code)
                checker = input("Enter the verification code we sent to your email: ")
                if checker != code:
                    print('Invalid code.')
                    return
                db.open()
                db.add_info(self.ID, self.data)
                db.add_contact(self.ID, email, name)
                db.close()
                print('Your information has been added to our database, and you will be contacted if anyone connects with you.')
                if input('Would you like to find a connection based on your information? y/n: ') == 'y':
                    if self._tos('MATCHING'):
                        db.open()
                        users = db.get_participating(self.ID)
                        if len(users) == 0:
                            print('no matches right now. you will be contacted')
                        else:
                            scores = {}
                            for user in users:
                                score = self.f.similarity_score(list(db.get_attributes(self.ID)), list(df.get_attributes(user)))
                                scores[user] = scores
                            matchingID = min(scores, key=scores.get)
                            user = db.get_info(matchingID)
                            db.close()
                            name = user['name']
                            email = user['email']
                            print(f'You have been matched with: {name}!! You will be able to contact them via email at {email}')
                            if input('Would you like us to connect you and your match via email? y/n: ') == 'y':
                                if self._tos('EMAILING'):
                                    self.f.email_connection(self.ID, matchingID)
                                    print('an email has been sent to both of you')
                                else:
                                    print('you must agree to our terms of service for emailing to perform this action.')
                    else:
                        print('you must agree to our terms of service for matching to perform this action.')
            except:
                print('failed')
                pass
            db.close()
        else:
            print('you must agree to our terms of service for connecting to perform this action.')

    def contribute(self):
        self.check()
        if self._tos('CONTRIBUTION'):
            db.open()
            try:
                db.add_info(self.ID, self.data)
            except:
                pass
            db.close()
            print(f'When prompted for contribution ID when contributing to the study, give the following ID: {self.ID}')
        else:
            print('you must agree to our terms of service for contribution to perform this action.')
    
    def remove_email(self):
        self.check()
        if self._tos('CONTRIBUTION'):
            email = input('What is your email: ')
            code = random.randint(100000,999999)
            self.f.verify_email(email, code)
            checker = input("Enter the verification code we sent to your email: ")
            if checker == code:
                db.open()
                try:
                    db.remove_contact(email)
                except:
                    pass
                db.close()
            else:
                print('Invalid code.')
        else:
            print('you must agree to our terms of service for contribution to perform this action.')
Blossom()