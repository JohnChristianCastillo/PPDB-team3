class Ride:
    def __init__(self, id, departure_time, arrival_time, user_id, address_to, address_from, car_id):
        # address_to & address_from are id's pointing to addresses
        self.id = id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.user_id = user_id
        self.address_to = address_to
        self.address_from = address_from
        self.car_id = car_id

    def get(dbconnect, id):
        cursor = dbconnect.get_cursor()
        cursor.execute(
            "SELECT id,departure_time,arrival_time,user_id,address_to,address_from,car_id FROM ride WHERE id = %s",
            (id,))
        id, departure_time, arrival_time, user_id, address_to, address_from, car_id = cursor.fetchone()
        return Ride(id, departure_time, arrival_time, user_id, address_to, address_from, car_id)

    def get_all(dbconnect):
        cursor = dbconnect.get_cursor()
        cursor.execute("SELECT id,departure_time,arrival_time,user_id,address_to,address_from,car_id FROM ride")
        rides = list()
        for row in cursor:
            ride = Ride(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            rides.append(ride)
        return rides

    def to_dict(self):
        return {'id': self.id, 'departure_time': self.departure_time, 'arrival_time': self.arrival_time,
                'user_id': self.user_id, 'address_to': self.address_to, 'address_from': self.address_from,
                'car_id': self.car_id}
