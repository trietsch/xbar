import requests
from arrow import Arrow
from ics import Calendar

from .config import MotdConfig
from .domain import MotdIcons


def print_current_motd(_calendar: Calendar):
    try:
        # Shift one day, as the timeline has an offset of one day
        now_plus_one_day = Arrow.now().shift(days=1)
        today = list(_calendar.timeline.on(now_plus_one_day))[0]
        motd_first_name = list(today.attendees)[0].common_name.split(' ')[0]

        print(f'MotD: {motd_first_name} | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
    except:
        print(f'MotD: ? | templateImage={MotdIcons.MOTD_LOGO.base64_image}')


def print_coming_motd(_calendar: Calendar):
    try:
        motd = list()

        for day in range(2, 4):
            event = list(_calendar.timeline.on(Arrow.now().shift(days=day)))[0]
            week_day_name = event.begin.datetime.strftime("%A")
            upcoming_motd_first_name = list(event.attendees)[0].common_name.split(' ')[0]

            motd.append(f'{week_day_name}: {upcoming_motd_first_name}')

        if len(motd) != 0:
            print("---")

            for m in motd:
                print(m)
    except:
        pass


if __name__ == '__main__':
    req = requests.get(MotdConfig.MOTD_ICAL_URL)

    calendar = Calendar(req.text)

    print_current_motd(calendar)
    print_coming_motd(calendar)
