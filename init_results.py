import yaml, json, os

def init_results(config):
   tasks = config['tasks']
   for key in tasks.keys():
      output = {}
      name = key
      criterion = tasks[key]['criterion']
      num = tasks[key]['totalNum']
      for i in range(num):
         temp = {}
         for j in criterion:
            temp[list(j.keys())[0]] = -1
         output[i]=temp
      with open(f'./results/{name}.json','w') as f:
         json.dump(output,f,indent=4)

if __name__ == '__main__':
   with open('config.yml','r') as f:
      config = yaml.load(f, yaml.FullLoader)
   init_results(config)