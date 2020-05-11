import requests
from ics import Calendar

from .config import MotdConfig
from .domain import MotdIcons

if __name__ == '__main__':
    try:
        req = requests.get(MotdConfig.MOTD_ICAL_URL)

        cal = Calendar(req.text)

        today = list(cal.timeline)[0]
        motd_first_name = list(today.attendees)[0].common_name.split(' ')[0]

        print(f'MotD: {motd_first_name} | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
    except:
        print(f'MotD: ? | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
