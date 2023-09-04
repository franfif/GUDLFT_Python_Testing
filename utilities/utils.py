import json
from datetime import datetime


# Max number of places a club is able to book for a competition
MAX_BOOKING = 12


def is_upcoming(date):
    return date > datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def load_clubs():
    with open('./clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('./competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def load_booking():
    with open('./booking.json') as b:
        list_of_bookings = json.load(b)['bookings']
        return list_of_bookings


competitions = load_competitions()
clubs = load_clubs()
bookings = load_booking()


def process_purchase(club, competition, places_required):
    processed = False
    messages = []

    if not is_upcoming(competition['date']):
        messages.append("This competition is over. Please select another competition.")
        return processed, messages
    if places_required <= 0:
        messages.append("Please enter a positive number of places to purchase for the competition.")
    # Club is not allowed to book more than 12 places in a competition
    if places_required + int(bookings[competition['name']][club['name']]) > MAX_BOOKING:
        messages.append("You are not allowed to purchase more than 12 places for a single competition.")
    # Club is not able to purchase more places than they have points
    if places_required > int(club['points']):
        messages.append(f"You are only able to purchase {club['points']} places for your club.")
    # Club is not able to purchase more places than the competition offers
    if places_required > int(competition['numberOfPlaces']):
        messages.append(f"There are only {competition['numberOfPlaces']} places left in this competition.")

    if not messages:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club['points'] = int(club['points']) - places_required
        bookings[competition['name']][club['name']] = int(bookings[competition['name']][club['name']]) + places_required
        messages.append("Great-booking complete!")
        processed = True

    return processed, messages
