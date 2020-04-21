DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    country VARCHAR(256) NOT NULL,
    city VARCHAR(256) NOT NULL,
    postal_code VARCHAR(256) NOT NULL,
    street VARCHAR(256) NOT NULL,
    nr VARCHAR(256) NOT NULL,
    latitude float8 NOT NULL,
    longitude float8 NOT NULL
);

/*
type for gender, 2 options
*/
DROP TYPE IF EXISTS gender_type CASCADE;
CREATE TYPE gender_type AS ENUM (
    'M',
    'F'
);

/*
picture table for profile picture ("user") and picture of car
(not required for either -> doesn't go in "user"/car tables)
filename is path to file
*/
DROP TABLE IF EXISTS picture CASCADE;
CREATE TABLE picture (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(256) NOT NULL
);

/*
"user" table, last name & age are required
gender either M or F from gender_type
*/
DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(256),
    last_name VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password varchar not null,
    joined_on timestamp not null,
    age INTEGER,
    gender gender_type,
    phone_number VARCHAR(20),
    picture int REFERENCES picture(id),
    address int REFERENCES address(id)
);

/*
type for fuel, 5 options (for now?)
*/
DROP TYPE IF EXISTS fuel_type CASCADE;
CREATE TYPE fuel_type AS ENUM (
    'benzine', /* = gasoline = petrol */
    'diesel',
    'electricity',
    'CNG', /* = compressed natural gas */
    'LPG', /* = liquefied petroleum gas */
    'ethanol',
    'bio-diesel'
);

/*
car table, color/brand/model is optional
optional picture
fuel from 5 fuel options (fuel_type)
*/
DROP TABLE IF EXISTS car CASCADE;
CREATE TABLE car (
    id SERIAL PRIMARY KEY,
    number_plate VARCHAR(10) NOT NULL,
    color VARCHAR(30),
    brand VARCHAR(30) NOT NULL,
    model VARCHAR(256) NOT NULL,
    nr_seats INTEGER NOT NULL,
    construction_year INTEGER,
    fuel_consumption VARCHAR(30),
    fuel fuel_type,
    user_id int REFERENCES "user"(id) NOT NULL,
    picture int REFERENCES picture(id)
);

/*
ride table, belongs to a "user"
has a departure time (date + time) that's required
arrival time is not required
*/
DROP TABLE IF EXISTS ride CASCADE;
CREATE TABLE ride (
    id SERIAL PRIMARY KEY,
    departure_time timestamp NOT NULL,
    arrival_time timestamp NOT NULL,
    user_id int REFERENCES "user"(id) NOT NULL,
    address_1 int REFERENCES address(id) NOT NULL,
    campus int REFERENCES campus(id) NOT NULL,
    to_campus bool default true,
    car_id int REFERENCES car(id),
    passengers int NOT NULL,
    pickup_point_1 int REFERENCES pickup_point(id),
    pickup_point_2 int REFERENCES pickup_point(id),
    pickup_point_3 int REFERENCES pickup_point(id)
);

/*
ride passenger table keeps track of all passengers that belong to a ride.
 */
DROP TABLE IF EXISTS passenger_ride CASCADE;
CREATE TABLE passenger_ride (
    user_id int REFERENCES "user"(id) NOT NULL,
    ride_id int REFERENCES ride(id) NOT NULL
);

/*
pickup point table keeps track of all the pickup points used in a ride.
*/
DROP TABLE IF EXISTS pickup_point CASCADE;
CREATE TABLE pickup_point (
    id SERIAL PRIMARY KEY,
    latitude float8 NOT NULL,
    longitude float8 NOT NULL,
    estimated_time timestamp NOT NULL
);

/*
review table for a review, is connected to 2 people: the writer and the reviewed person
also holds an amount of stars, the title of the review and the text
title and text can be empty, it's possible to only leave the star review
*/

DROP TABLE IF EXISTS review CASCADE;
CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    user_for int REFERENCES "user"(id) NOT NULL,
    user_from int REFERENCES "user"(id) NOT NULL,
    amount_of_stars INTEGER NOT NULL,
    title VARCHAR(256),
    review_text VARCHAR(1000),
    creation date default now()
);


/* start punt: Thomas More - Lesplaats Duffel (SNOR), coordinaten: 51.0953, 4.49607 */
insert into address  -- one address = id 1
values (default, 'Belgium', 'Antwerp', '2600', 'KwebbelStraat', '69', 51.0953, 4.49607);

insert into "user"  -- one user = id 1
values (default , 'Kabouter', 'Lui', 'admin@blog.com', 'password', '1999-04-04 01:12:11', 20, 'M', NULL, NULL, 1);

insert into car  -- one car = id 1
values (default , '9999', 'Red', 'Toyota', 'asdf', 4, 1996, '4', 'ethanol', 1, NULL);

/* pickup 1 */
insert into pickup_point
values (default, 51.100562, 4.473305, '2020-04-14 14:03');

/* pickup 2 */
insert into pickup_point
values (default, 51.106853, 4.438677, '2020-04-14 14:05');

/* pickup 3 */
insert into pickup_point
values (default, 51.112011, 4.424566, '2020-04-14 14:08');

/* route 1:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Middelheim (301)
 */
insert into ride
values (default , '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 301, true, 1, 3, 1, 2, 3);

/* route 2:
        start punt: address 1
        eindpunt: UAntwerpen - Campus Groenenborger (300)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 300, true, 1, 3, 1, 2, 3);

/* route 3:
        start punt: address 1
        eindpunt: Hoger Instituut voor Godsdienstwetenschappen (148)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 148, true, 1, 3, 1, 2, 3);

/* route 4:
        start punt: address 1
        eindpunt: KdG Hogeschool - Campus Hoboken (248)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 248, true, 1, 3, 1, 2, 3);

/* route 5:
        start punt: address 1
        eindpunt: APB - Campus Vesta (14)
 */
insert into ride
values (default, '2020-04-14 13:00', '2020-04-14 14:00', 1, 1, 14, true, 1, 3, 1, 2, 3);

/*
USAGE:
    - open kaart en zoek naar Duffel, waar startpunt Thomas More - Lesplaats Duffel (SNOR)
    - kies 1 van bovenstaande 5 campussen, of kies een punt op de kaart.
    - zet de tijd op 14 april 2020 13u00 (depart at) of 14u00 (arrive by)
    - verwachte resultaten:
        + UAntwerpen - Campus Middelheim (301) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + UAntwerpen - Campus Groenenborger (300) als eindpunt geeft 3 resultaten terug, campussen 301, 300 en 148
        + Hoger Instituut voor Godsdienstwetenschappen (148) als eindpunt geeft 3 resultaten terug, campussen 301, 300, 148 en 248
        + KdG Hogeschool - Campus Hoboken (248) als eindpunt geeft 2 resultaten terug, campussen 148 en 248
        + APB - Campus Vesta (14) ligt heel ver van de andere campussen verwijdert, dus 1 resultaat: campus zelf (14)
 */