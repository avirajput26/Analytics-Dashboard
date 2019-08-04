from flask import Flask, Markup, render_template , request
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import base64
app = Flask(__name__)

conn = MySQLdb.connect("localhost","root","","csvfile" )
cursor = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/csvfile'

db = SQLAlchemy(app)


class Csvrecords(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    advertiserName = db.Column(db.String(80),  nullable=False)
    publisherName = db.Column(db.String(80), nullable=False)
    impression = db.Column(db.String(80),  nullable=True)
    click = db.Column(db.String(20), nullable=True)
    install = db.Column(db.String(20), nullable=True)
    purchase = db.Column(db.String(20), nullable=True)
    os = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    deviceBrand = db.Column(db.String(80), nullable=False)




@app.route('/')
def home():
   return render_template('index.html')

# Inserting data from user into database :-
@app.route('/insert',methods=['GET','POST'])
def insert():
    #Add entry to the database
    if(request.method=='POST'):
      advertiserName=request.form.get('advertiserName')
      publisherName= request.form.get('publisherName')
      impression= request.form.get('impression')
      click= request.form.get('click')
      install = request.form.get('install')
      purchase= request.form.get('purchase')
      os= request.form.get('os')
      city = request.form.get('city')
      deviceBrand = request.form.get('deviceBrand')
      entry = Csvrecords(advertiserName=advertiserName, publisherName=publisherName, impression=impression, click=click, install=install, purchase=purchase, os=os, city=city, deviceBrand=deviceBrand )
      db.session.add(entry)
      db.session.commit()

    return render_template('insert.html')


#Fetch all Record from database and show all data :-
@app.route('/table')
def table():
    cursor.execute("select * from csvrecords")
    data = cursor.fetchall() #data from database
    return render_template("table.html", value=data)




""" Code fot ploting Bar graph by csv file :-

@app.route('/barGraph')
def barGraph(res):
   plt = pd.read_csv("assignment_data.csv",sep=",").set_index('advertiserName')
   plt.set_index('city')[['install', 'purchase']].plot.bar()
   res=plt.show()
 return render_template('barGraph.html',res=res)
 
 """

"""Code for ploting bar graph from datatable from database

@app.route('/barGraph')
def barGraph(res):
     cur = conn.cursor()
     x = cur.execute("SELECT `install`,`purchase`,`product title` FROM `csvrecords`")

     plt.xlabel('install')
     plt.ylabel('purchase')
     rows = cur.fetchall()
     df = pd.DataFrame([[xy for xy in x] for x in rows])
     x=df[0]
     y=df[1]
     plt.bar(x,y)
     plt.show()
     cur.close()
     conn.close()
"""
"""

#Code for ploting pie Chart from csv file
@app.route('/barGraph')
def pie()
    df =  pd.read_csv('assignment_data.csv')
    country_data = df["install"]
    medal_data = df["purchase"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b"]
    explode = (0.1, 0, 0, 0, 0)  
    plt.pie(advertiserName, labels=city, explode=explode, colors=colors,
    autopct='%1.1f%%', pieHole=0.4, shadow=True, startangle=140)
    plt.title("Pie Chart")
    plt.show()
"""



labels = ['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'JUL', 'AUG','SEP', 'OCT', 'NOV', 'DEC']

values = [967.67, 1190.89, 1079.75, 1349.19,2328.91, 2504.28, 2873.83, 4764.87,4349.29, 6458.30, 9907, 16297]

colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1","#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/piechart')
def pie():
   pie_labels = labels
   pie_values = values
   return render_template('piechart.html', title='Pie Chart', max=17000,set=zip(values, labels, colors))

@app.route('/barGraph')
def bar():
   bar_labels=labels
   bar_values=values
   return render_template('barGraph.html', title='Bar Graph', max=17000, labels=bar_labels, values=bar_values)





#app.run(host='0.0.0.0', port=5000)
app.run(debug=True)