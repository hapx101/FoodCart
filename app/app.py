#!/usr/bin/env python3

from flask import Flask, render_template, redirect, session, url_for, g, request
import sqlite3, hashlib, os, logging, sys, datetime
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()


logger.info("Initializing Flask")
app = Flask(__name__)
logger.info("Setting Secret")
try:
    app.secret_key = os.environ['SECRET']
except:
    app.secret_key = 'RandomKey123'
DATABASE = 'cart.db'


def pass_validation(email, password):
    logger.debug("Email:" + str(email))
    logger.debug("Password:" + str(password))
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT password FROM USER WHERE email='" + str(email) + "'")
    actual_passwd = cur.fetchone()[0]
    logger.debug("Actual Password:" + str(actual_passwd))
    con.close()
    if password == actual_passwd:
        return True
    return False

def getUser(email):
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT fname FROM USER WHERE email='" + str(email) + "'")
    fname = cur.fetchone()[0]
    logger.debug("First Name:" + str(fname))
    con.close()
    return fname

def getOrder(email, status='open'):
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT orderid, productid, quantity FROM CART WHERE email='" + str(email) + "' AND status='" + str(status) +"'")
    orders = cur.fetchall()
    out = []
    for order in orders:
        order_id = order[0]
        product_id = order[1]
        quantity = order[2]
        cur.execute("SELECT product, description, price FROM ITEM WHERE productid='" + str(product_id) + "'")
        item = cur.fetchone()
        product = item[0]
        description = item[1]
        price = item[2]
        out.append((product_id, product, description, price, quantity, order_id))
    logger.debug("Orders:" + str(orders))
    con.close()
    return out

def getUserAddress(email):
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT fname, lname, apartment, street, city, pincode, country, phone FROM USER WHERE email='" + str(email) + "'")
    user = cur.fetchone()
    logger.debug('Database Output for email:' + email + '-' + str(user))
    con.close()
    return user

def getOrderId():
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT orderid FROM CART")
    order = cur.fetchall()
    logger.debug("Orders:" + str(order))
    con.close()
    return order

def getItems():
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEM")
    items = cur.fetchall()
    logger.debug("Items:" + str(items))
    con.close()
    return items

def addToCart(orderid, productid, quantity, email, bill=False):
    user = getUserAddress(email)
    fname = str(user[0])
    lname = str(user[1])
    apartment = str(user[2])
    street = str(user[3])
    city = str(user[4])
    pincode = str(user[5])
    country = str(user[6])
    phone = str(user[7])
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    con.execute("INSERT INTO CART (ORDERID, PRODUCTID, QUANTITY, EMAIL, FNAME, LNAME, APARTMENT, STREET, CITY, PINCODE, COUNTRY, PHONE, BILL, STATUS) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (orderid, productid,quantity, email, fname, lname, apartment, street, city, pincode, country, phone, bill, 'open'))
    logger.debug("Cart:" + str(getOrder(email, 'open')))
    con.commit()
    con.close()
    return 201

def checkoutCommit(orderid):
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("UPDATE CART SET STATUS='ordered' WHERE orderid=" + str(orderid) + "")
    con.commit()
    con.close()
    return 201

def removeFromCartCommit(orderid):
    con = sqlite3.connect(DATABASE)
    con.set_trace_callback(logger.debug)
    cur = con.cursor()
    cur.execute("UPDATE CART SET STATUS='removed' WHERE orderid=" + str(orderid) + "")
    con.commit()
    con.close()
    return 201

@app.route("/")
def root():
    items = getItems()
    if 'email' in session:
        loggedIn = True
        fname = getUser(session['email'])
        cart = len(getOrder(session['email'], status='open'))
    else:
        loggedIn = False
        fname = ''
        cart = 0
    return render_template('home.html', loggedIn=loggedIn, fname=fname, cart=cart, items=items)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

@app.route("/login")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/loginFormSubmit", methods = ['POST'])
def loginSubmit():
    email = request.form['email']
    password = request.form['password']
    if pass_validation(email, password):
            session['email'] = email
            return redirect(url_for('root'))
    else:
        error = 'Invalid UserId / Password'
        return render_template('login.html', error=error)

@app.route("/orders")
def orders():
    if 'email' in session:
        fname = getUser(session['email'])
        items= getOrder(session['email'], status='open')
        cart_len = len(items)
        orders= getOrder(session['email'], status='ordered')
        orders.reverse()
        return render_template('order.html', fname=fname, cart=cart_len, items=orders)
    else:
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
    if 'email' in session:
        fname = getUser(session['email'])
        items= getOrder(session['email'], status='open')
        cart_len = len(items)
        bill = 0
        for item in items:
            bill = bill + (item[3] * item[4])
        user = getUserAddress(session['email'])
        return render_template('cart.html', fname=fname, items=items, cart=cart_len, user=user, bill=round((bill), 2))
    else:
        return redirect(url_for('root'))

@app.route("/addToCart", methods = ['POST'])
def addToCartSubmit():
    logger.debug('Request submitted: ' + str(request.form))
    productid = int(request.form['productId'])
    price = request.form['price']
    quantity = int(request.form['Quantity'])
    bill = price * quantity
    orderid = int(len(getOrderId()) + 1)
    if 'email' in session:
        addToCart(orderid, productid, quantity, session['email'], bill)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('loginForm'))

@app.route("/removeToCart", methods = ['GET'])
def removeFromCartSubmit():
    logger.debug('Request submitted: ' + str(request.args.get))
    orderid = request.args.get('orderId')
    logger.debug('OrderId: ' + str(orderid))
    if 'email' in session:
        removeFromCartCommit(orderid)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('loginForm'))

@app.route("/checkout", methods = ['POST'])
def checkout():
    logger.debug('Request submitted: ' + str(request.form))
    if 'email' in session:
        for iter in range(0, len(request.form)):
            orderid = request.form['orderId' + str(iter)]
            logger.debug('Order ID: ' + str(orderid))
            checkoutCommit(orderid)
        return redirect(url_for('orders'))
    else:
        return redirect(url_for('loginForm'))

if __name__ == '__main__':
    app.run(debug=True)