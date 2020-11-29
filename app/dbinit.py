#!/usr/bin/env python3

import sqlite3, secrets, logging, sys


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()

logger.info("Creating and connecting to cart.db database")
conn = sqlite3.connect('cart.db')
logger.info("Connected to cart.db database")

logger.info("Creating USER table")
conn.execute('''CREATE TABLE USER (
    EMAIL TEXT PRIMARY KEY NOT NULL,
    PASSWORD TEXT NOT NULL,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    AGE INT NOT NULL,
    APARTMENT TEXT NOT NULL,
    STREET TEXT NOT NULL,
    CITY TEXT NOT NULL,
    PINCODE TEXT NOT NULL,
    COUNTRY TEXT NOT NULL,
    PHONE TEXT NOT NULL
);''')
logger.info("USER table created successfully")

logger.info("Creating CART table")
conn.execute('''CREATE TABLE CART (
    ORDERID INT PRIMARY KEY NOT NULL,
    PRODUCTID INT NOT NULL,
    QUANTITY INT NOT NULL,
    EMAIL TEXT  NOT NULL,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    APARTMENT TEXT NOT NULL,
    STREET TEXT NOT NULL,
    CITY TEXT NOT NULL,
    PINCODE TEXT NOT NULL,
    COUNTRY TEXT NOT NULL,
    PHONE TEXT NOT NULL,
    BILL REAL,
    STATUS TEXT NOT NULL
);''')
logger.info("CART table created successfully")

logger.info("Creating SELLER table")
conn.execute('''CREATE TABLE SELLER (
    EMAIL TEXT PRIMARY KEY NOT NULL,
    PASSWORD TEXT NOT NULL,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    BUSINESS TEXT NOT NULL,
    APARTMENT TEXT NOT NULL,
    STREET TEXT NOT NULL,
    CITY TEXT NOT NULL,
    PINCODE TEXT NOT NULL,
    COUNTRY TEXT NOT NULL,
    PHONE TEXT NOT NULL 
);''')
logger.info("SELLER table created successfully")

logger.info("Creating ITEM table")
conn.execute('''CREATE TABLE ITEM (
    PRODUCTID INT PRIMARY KEY NOT NULL,
    PRODUCT TEXT NOT NULL,
    EMAIL TEXT NOT NULL,
    PRICE REAL NOT NULL,
    DESCRIPTION TEXT NOT NULL,
    FOREIGN KEY (EMAIL) REFERENCES SELLER(EMAIL)
);''')
logger.info("ITEM table created successfully")

Password = str(secrets.token_hex(8))

logger.info("Creating User: John Doe")

conn.execute("INSERT INTO USER (EMAIL, PASSWORD, FNAME, LNAME, AGE, APARTMENT, STREET, CITY, PINCODE, COUNTRY, PHONE) VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('john.doe@gmail.com', Password, 'John', 'Doe', 24, 'Apartment 14', 'Lind Street', 'Paris', '213112', 'France', '+33-987-654321'))

logger.info('Password for User john.doe@gmail.com is: ' + Password)

Password = str(secrets.token_hex(8))

conn.execute("INSERT INTO USER (EMAIL, PASSWORD, FNAME, LNAME, AGE, APARTMENT, STREET, CITY, PINCODE, COUNTRY, PHONE) VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('jean.paul@gmail.com', Password, 'Jean', 'Doe', 29, 'Apartment 17', 'Times Street', 'Paris', '213112', 'France', '+33-987-654321'))

Password = str(secrets.token_hex(8))

conn.execute("INSERT INTO SELLER (EMAIL, PASSWORD, FNAME, LNAME, APARTMENT, BUSINESS, STREET, CITY, PINCODE, COUNTRY, PHONE) VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('jean.dupont@gmail.com', Password, 'Jean', 'Dupont', 'Quick Meals', 'Apartment 2', 'Stroll Street', 'Paris', '213112', 'France', '+33-987-654321'))

Password = str(secrets.token_hex(8))

conn.execute("INSERT INTO SELLER (EMAIL, PASSWORD, FNAME, LNAME, BUSINESS, APARTMENT, STREET, CITY, PINCODE, COUNTRY, PHONE) VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('paul.jacques@gmail.com', Password, 'Paul', 'Jacques', 'Los Pollos', 'Apartment 4', 'Lord Street', 'Paris', '213112', 'France', '+33-987-654321'))

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
    VALUES ('1', 'Pâtes à la carbonara', 'jean.dupont@gmail.com', 7.95, 'Home made pasta, bacon, egg, garlic and parsley, all mixed together to provide a genuine Italian taste');
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('2', 'Wrap au poulet grillé', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('3', 'Curry Thaï Végétalien à la patate douce et pois chiche croquants', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('4', 'Pasta à la tomate et champignons', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('5', 'Teriyaki salmon with rice and vegetables', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('6', 'Lasagnes bolognaises', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.execute('''INSERT INTO ITEM (PRODUCTID, PRODUCT, EMAIL, PRICE, DESCRIPTION)
     VALUES ('7', 'One Pan Quinoa facon Mexicaine', 'jean.dupont@gmail.com', 7.95, 'Grilled chicken breast with cheddar, scallions, diced tomatoes, lettuce, ranch dressing wrapped in a tortilla')
''')

conn.commit()
logger.info("Database created successfully")
conn.close()