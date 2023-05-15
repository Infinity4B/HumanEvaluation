from flask import Flask, redirect, url_for, request, render_template, send_from_directory
import yaml, json, os

def submitResult(task, num, resDict):
   with open(f'./results/{task}.json', 'r') as f:
      results = json.load(f)
   for key in resDict.keys():
      results[str(int(num) - 1)][key] = resDict[key]
   with open(f'./results/{task}.json', 'w') as f:
      json.dump(results, f, indent=4)

def readResult(task,num):
   with open(f'./results/{task}.json', 'r') as f:
      results = json.load(f)
   return results[str(int(num) - 1)]

app = Flask(__name__, root_path=os.getcwd(),static_folder=os.path.join(os.getcwd(),'static'))
with open('config.yml','r') as f:
   globalConfig = yaml.load(f, yaml.FullLoader)

@app.route('/favicon.ico')
def icon():
   return send_from_directory('./static/icon.svg')

@app.route('/')
def mainpage():
   tasks = globalConfig['tasks']
   return render_template('./index.html',tasks=tasks)

@app.route('/<task>/')
def rating(task):
   return redirect(f'/{task}/1')

@app.route('/<task>/<num>/submit',methods=['POST'])
def submit(task,num):
   submitResult(task, num, request.form.to_dict())
   totalNum = globalConfig['tasks'][task]['totalNum']
   if int(num) > totalNum:
      return redirect(f'/{task}/{totalNum}')
   else:
      return redirect(f'/{task}/{str(int(num)+1)}')

@app.route('/<task>/jump',methods=['POST'])
def direct(task):
   taskConfig = globalConfig['tasks'][task]
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
   taskConfig = globalConfig['tasks'][task]
   totalNum = taskConfig['totalNum']
   pageMax = totalNum // globalConfig['settings']['indexPerPage']
   page = int(request.args.get('page', 1))
   loopMax = totalNum if page*36 > totalNum else page*36
   with open(os.path.join(os.getcwd(),taskConfig['datasetPath']),'r') as f:
      data = json.load(f)
   resDict = readResult(task, num)

   if int(num) < 1:
      return redirect(f'/{task}/1')
   elif int(num) > totalNum:
      return redirect(f'/{task}/{totalNum}')
   if page < 1:
      return redirect(f'/{task}/{num}?page=1')
   elif page > pageMax + 1:
      return redirect(f'/{task}/{num}?page={pageMax+1}')
   else:
      return render_template('./taskSpecific.html',num=int(num),totalNum=totalNum,page=page,pageMax=pageMax,loopMax=loopMax,task=task,data=data,criterion=taskConfig['criterion'],resDict=resDict)

if __name__ == '__main__':
   app.run(debug=True)