from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector
import json
from datetime import datetime

# Create your views here.
def login(request):
    if (request.method == 'POST'):
        email = request.POST.get("customer[email]")
        password = request.POST.get("customer[password]")
        if (email=="" or password ==""):
            print("Enter all Fields")
            messages.error(request,'Enter all Fields')
            return render(request,'login.html')
        else:
            db = mysql.connector.connect(
                    host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                    username='admin',
                    password='Decent124',
                    database='stadorm'
                )
            cur = db.cursor()

            sql = "SELECT * FROM User WHERE email = '"+email+"';"

            cur.execute(sql)

            a = cur.fetchall()

            if (len(a) == 0):
                messages.error(request,"Email not registered")
            else:
                db_password = a[0][4]
                db_username = a[0][5]
                db_userId = a[0][0]
                if (db_password==password):
                    return redirect(str(db_userId)+'/'+str(db_username))
                else:
                    messages.error(request,"Incorrect Password")

        return render(request,'login.html')

    return render(request,'login.html')

def signup(request):
    if (request.method == 'POST'):
        email = request.POST.get("customer[email]")
        password = request.POST.get("customer[password]")
        fname = request.POST.get("customer[first_name]")
        lname = request.POST.get("customer[last_name]")
        username = request.POST.get("customer[user_name]")
        if (email=="" or password ==""or fname =="" or lname=="" or username==""):
            print("Enter all Fields")
            messages.error(request,'Enter all Fields')
            return render(request,'signup.html')
        else:
            db = mysql.connector.connect(
                    host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                    username='admin',
                    password='Decent124',
                    database='stadorm'
                )

            cur = db.cursor()

            sql = "INSERT INTO User (fname, lname, email, password, username) VALUE ('"+fname+"','"+lname+"','"+email+"','"+password+"','"+username+"');"

            try:
                cur.execute(sql)
            except:
                messages.error(request,'Email or Username already registered')
                return render(request,'signup.html')

            db.commit()

            messages.success(request,'Added the user')

    return render(request,'signup.html')

def home(request):
    db = mysql.connector.connect(
                host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                username='admin',
                password='Decent124',
                database='stadorm'
            )
    cur = db.cursor()
    sql = "SELECT * FROM Product WHERE type = 'r';"
    cur.execute(sql)
    a = cur.fetchall()
    a = list([list(i) for i in a])
    for i in range(len(a)):
        a[i].append(json.loads(a[i][5])[0])

    return render(request,'index.html',context={'a':a})

def rooms(request):
    db = mysql.connector.connect(
                host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                username='admin',
                password='Decent124',
                database='stadorm'
            )
    cur = db.cursor()
    sql = "SELECT * FROM Product WHERE type = 'r';"
    cur.execute(sql)
    a = cur.fetchall()
    a = list([list(i) for i in a])

    for i in range(len(a)):
        a[i].append(json.loads(a[i][5])[0])
    return render(request,'rooms.html',context={'a':a})

def details(request,productId):
    if (request.method == 'POST'):
        if request.POST.get("subscription") == 'true':
            length = request.POST.get("length")
        else:
            length = 0
        return redirect('/checkout/'+str(productId)+'/'+str(length)+'/')
    db = mysql.connector.connect(
                host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                username='admin',
                password='Decent124',
                database='stadorm'
            )
    cur = db.cursor()
    sql = "SELECT * FROM Product where productId = '"+str(productId)+"';"
    cur.execute(sql)
    a = cur.fetchall()
    a = list(a[0])
    images = json.loads(a[5])
    db.commit()

    return render(request,'details.html',context={'productId':productId,'a':a,'images':images})

def checkout(request,productId,length):
    db = mysql.connector.connect(
                host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                username='admin',
                password='Decent124',
                database='stadorm'
            )
    cur = db.cursor()
    if (request.method == 'POST'):
        email = request.POST.get("customer[email]")
        fname = request.POST.get("customer[first_name]")
        lname = request.POST.get("customer[last_name]")
        number = request.POST.get("customer[number]")
        if (email=="" or fname =="" or lname=="" or number == ""):
            print("Enter all Fields")
            messages.error(request,'Enter all Fields')
            return render(request,'checkout.html')
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        sql = "SELECT * FROM Product where productId = '"+str(productId)+"';"
        cur.execute(sql)
        a = cur.fetchall()
        a = list(a[0])
        type = a[3]
        amount = a[4]
        if length == 0:
            amount = 0
        sql = f"INSERT INTO Transaction (productId,date,length,type,amount,fname,lname,email,number) VALUE ({productId},'{date}',{length},'{type}',{amount},'{fname}','{lname}','{email}','{number}');"
        cur.execute(sql)
        db.commit()
        sql = "SELECT transactionId FROM Transaction ORDER BY transactionId DESC LIMIT 1;"
        cur.execute(sql)
        a = cur.fetchall()
        transactionId = list(a[0])[0]
        db.commit()
        return redirect(f'/confirmation/{productId}/{transactionId}/')

    sql = f"SELECT * FROM Product where productId = {productId}"
    cur.execute(sql)
    a = cur.fetchall()
    a = list(a[0])
    image = json.loads(a[5])[0]

    return render(request,'checkout.html',{'a':a,'image':image})

def subscription(request):
    return render(request,'subscription.html')

def confirmation(request,productId,transactionId):
    db = mysql.connector.connect(
                host='stadorm.cyw0lj2jrms0.ap-south-1.rds.amazonaws.com',
                username='admin',
                password='Decent124',
                database='stadorm'
            )
    cur = db.cursor()
    sql = f"SELECT * FROM Transaction Where transactionId = {transactionId};"
    cur.execute(sql)
    a = cur.fetchall()
    a = list(a[0])

    return render(request,'confirmation.html',{'a':a})
