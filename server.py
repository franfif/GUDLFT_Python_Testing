# import json
from flask import Flask, render_template, request, redirect, flash, url_for

from utilities.utils import process_purchase, MAX_BOOKING
from utilities.utils import clubs, competitions, bookings


app = Flask(__name__)
app.secret_key = 'something_special'


@app.context_processor
def get_maximum_allowed():
    def or_maximum_allowed(places):
        return min([int(places), MAX_BOOKING])
    return dict(or_maximum_allowed=or_maximum_allowed)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("This email is not registered, please try again.")
        return redirect('/')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = request.form['places']
    if places_required == '':
        places_required = 0
    places_required = int(places_required)
    # call helper function with competition and club
    # DO I NEED TO RETURN club, competition, and booking?
    purchase, messages = process_purchase(club, competition, places_required)
    for message in messages:
        flash(message)
    if purchase:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return redirect(f'/book/{competition["name"]}/{club["name"]}')

    # helper function returns club and competition as well as exception
    # purchase_places() handle exception with appropriate flash message


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
