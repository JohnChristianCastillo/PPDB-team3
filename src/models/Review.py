class Review:
    def __init__(self, id, user_for, user_from, amount_of_stars, title, review_text):
        self.id = id
        self.user_for = user_for
        self.user_from = user_from
        self.amount_of_stars = amount_of_stars
        self.title = title
        self.review_text = review_text

    def get(cursor, id):
        cursor.execute("SELECT id,user_for,user_from,amount_of_stars,title,review_text FROM review WHERE id = %s", (id,))
        id,user_for,user_from,amount_of_stars,title,review_text = cursor.fetchone()
        return Ride(id,user_for,user_from,amount_of_stars,title,review_text)

    def to_dict(self):
        return {'id': self.id, 'user_for': self.user_for, 'user_from': self.user_from,
        'amount_of_stars': self.amount_of_stars, 'title': self.title, 'review_text': self.review_text}
