import requests
from decision_engine import settings
from dateutil.parser import parse
from datetime import date


def get_user_data(user_id):
    response = requests.get(
            'https://%s/dev/api/cdv/getusermetadata/%s' %
            (settings.WELIVE_HOST, user_id),
            auth=(settings.BASIC_USER, settings.BASIC_PASSWORD))

    if response.status_code == 200:
        user_age, user_location, user_apps, user_tags = 99, None, None, None
        json_response = response.json()
        user_apps = []
        if 'usedApps' in json_response:
            for app in json_response['usedApps']:
                user_apps.append(app['appID'])
        today = date.today()
        if 'birthdate' in json_response:
            if json_response['birthdate'] != None:
                born = parse(json_response['birthdate'])
                user_age = today.year - born.year - \
                    ((today.month, today.day) < (born.month, born.day))
                user_location = json_response.get('city', None)
                user_tags = json_response.get('userTags', [])
        return user_age, user_location, user_apps, user_tags
    else:
        raise Exception(response.content)
