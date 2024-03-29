import sys
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from src import BaseConfig
# user_loader expects user_model to have certain attributes and methods: isAuthenticated, isActive, isAnonymous, getID
from flask_login import UserMixin


# Class that represents the "user" table from the database
class User:
    def __init__(self, first_name, last_name, email, password):
        # gender is M or F, active_since is a date, address & picture are id's that reference an address & picture
        self.id = None
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.age = None
        self.gender = None
        self.phone_number = None
        self.joined_on = None
        self.picture = None
        self.address = None
        self.send_emails = 'FALSE'

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No "id" attribute - override "get_id"')

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """

        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    if sys.version_info[0] != 2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    def to_dict(self):
        return {'id': self.id, ' email': self.email, 'first_name': self.first_name, 'last_name': self.last_name,
                'age': self.age, 'gender': self.gender, 'phone_number': self.phone_number,
                'joined_on': self.joined_on, 'picture': self.picture,
                'address': self.address}

    def generate_auth_token(self, expiration=600):
        """
        generate an authentication token which is used in the API to check if a user is
        authenticated and has access to certain pages that require login.
        :param expiration: time before token expires. Default is 600s (10 minutes)
        :return: generated token
        """
        if self.id is not None:
            s = Serializer(BaseConfig.SECRET_KEY, expires_in=expiration)
            return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        check if authentication token is valid. If it is, return the user id it belongs to.
        :param token: token to check
        :return: user id linked to token if token is valid, else None
        """
        s = Serializer(BaseConfig.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return data['id']


# Class used for accessing data from the "user" table from the database
class UserAccess:
    def __init__(self, dbconnect):
        self.dbconnect = dbconnect

    def get_users(self):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, id FROM "user"')
        users = list()
        for row in cursor:
            user_obj = User(row[0], row[1], row[2], row[3])
            user_obj.id = row[4]
            users.append(user_obj)
        return users

    def get_user(self, id):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, id FROM "user" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row:
            result = User(row[0], row[1], row[2], row[3])
            result.id = row[4]
            return result
        return None

    def get_user_on_email(self, email):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, id FROM "user" WHERE email=%s', (email,))
        row = cursor.fetchone()
        if row:
            result = User(row[0], row[1], row[2], row[3])
            result.id = row[4]
            return result
        return None

    def get_user_on_id(self, theId):
        cursor = self.dbconnect.get_cursor()
        cursor.execute('SELECT first_name, last_name, email, password, age, gender, phone_number, address, picture, send_emails '
                       'FROM "user" WHERE id=%s', (theId,))
        row = cursor.fetchone()
        if row:
            user = User(row[0], row[1], row[2], row[3])
            user.age = row[4]
            user.gender = row[5]
            user.phone_number = row[6]
            user.address = row[7]
            user.picture = row[8]
            user.send_emails = row[9]
            user.id = theId
            return user
        return None

    def add_user(self, user_obj):
        cursor = self.dbconnect.get_cursor()

        cursor.execute('INSERT INTO "user" ("id","first_name","last_name","email","password","joined_on","age","gender","phone_number","send_emails") '
                       'VALUES(default, %s, %s, %s, %s, now(), %s, %s, %s, %s)',
                           (user_obj.first_name, user_obj.last_name, user_obj.email, user_obj.password, user_obj.age,
                            user_obj.gender, user_obj.phone_number, user_obj.send_emails))
        self.dbconnect.commit()


    def edit_user(self, user_id, first_name, last_name, email, gender, age, phone_number, address_id, picture_id, send_emails):
        cursor = self.dbconnect.get_cursor()
        user = self.get_user_on_id(user_id)

        try:
            cursor.execute('UPDATE "user" SET first_name=%s,last_name=%s,email=%s,gender=%s,age=%s,phone_number=%s,'
                           'address=%s,picture=%s,send_emails=%s WHERE id=%s',
            (first_name,last_name,email,gender,age,phone_number,address_id,picture_id,send_emails,user_id))
            self.dbconnect.commit()
        except:
            raise Exception('Unable to edit user')

    def delete_user(self, user_id):
        cursor = self.dbconnect.get_cursor()

        cursor.execute('DELETE FROM "user" WHERE id=%s',(user_id,))
        self.dbconnect.commit()


