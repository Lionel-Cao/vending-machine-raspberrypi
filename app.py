import RPi.GPIO as GPIO
import time
import pyrebase
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

config = {
      "apiKey": "AIzaSyCz-FHXfyY1nr5tkQfiw8G6rqJYipF24JA",
      "authDomain": "vending-machine-6f41b.firebaseapp.com",
      "databaseURL": "https://vending-machine-6f41b-default-rtdb.firebaseio.com",
      "projectId": "vending-machine-6f41b",
      "storageBucket": "vending-machine-6f41b.appspot.com",
      "messagingSenderId": "866803929412",
      "appId": "1:866803929412:web:630ba649987ebc142d4711",
      "measurementId": "G-9T3KV64TYF"
     }
firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
database = firebase.database()

app = Flask(__name__)

enA = 18
in1 = 23
in2 = 24
in3 = 16
in4 = 20
enB = 12
enC = 13
in5 = 19
in6 = 26
cb1 = 22
cb2 = 27
cb3 = 5
temp1=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.setup(in5,GPIO.OUT)
GPIO.setup(in6,GPIO.OUT)
GPIO.setup(enC,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(in5,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
GPIO.setup(cb1, GPIO.IN)
GPIO.setup(cb2, GPIO.IN)
GPIO.setup(cb3, GPIO.IN)
p=GPIO.PWM(enA,10000)
p.start(50)
q=GPIO.PWM(enB,10000)
q.start(50)
k=GPIO.PWM(enC,10000)
k.start(50)

id_1 = {
           'name' : 'Coca',
           'price' : 5000,
           'quantity' : 0,
           'stock' : 0,
           'total' : 0
        }#end id_1
id_2 = {
           'name' : 'Pepsi',
           'price' : 4000,
           'quantity' : 0,
           'stock' : 0,
           'total' : 0
        }#end id_2
id_3 = {
           'name' : 'Mitom',
           'price' : 3000,
           'quantity' : 0,
           'stock' : 0,
           'total' : 0
        }#end id_3
slot_1 = None
slot_2 = None
slot_3 = None
DS1 = 0
DS2 = 0
DS3 = 0
id1Input = 0
id2Input = 0
id3Input = 0
productPlus = 0
subTotal = 0
def prepareBegin():
    temp = 0
    while GPIO.input(cb1) != 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp += 1
        time.sleep(1)
        if temp > 5:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            break
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
    time.sleep(2)
    temp = 0
    while GPIO.input(cb2) != 0:
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
        temp += 1
        time.sleep(1)
        if temp > 5:
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            break
        else:
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
    time.sleep(2)
    temp = 0
    while GPIO.input(cb3) != 0:
        GPIO.output(in5,GPIO.LOW)
        GPIO.output(in6,GPIO.HIGH)
        temp += 1
        time.sleep(1)
        if temp > 5:
            GPIO.output(in5,GPIO.LOW)
            GPIO.output(in6,GPIO.LOW)
            break
        else:
            GPIO.output(in5,GPIO.LOW)
            GPIO.output(in6,GPIO.LOW)
@app.route('/pickup/<status>/<productPlus>')
def pick(productPlus, status):
    global slot_1
    global slot_2
    global slot_3
    global id_1
    global id_2
    global id_3
    if productPlus == 'item1' and status == 'plus':
        cart(1)
        id_1['total'] = id_1['price']*id_1['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html', id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
    elif productPlus == 'item1' and status == 'minus':
        minusCart(1)
        id_1['total'] = id_1['price']*id_1['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html',id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
    if productPlus == 'item2' and status == 'plus':
        cart(2)
        id_2['total'] = id_2['price']*id_2['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html',id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
    elif productPlus == 'item2' and status == 'minus':
        minusCart(2)
        id_2['total'] = id_2['price']*id_2['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html',id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
    if productPlus == 'item3' and status == 'plus':
        cart(3)
        id_3['total'] = id_3['price']*id_3['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html',id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
    elif productPlus == 'item3' and status == 'minus':
        minusCart(3)
        id_3['total'] = id_3['price']*id_3['quantity']
        subTotal = id_1['total'] + id_2['total'] + id_3['total']
        return render_template('index.html',id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3, subTotal=subTotal)
def cart(id_input):
        global slot_1
        global slot_2
        global slot_3
        global id_1
        global id_2
        global id_3
#         id_pick = dict()
        if id_input == 1 and id_1['quantity'] < id_1['stock']:
            id_1['quantity'] = id_1['quantity'] + 1
            if slot_1 == None or slot_1['name'] == id_1['name']:
                slot_1 = id_1
            elif slot_2 == None or slot_2['name'] == id_1['name']:
                slot_2 = id_1
            elif slot_3 == None or slot_3['name'] == id_1['name']:
                slot_3 = id_1
        elif id_input == 2 and id_2['quantity'] < id_2['stock']:
            id_2['quantity'] = id_2['quantity'] + 1
            if slot_1 == None or slot_1['name'] == id_2['name']:
                slot_1 = id_2
            elif slot_2 == None or slot_2['name'] == id_2['name']:
                slot_2 = id_2
            elif slot_3 == None or slot_3['name'] == id_2['name']:
                slot_3 = id_2
        elif id_input == 3 and id_3['quantity'] < id_3['stock']:
            id_3['quantity'] = id_3['quantity'] + 1
            if slot_1 == None or slot_1['name'] == id_3['name']:
                slot_1 = id_3
            elif slot_2 == None or slot_2['name'] == id_3['name']:
                slot_2 = id_3
            elif slot_3 == None or slot_3['name'] == id_3['name']:
                slot_3 = id_3
        print('slot 3',slot_3)
#         if slot_1 == None:
#             slot_1 = id_pick
#         else:
#             if slot_1['name'] == id_pick['name'] and id_pick['quantity'] < id_pick ['stock']:
#                 slot_1 = id_pick
#             elif slot_2 == None and id_pick['quantity'] < id_pick ['stock']:
#                 slot_2 = id_pick
#             elif slot_2['name'] == id_pick['name'] and id_pick['quantity'] < id_pick ['stock']:
#                 slot_2 = id_pick
#             elif slot_3 == None and id_pick['quantity'] < id_pick ['stock']:
#                 slot_3 = id_pick
#             elif slot_3['name'] == id_pick['name'] and id_pick['quantity'] < id_pick ['stock']:
#                 slot_3 = id_pick
        return slot_1, slot_2, slot_3
def minusCart(id_input):
        global slot_1
        global slot_2
        global slot_3
        global id_1
        global id_2
        global id_3
        id_pick = dict()
        if id_input == 1 and id_1['quantity'] > 0:
            id_1['quantity'] = id_1['quantity']-1
            if slot_1['name'] == id_1['name'] and id_1['quantity'] > 0:
                slot_1['quantity'] = id_1['quantity']
            elif slot_1['name'] == id_1['name'] and id_1['quantity'] == 0:
                slot_1 = None
            elif slot_2['name'] == id_1['name'] and id_1['quantity'] > 0:
                slot_2['quantity'] = id_1['quantity']
            elif slot_2['name'] == id_1['name'] and id_1['quantity'] == 0:
                slot_2 = None
            elif slot_3['name'] == id_1['name'] and id_1['quantity'] > 0:
                slot_3['quantity'] = id_1['quantity']
            elif slot_3['name'] == id_1['name'] and id_1['quantity'] == 0:
                slot_3 = None
        elif id_input == 2 and id_2['quantity'] > 0:
            id_2['quantity'] = id_2['quantity']-1
            if slot_1['name'] == id_2['name'] and id_2['quantity'] > 0:
                slot_1['quantity'] = id_2['quantity']
            elif slot_1['name'] == id_2['name'] and id_2['quantity'] == 0:
                slot_1 = None
            elif slot_2['name'] == id_2['name'] and id_2['quantity'] > 0:
                slot_2['quantity'] = id_2['quantity']
            elif slot_2['name'] == id_2['name'] and id_2['quantity'] == 0:
                slot_2 = None
            elif slot_3['name'] == id_2['name'] and id_2['quantity'] > 0:
                slot_3['quantity'] = id_2['quantity']
            elif slot_3['name'] == id_2['name'] and id_2['quantity'] == 0:
                slot_3 = None
        elif id_input == 3 and id_3['quantity'] > 0:
            id_3['quantity'] = id_3['quantity']-1
            if slot_1['name'] == id_3['name'] and id_3['quantity'] > 0:
                slot_1['quantity'] = id_3['quantity']
            elif slot_1['name'] == id_3['name'] and id_3['quantity'] == 0:
                slot_1 = None
            elif slot_2['name'] == id_3['name'] and id_3['quantity'] > 0:
                slot_2['quantity'] = id_3['quantity']
            elif slot_2['name'] == id_3['name'] and id_3['quantity'] == 0:
                slot_2 = None
            elif slot_3['name'] == id_3['name'] and id_3['quantity'] > 0:
                slot_3['quantity'] = id_3['quantity']
            elif slot_3['name'] == id_3['name'] and id_3['quantity'] == 0:
                slot_3 = None
        return slot_1, slot_2, slot_3      
@app.route('/')
def index():
        global slot_1
        global slot_2
        global slot_3
        global id_1
        global id_2
        global id_3
        global subTotal
        global subQuantity
        slot_1 = None
        slot_2 = None
        slot_3 = None
        quanS1 = 0
        quanS2 = 0
        quanS3 = 0
        id_1['quantity'] = 0
        id_2['quantity'] = 0
        id_3['quantity'] = 0
        id_1['total'] = 0
        id_2['total'] = 0
        id_3['total'] = 0
        subTotal = 0
        prepareBegin()
        return render_template('index.html', id_1=id_1, id_2=id_2, id_3=id_3, slot_1=slot_1, slot_2=slot_2, slot_3=slot_3)



#     data = {'product': product,'item1' : item1, 'item2': item2, 'item3' : item3}
# 
#     return render_template('index.html', **data)
@app.route('/pay')
def pay():
    return render_template('pay.html')
@app.route('/payment')
def action():
    global id_1, id_2, id_3
    global cb1, cb2, cb3
    global in1, in2, in3, in4
    count1 = int(id_1['quantity'])
    for i in range(1, count1 + 1 ):
        while(True):
            time.sleep(0.25)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            if GPIO.input(cb1) != 0:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                time.sleep(0.25)
                break
        while(True):
            if GPIO.input(cb1) == 0:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                time.sleep(0.25)
                break
            if GPIO.input(cb1) != 0 and i == count1:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                time.sleep(0.25)
                break
    if id_1['quantity'] > 0:
        SendFB(1)
        if id_1['stock'] > 0:
            id_1['stock'] = id_1['stock'] - id_1['quantity']
    time.sleep(1)
    count2 = int(id_2['quantity'])
    for i in range(1, count2 + 1 ):
        while(True):
            time.sleep(0.25)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            if GPIO.input(cb2) != 0:
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                time.sleep(0.25)
                break
        while(True):
            if GPIO.input(cb2) == 0:
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                time.sleep(0.25)
                break
            if GPIO.input(cb2) != 0 and i == count2:
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                time.sleep(0.25)
                break
    if id_2['quantity'] > 0:
        SendFB(2)
        if id_2['stock'] > 0:
            id_2['stock'] = id_2['stock'] - id_2['quantity']
    time.sleep(1)
    count3 = int(id_3['quantity'])
    for i in range(1, count3 + 1 ):
        while(True):
            time.sleep(0.25)
            GPIO.output(in5,GPIO.LOW)
            GPIO.output(in6,GPIO.HIGH)
            if GPIO.input(cb3) != 0:
                GPIO.output(in5,GPIO.LOW)
                GPIO.output(in6,GPIO.HIGH)
                time.sleep(0.25)
                break
        while(True):
            if GPIO.input(cb3) == 0:
                GPIO.output(in5,GPIO.LOW)
                GPIO.output(in6,GPIO.LOW)
                time.sleep(0.25)
                break
            if GPIO.input(cb3) != 0 and i == count3:
                GPIO.output(in5,GPIO.LOW)
                GPIO.output(in6,GPIO.LOW)
                time.sleep(0.25)
                break
    if id_3['quantity'] > 0:
        SendFB(3)
        if id_3['stock'] > 0:
            id_3['stock'] = id_3['stock'] - id_3['quantity']
    doanhso()
    return redirect(url_for('index'))
def doanhso():
    global id_1, id_2, id_3
    global DS1, DS2, DS3
    tg = datetime.now()
    dateStr = tg.strftime("%d-%m-%Y")
    DS1 = DS1 + id_1['quantity']
    DS2 = DS2 + id_2['quantity']
    DS3 = DS3 + id_3['quantity']
    sendDs = {
        'Time' : dateStr,
        'DS1' : DS1,
        'DS2' : DS2,
        'DS3' : DS3
        }
    database.child('DoanhSo').set(sendDs)
    
def SendFB(id_com):
    global id_1, id_2, id_3
    if id_com == 1:
        sendInfo = id_1
        tg = datetime.now()
        dateStr = tg.strftime("%d%m%Y%H%M%S")
        sendInfo["OrderCode"] = "NS"+ dateStr
        database.child("DH").set(sendInfo)
    elif id_com == 2:
        sendInfo = id_2
        tg = datetime.now()
        dateStr = tg.strftime("%d%m%Y%H%M%S")
        sendInfo["OrderCode"] = "CC"+ dateStr
        database.child("DH").set(sendInfo)
    elif id_com == 3:
        sendInfo = id_3
        tg = datetime.now()
        dateStr = tg.strftime("%d%m%Y%H%M%S")
        sendInfo["OrderCode"] = "MT"+ dateStr
        database.child("DH").set(sendInfo)
@app.route('/stock')
def stock():
    global id_1, id_2, id_3
    global id1Input, id2Input, id3Input
    id_1['stock'] = id_1['stock'] + id1Input
    id_2['stock'] = id_2['stock'] + id2Input
    id_3['stock'] = id_3['stock'] + id3Input
    id1Input = 0
    id2Input = 0
    id3Input = 0
    return render_template('stock.html', id_1=id_1, id_2=id_2, id_3=id_3)
@app.route('/stock/<product>/<status>')
def stockin(product, status):
    global id_1, id_2, id_3
    global id1Input, id2Input, id3Input
    if product == 'item1':
        if status == 'plus':
            id1Input = id1Input + 1
        elif status == 'minus' and id1Input > 0:
            id1Input = id1Input - 1
    if product == 'item2':
        if status == 'plus':
            id2Input = id2Input + 1
        elif status == 'minus' and id2Input > 0:
            id2Input =id2Input - 1
    if product == 'item3':
        if status == 'plus':
            id3Input =id3Input + 1
        elif status == 'minus' and id3Input > 0:
            id3Input = id3Input + 1
    return render_template('stock.html', input1=id1Input, input2=id2Input, input3=id3Input, id_1=id_1, id_2=id_2, id_3=id_3)
if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug=True)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
