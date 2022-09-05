from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Ride:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.destination = data.get('destination')
        self.pickup_location = data.get('pickup_location')
        self.rideshare_date = data.get('rideshare_date')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.request_id = None
        self.driver_id = None

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