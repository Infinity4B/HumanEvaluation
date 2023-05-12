from flask import Flask, redirect, url_for, request, render_template
import yaml, json, os


app = Flask(__name__, root_path=os.getcwd(),static_folder=os.path.join(os.getcwd(),'static'))

@app.route('/')
def mainpage():
   tasks = config['tasks']
   return render_template('./index.html',tasks=tasks)

@app.route('/<task>/')
def rating(task):
   return redirect(f'/{task}/1')

@app.route('/<task>/submit',methods=['POST'])
def submit(task):
   return redirect('/')

@app.route('/<task>/jump',methods=['POST'])
def direct(task):
   taskConfig = config['tasks'][task]
   totalNum = taskConfig['totalNum']
   if request.method == 'POST':
      num = request.form['num']
      if int(num) < 1:
         return redirect(f'/{task}/1')
      elif int(num) > totalNum:
         return redirect(f'/{task}/{totalNum}')
      else:
         return redirect(f'/{task}/{num}')
   
   return redirect('/')

@app.route('/<task>/<num>')
def rating_n(task, num):
   taskConfig = config['tasks'][task]
   totalNum = taskConfig['totalNum']
   pageMax = totalNum // config['settings']['indexPerPage']
   page = int(request.args.get('page', 1))
   loopMax = totalNum if page*36 > totalNum else page*36
   with open(os.path.join(os.getcwd(),taskConfig['datasetPath']),'r') as f:
      data = json.load(f)
   
   if int(num) < 1:
      return redirect(f'/{task}/1')
   elif int(num) > totalNum:
      return redirect(f'/{task}/{totalNum}')
   return render_template('./taskSpecific.html',num=int(num),totalNum=totalNum,page=page,pageMax=pageMax,loopMax=loopMax,task=task,data=data,criterion=taskConfig['criterion'])

if __name__ == '__main__':
   with open('config.yml','r') as f:
      config = yaml.load(f, yaml.FullLoader)
   app.run(debug=True)