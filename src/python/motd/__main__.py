import requests
from arrow import Arrow
from ics import Calendar, Event

from .config import MotdConfig
from .domain import MotdIcons


def print_current_motd(_timeline):
    today = _timeline[0]
    motd_first_name = get_attendee_name(today)

    print(f'MotD: {motd_first_name} | templateImage={MotdIcons.MOTD_LOGO.base64_image}')


def print_coming_motd(_timeline):
    try:
        motd = list()

        for day in range(1, 3):
            event = _timeline[day]
            week_day_name = event.begin.datetime.strftime("%A")
            day_of_month_and_month_name = f'{event.begin.datetime.strftime("%-d")} {event.begin.datetime.strftime("%b")}'
            upcoming_motd_first_name = get_attendee_name(event)

            motd.append(f'{week_day_name} ({day_of_month_and_month_name}): {upcoming_motd_first_name}')

        if len(motd) != 0:
            print("---")

            for m in motd:
                print(m)
    except:
        pass


def get_attendee_name(event: Event):
    return list(event.attendees)[0].common_name.split(' ')[0]


if __name__ == '__main__':
    try:
        req = requests.get(MotdConfig.MOTD_ICAL_URL, timeout=5)

        calendar = Calendar(req.text)
        timeline = list(calendar.timeline.start_after(Arrow.now().shift(days=-1)))

        print_current_motd(timeline)
        print_coming_motd(timeline)
    except:
        print(f'MotD: ? | templateImage={MotdIcons.MOTD_LOGO.base64_image}')
