import json

with open('./VCRref_ori.json','r') as f:
    datas = json.load(f)

output = {}
for key in datas.keys():
    cur = {}
    cur_item = datas[key]
    cur['path'] = '/static/images/VCR/' + cur_item['id'] + '.png'
    cur['Question'] = cur_item['que'][0]
    cur['Label'] = cur_item['label'][0]
    cur['Predition'] = cur_item['pred']
    output[key] = cur

with open('./VCRref.json','w') as f1:
    json.dump(output, f1, indent=4)