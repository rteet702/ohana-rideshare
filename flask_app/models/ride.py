from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash
from datetime import datetime


class Ride:
    def __init__(self, data:dict) -> None:

        """
        This class represents a 'ride' within the rideshare program.. All methods inside this class will pertain to the Ride, as well as any related data.
        """

        self.id = data.get('id')
        self.destination = data.get('destination')
        self.pickup_location = data.get('pickup_location')
        self.rideshare_date = data.get('rideshare_date').strftime('%b %d, %Y')
        self.details = data.get('details')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.request_id = None
        self.driver_id = None

    @staticmethod
    def validate_form(form:dict) -> bool:
        '''Quick and dirty validation. Returns True if the form is valid, False otherwise.'''

        is_valid = True

        if not form.get('destination') or len(form.get('destination')) < 3:
            flash('* Please enter a valid destination.')
            is_valid = False
        if not form.get('pickup_location') or len(form.get('pickup_location')) < 3:
            flash('* Please enter a valid pickup location.')
            is_valid = False
        if not form.get('rideshare_date'):
            flash('* Please enter a valid date.')
            is_valid = False
        if not form.get('details') or len(form.get('details')) < 10:
            flash('* Please enter details. Must be at least 10 characters.')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_edit(form:dict) -> bool:
        '''Quick and dirty validation. Returns True if the form is valid, False otherwise.'''

        is_valid = True

        if not form.get('pickup_location') or len(form.get('pickup_location')) < 3:
            flash('* Please enter a valid pickup location.')
            is_valid = False
        if not form.get('details') or len(form.get('details')) < 10:
            flash('* Please enter details. Must be at least 10 characters.')
            is_valid = False

        return is_valid

    @staticmethod
    def delete_ride(data:dict) -> None:
        '''Delete a ride from the database.'''

        query = "DELETE FROM rides WHERE id=%(id)s;"
        connectToMySQL('rideshare').query_db(query, data)

    @classmethod
    def get_all_rides(cls) -> list:
        '''Get a list of all rides currently created, as well as associating the driver / rider with the ride.'''

        query = """SELECT
                        rides.id,
                        destination,
                        pickup_location,
                        rideshare_date,
                        rides.created_at,
                        rides.updated_at,
                        users.email AS rider,
                        users_2.email AS driver
                    FROM
                        rides
                    JOIN
                        users
                    ON
                        request_id = users.id
                    LEFT JOIN
                        users AS users_2
                    ON
                        driver_id = users_2.id;"""

        results = connectToMySQL('rideshare').query_db(query)
        return_list = []

        for row in results:
            ride_data = {
                'id': row.get('id'),
                'destination' : row.get('destination'),
                'pickup_location' : row.get('pickup_location'),
                'rideshare_date' : row.get('rideshare_date'),
                'created_at' : row.get('rides.created_at'),
                'updated_at' : row.get('rides.updated_at')
            }

            request_data = {'email': row.get('rider')}
            driver_data = {'email': row.get('driver', None)}

            request = User.get_by_email(request_data)
            driver = User.get_by_email(driver_data)

            ride = cls(ride_data)

            ride.request_id = request
            ride.driver_id = driver

            return_list.append(ride)
        return return_list

    @classmethod
    def create_ride(cls, data:dict) -> int:
        '''Quick method to take the data from a form and create a new ride. Returns the id of the new row.'''

        query = "INSERT INTO rides (destination, pickup_location, rideshare_date, request_id, details) VALUES (%(destination)s, %(pickup_location)s, %(rideshare_date)s, %(user_id)s, %(details)s);"

        return connectToMySQL('rideshare').query_db(query, data)

    @classmethod
    def accept_ride(cls, data:dict) -> None:
        '''Update the given ride's driver_id to match the accepting user.'''

        query = "UPDATE rides SET driver_id=%(user_id)s WHERE id=%(ride_id)s;"

        connectToMySQL('rideshare').query_db(query, data)

    @classmethod
    def cancel_ride(cls, data:dict) -> None:
        '''Update the given ride's driver_id to None'''

        query = "UPDATE rides SET driver_id=default WHERE id=%(ride_id)s;"

        connectToMySQL('rideshare').query_db(query, data)

    @classmethod
    def update_ride(cls, data:dict) -> None:
        '''Update the given ride's pickup location and details.'''

        query = "UPDATE rides SET pickup_location=%(pickup_location)s, details=%(details)s WHERE id=%(ride_id)s;"

        connectToMySQL('rideshare').query_db(query, data)

    @classmethod
    def get_by_id(cls, data:dict) -> list:
        '''Get a list of all rides currently created, as well as associating the driver / rider with the ride.'''

        query = """SELECT
                        rides.id,
                        destination,
                        pickup_location,
                        rideshare_date,
                        rides.created_at,
                        rides.updated_at,
                        rides.details,
                        users.email AS rider,
                        users_2.email AS driver
                    FROM
                        rides
                    JOIN
                        users
                    ON
                        request_id = users.id
                    LEFT JOIN
                        users AS users_2
                    ON
                        driver_id = users_2.id
                    WHERE
                        rides.id=%(ride_id)s;"""

        result = connectToMySQL('rideshare').query_db(query, data)

        print(result)
        request_data = {'email': result[0].get('rider')}
        driver_data = {'email': result[0].get('driver')}

        ride = cls(result[0])
        ride.driver_id = User.get_by_email(driver_data)
        ride.request_id = User.get_by_email(request_data)

        return ride