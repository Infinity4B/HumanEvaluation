from flask import Flask, redirect, url_for, request, render_template, send_from_directory, flash
import yaml, json, os


app = Flask(__name__, root_path=os.getcwd(),static_folder=os.path.join(os.getcwd(),'static'))


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

def getIndexState(task, page, totalNum):
   with open(f'./results/{task}.json', 'r') as f:
      results = json.load(f)
   with open('config.yml','r') as f:
      globalConfig = yaml.load(f, yaml.FullLoader)
   res = []
   per = globalConfig['settings']['indexPerPage']
   loopMax = totalNum if page*per > totalNum else page*per
   for i in range((page-1)*per, loopMax):
      if checkFilled(results[str(i)]):
         res.append(1)
      else:
         res.append(0)
   return res

def checkFilled(res:dict):
   for key in res.keys():
      if res[key] == -1:
         return False
   return True

@app.route('/favicon.ico')
def icon():
   return send_from_directory('./static/icon.svg')

@app.route('/')
def mainpage():
   with open('config.yml','r') as f:
      globalConfig = yaml.load(f, yaml.FullLoader)
   tasks = globalConfig['tasks']
   return render_template('./index.html',tasks=tasks)

@app.route('/<task>/')
def rating(task):
   return redirect(f'/{task}/1')

@app.route('/createTask')
def createTask():
   return render_template('./createTask.html')

@app.route('/<task>/<num>/submit',methods=['POST'])
def submit(task,num):
   submitResult(task, num, request.form.to_dict())
   with open('config.yml','r') as f:
      globalConfig = yaml.load(f, yaml.FullLoader)
   totalNum = globalConfig['tasks'][task]['totalNum']
   if int(num)+1 > totalNum:
      return redirect(f'/{task}/{totalNum}')
   else:
      return redirect(f'/{task}/{str(int(num)+1)}')

@app.route('/<task>/jump',methods=['POST'])
def direct(task):
   with open('config.yml','r') as f:
      globalConfig = yaml.load(f, yaml.FullLoader)
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
   with open('config.yml','r') as f:
      globalConfig = yaml.load(f, yaml.FullLoader)
   taskConfig = globalConfig['tasks'][task]
   totalNum = taskConfig['totalNum']
   pageMax = totalNum // globalConfig['settings']['indexPerPage']
   per = globalConfig['settings']['indexPerPage']
   page = int(request.args.get('page', 1))
   loopMax = totalNum if page*per > totalNum else page*per
   with open(os.path.join(os.getcwd(),taskConfig['datasetPath']),'r') as f:
      data = json.load(f)
   resDict = readResult(task, num)
   indexState = getIndexState(task,page,totalNum)
   usePicture = taskConfig['usePicture']

   if int(num) < 1:
      return redirect(f'/{task}/1')
   elif int(num) > totalNum:
      return redirect(f'/{task}/{totalNum}')
   if page < 1:
      return redirect(f'/{task}/{num}?page=1')
   elif page > pageMax + 1:
      return redirect(f'/{task}/{num}?page={pageMax+1}')
   else:
      return render_template('./taskSpecific.html',num=int(num),totalNum=totalNum,page=page,pageMax=pageMax,loopMax=loopMax,task=task,data=data,criterion=taskConfig['criterion'],resDict=resDict,per=per,indexState=indexState, usePicture=usePicture)

if __name__ == '__main__':
   app.run(debug=True)