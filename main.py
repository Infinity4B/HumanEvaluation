from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

TOTAL_NUM=20

@app.route('/')
def mainpage():
   file = './static/1.png'
   return render_template('./index.html',file=file)

@app.route('/<num>')
def rating_n(num):
   file = './static/1.png'
   return render_template('./index.html',file=file,num=num,totalNum=TOTAL_NUM)

if __name__ == '__main__':
   app.run(debug=True)