from flask import Flask, redirect, url_for, request, render_template
# from flask_paginate import Pagination, get_page_parameter
app = Flask(__name__)

TOTAL_NUM=200
INDEX_PAGES=TOTAL_NUM//36

@app.route('/')
def mainpage():
   file = './static/1.png'
   return render_template('./index.html',file=file)

@app.route('/<num>')
def rating_n(num):
   page = int(request.args.get('page', 1))
   file = './static/1.png'
   return render_template('./index.html',file=file,num=num,totalNum=TOTAL_NUM,page=page)

if __name__ == '__main__':
   app.run(debug=True)