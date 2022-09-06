from flask_app import app
from flask_app.models.user import User
from flask_app.models.ride import Ride
from flask import render_template, redirect, session, request, flash


@app.route('/rides/dashboard')
def r_dashboard():
    if 'user_id' not in session:
        flash('* Please login or create an account first.', 'registration')
        return redirect('/')

    active_data = {'id': session['user_id']}
    active_user = User.get_by_id(active_data)
    rides = Ride.get_all_rides()
    return render_template('dashboard.html', active_user=active_user, rides=rides)


@app.route('/rides/create')
def r_create():
    if 'user_id' not in session:
        flash('* Please login or create an account first.', 'registration')
        return redirect('/')

    return render_template('create_ride.html')