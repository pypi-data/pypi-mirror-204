import requests

from time import sleep
import re
import json
from .abc import Intranet
from .checkers import check_autologin
from .constants import PROMOTIONS, courses

class AutologinIntranet(Intranet):
    def __init__(self, token=""):
        self.token = check_autologin(token)

    def set_token(self, token):
        self.token = check_autologin(token)

    def get_current_scholar_year(self):
        content = requests.get(
            f'https://intra.epitech.eu/').content.decode('utf-8')
        matches = re.finditer(r'\"scolaryear\":([0-9]{4})', content)
        result = filter(id, matches)
        return next(result)[1]
 
    def get_students(self, promotion, year):
        results, nb_items, total = [], 0, 1
        promo = f'{PROMOTIONS[promotion]}'
        while nb_items < total:
            try:
                req = requests.get(
                    f'{self.token}/user/filter/user?format=json&location=FR/LYN&year={year}&active=true&promo={promo}&offset={nb_items}'
                )
            except Exception as e:
                print(f'[getStudents] An error occured while asking intra : {e}')
                return None
            results += [elem['login'] for elem in req.json()['items']]
            total = req.json()['total']
            nb_items += len(req.json()['items'])
        return results
    
    def register_students(self, event, students):
        if not students:
            return None
        data = {
            f'items[{index}][login]' : row
            for index, row in enumerate(students)
        }
        try:
            req = requests.post(
                f'{self.token}{event}/updateregistered?format=json', data)
        except Exception as e:
            print(f'[registerStudents] An error occured while asking intra : {e}')
            return None
        sleep(0.2) # HACK: avoid intra rate limit
        return students

    def create_event(self, activity, date, hour):
        acti_data = {'start': date + ' ' + hour}
        try:
            req = requests.post(
                f'{self.token}{activity}planify?format=json', acti_data)
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return None
        sleep(0.2) # HACK: avoid intra rate limit
        return req.json()

    def get_events(self, activity, date=None):
        try:
            print(self.token)
            activities = requests.get(f'{self.token}{activity}?format=json')
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return None
        activities_json = activities.json()
        events = activities_json.get('events', None)
        if events == None:
            error_message = activities_json.get('message', None)
            print(error_message)
            print('An error occured with the request : unable to get correct content')
            return None
        if date:
            today_event = [
                a['code'] 
                for a in events
                if a['begin'][:10] == date
            ]
            return today_event
        return events

    def get_registered_students(self, event):
        students = requests.get(
            f'{self.token}{event}/registered?format=json')
        presence = {
            a['login'] : a['present']
            for a in students.json()
        }
        return presence
    
    def get_activities(self, year, codeModule, codeInstance):
        try:
            data = requests.get(
                f'{self.token}/module/{year}'
                f'/{codeModule}/{codeInstance}/?format=json')
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return
        activities = data.json()
        return activities
    
    def get_modules(self, year):
        try:
            data = requests.get(
                f'{self.token}/course/filter'
                f'?format=json&preload=1&scolaryear[]={year}&{courses}')
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return

        result = data.json()
        return result['items']
    
    def get_module(self, year, code, instance):
        try:
            data = requests.get(
                f'{self.token}/module/{year}/{code}/{instance}/?format=json')
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return
        result = data.json()
        return result