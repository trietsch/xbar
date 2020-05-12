import requests
from ics import Calendar
from arrow import Arrow

from .config import MotdConfig
from .domain import MotdIcons

if __name__ == '__main__':
    try:
        req = requests.get(MotdConfig.MOTD_ICAL_URL)

        cal = Calendar(req.text)

        # Shift one day, as the timeline has an offset of one day
        now_plus_one_day = Arrow.now().shift(days=1)
        today = list(cal.timeline.on(now_plus_one_day))[0]
        motd_first_name = list(today.attendees)[0].common_name.split(' ')[0]

        print(f'MotD: {motd_first_name} | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
    except:
        print(f'MotD: ? | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
