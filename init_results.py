import yaml, json, os
import argparse

def init_results(config, name):
   task = config['tasks'][name]
   output = {}
   criterion = task['criterion']
   num = task['totalNum']
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
   parser = argparse.ArgumentParser()
   parser.add_argument('-t','--task',dest='name',required=True)
   args = parser.parse_args()
   init_results(config, args.name)