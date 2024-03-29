from postgis import *
from postgis.psycopg import register
from shapely import geometry, wkb


# due to alter table, some addresses are inserted as '?', if these addresses are used, the address is set correctly to
# avoid problems
def get_address_function(lat, lng):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="campus_carpool")
    location = geolocator.reverse(str(lat) + ', ' + str(lng), True, timeout=300)
    try:
        housenr = location.raw['address']['house_number']
    except Exception as e:
        housenr = ''
    try:
        road = location.raw['address']['road']
    except Exception as e:
        road = ''
        housenr = ''  # no road = no housenumber
    try:
        town = location.raw['address']['town']
    except Exception as e:
        try:
            town = location.raw['address']['city_district']
        except Exception as e:
            town = ''
    try:
        postcode = location.raw['address']['postcode']
    except Exception as e:
        postcode = ''
    return road, housenr, postcode, town


class Address:
    def __init__(self, id, country, city, postal_code, street, nr, coordinates, latitude=None, longitude=None):
        self.id = id
        self.dont_store_in_db = False
        if coordinates:
            self.coordinates = wkb.loads(coordinates, hex=True)
            self.latitude = self.coordinates.y
            self.longitude = self.coordinates.x
        else:
            try:  # new addresses may not have coordinates yet (None)
                self.coordinates = wkb.dumps(coordinates, hex=True)
                self.latitude = latitude
                self.longitude = longitude
            except Exception as e:
                self.coordinates = Point(longitude, latitude)
                self.latitude = latitude
                self.longitude = longitude
        if country == '?':  # FIX: due to alter table, see above
            self.street, self.nr, self.postal_code, self.city = get_address_function(self.latitude, self.longitude)
            self.country = 'Belgium'
            from src.utils import address_access
            address_access.edit_address_non_recursive(self)
        elif country is None:
            self.street, self.nr, self.postal_code, self.city = get_address_function(self.latitude, self.longitude)
            self.country = 'Belgium'
        else:
            self.country = country
            self.city = city
            self.postal_code = postal_code
            self.street = street
            self.nr = nr

    def to_dict(self):
        return {'id': self.id,
                'country': self.country,
                'city': self.city,
                'postal_code': self.postal_code,
                'street': self.street,
                'nr': self.nr,
                'lat': self.latitude,
                'lng': self.longitude}

    def addr_to_string(self):
        return self.street + ' ' + self.nr + ', ' + self.postal_code + ' ' + self.city

    def lat_lng(self):
        return [self.latitude, self.longitude]

    def fetch_id(self):
        if self.id is not None:
            return self.id
        else:
            from src.utils import address_access
            self.id = address_access.get_id(self.country, self.city, self.postal_code, self.street, self.nr)
            return self.id


class Addresses:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect
        # self.register = register(dbconnect)

    def get_latest_id(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            "SELECT id,country,city,postal_code,street,nr, coordinates FROM address order by id desc limit 1")
        address = cursor.fetchone()
        return address[0]

    def get_on(self, on, val):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr,coordinates FROM address WHERE %s=%s",
                       (on, val))
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            addresses.append(address)
        return addresses

    def get_on_id(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT id,country,city,postal_code,street,nr,coordinates FROM address WHERE id=%s',
                       (id,))
        address = cursor.fetchone()
        if address is None:
            return None
        address_obj = Address(address[0], address[1], address[2], address[3], address[4], address[5], address[6])
        return address_obj

    def get_on_lat_lng(self, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            'SELECT id,country,city,postal_code,street,nr,coordinates FROM address '
            'WHERE coordinates=ST_MakePoint(%s,%s)',
            (longitude, latitude,))
        address = cursor.fetchone()
        if address is None:
            return None
        address_obj = Address(address[0], address[1], address[2], address[3], address[4], address[5], address[6],
                              address[7])
        return address_obj

    def get_id(self, country, city, postal_code, street, nr):
        cursor = self.dbconnect.get_cursor()
        cursor.execute(
            'SELECT id FROM address WHERE street=%s AND nr=%s AND city=%s AND postal_code=%s AND country=%s',
            (street, nr, city, postal_code, country))
        row = cursor.fetchone()
        return row[0]

    def get_all(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT id,country,city,postal_code,street,nr,coordinates FROM address")
        addresses = list()
        for row in cursor:
            address = Address(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            addresses.append(address)
        return addresses

    def add_address(self, address: Address):
        if address.dont_store_in_db:
            return
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('INSERT INTO "address" VALUES(default, %s, %s, %s, %s, %s, %s)',
                           (address.country, address.city, address.postal_code, address.street, address.nr,
                            address.coordinates))
            self.dbconnect.commit()
        except Exception as e:
            raise Exception('Unable to add address')

    def edit_address(self, address_id, street, nr, city, postal_code, country, latitude, longitude):
        cursor = self.dbconnect.get_cursor()
        address = self.get_on_id(address_id)
        address.street = street
        address.nr = nr
        address.city = city
        address.postal_code = postal_code
        address.country = country
        address.latitude = latitude
        address.longitude = longitude
        address.coordinates = wkb.dumps(geometry.Point(longitude, latitude), hex=True)
        try:
            cursor.execute(
                'UPDATE "address" SET street = %s, nr = %s, city = %s, postal_code = %s, country = %s, '
                'coordinates = ST_MakePoint(%s, %s) WHERE id=%s',
                (street, nr, city, postal_code, country, longitude, latitude, address_id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to edit address')

    def edit_address_non_recursive(self, address: Address):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute(
                'UPDATE "address" SET street = %s, nr = %s, city = %s, postal_code = %s, country = %s, '
                'coordinates = ST_MakePoint(%s, %s) WHERE id=%s',
                (address.street, address.nr, address.city, address.postal_code, address.country, address.latitude,
                 address.longitude, address.id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to edit address')

    def delete_address(self, address_id):
        cursor = self.dbconnect.get_cursor()
        try:
            cursor.execute('DELETE FROM "address" WHERE id=%s', (address_id,))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to delete address')

    def get_distance(self, latitude, longitude, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute("SELECT ST_Distance(address.coordinates, ST_MakePoint(%s, %s)) FROM address WHERE id=%s"
                       , (longitude, latitude, id))
        dist = cursor.fetchone()[0]
        return dist
