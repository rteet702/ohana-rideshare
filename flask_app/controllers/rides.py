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

    return render_template('create_ride.html', active_user=session['user_id'])


@app.route('/rides/submit', methods=['POST'])
def f_create():
    data = {
        'user_id': request.form.get('user_id'),
        'destination': request.form.get('destination'),
        'pickup_location': request.form.get('pickup_location'),
        'rideshare_date': request.form.get('rideshare_date'),
        'details': request.form.get('details')
    }
    if not Ride.validate_form(data):
        return redirect('/rides/create')

    Ride.create_ride(data)
    return redirect('/rides/dashboard')


@app.route('/rides/<int:ride_id>/delete')
def f_delete(ride_id):
    data = {'id': ride_id}
    Ride.delete_ride(data)

    return redirect('/rides/dashboard')


@app.route('/rides/<int:ride_id>/accept')
def f_accept(ride_id):
    data = {'user_id': session['user_id'], 'ride_id': ride_id}
    Ride.accept_ride(data)

    return redirect('/rides/dashboard')


@app.route('/rides/<int:ride_id>/cancel')
def f_cancel(ride_id):
    data = {'ride_id': ride_id}
    Ride.cancel_ride(data)

    return redirect('/rides/dashboard')


@app.route('/rides/<int:ride_id>/details')
def r_details(ride_id):
    data = {'ride_id' : ride_id}
    ride = Ride.get_by_id(data)
    return render_template('details_ride.html', ride=ride)


@app.route('/rides/<int:ride_id>/edit')
def r_edit(ride_id):
    data = {'ride_id' : ride_id}
    ride = Ride.get_by_id(data)
    return render_template('edit_ride.html', ride=ride)


@app.route('/rides/edit', methods=['POST'])
def f_edit():
    ride_id = request.form.get('ride_id')
    data = {
        'ride_id': ride_id,
        'pickup_location': request.form.get('pickup_location'),
        'details': request.form.get('details')
    }
    if not Ride.validate_edit(data):
        return redirect(f'/rides/{ride_id}/edit')

    Ride.update_ride(data)
    return redirect(f'/rides/{ride_id}/details')