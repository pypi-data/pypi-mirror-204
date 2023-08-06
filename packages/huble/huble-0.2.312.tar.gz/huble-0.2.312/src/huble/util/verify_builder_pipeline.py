import pandas as pd
from sklearn.graph import Graph
from collections import Counter


def verify_pipeline(graph):
    issues = []
    steps = {}
    for node in graph["nodes"]:
        steps[node["data"]["name"]] = node["data"]["node_type"]
        if node["data"]["node_type"] == "primary_dataset" or node["data"]["node_type"] == "model" or node["data"]["node_type"] == "classification_model" or node["data"]["node_type"] == "regression_model":
            if "target" not in node:
                issues.append(node["data"]["name"] + " Node not connected")
        elif node["data"]["node_type"] == "evaluate_model":
            counter =0
            for i in graph['edges']:
              if i["target"]=="998":
                  counter+=1
            if counter<2:
                issues.append(node["data"]["name"] + " Node not connected")
        else:
            id = node['id']
            
            inputs = len(node['data']['inputParameters']['types'])
            outputs = len(node['data']['outputParameters']['types'])
            input=0
            output=0
            for i in graph['edges']:
              if i['target']==id:
                input+=1
              elif i['source']==id:
                output+=1
            
            if input!=inputs or output!=outputs:
                issues.append(node["data"]["name"] + " Node not connected")

    value_counter = Counter(steps.values())
    key_counter = Counter(steps.keys())
  
    if 'Train Model' not in steps:
      issues.append('Train Model Node Missing')
    elif key_counter['Train Model']>1:
      issues.append('More than one Train Model Node found')
    if 'Train-Test Split' not in steps:
      issues.append('Train-Test Split Node Missing')
    elif key_counter['Train-Test Split']>1:
      issues.append('More than one Train-Test Split Node found')
    if 'Evaluate Model' not in steps:
      issues.append('Evaluate Model Node Missing')
    elif key_counter['Evaluate Model']>1:
      issues.append('More than one Evaluate Model Node found')
    if 'model' not in steps.values() and 'classification_model' not in steps.values() and 'regression_model' not in steps.values():
      issues.append('Model Node Missing')
    elif value_counter['model']>1:
      issues.append('More than one Model Node found')
    if 'primary_dataset' not in steps.values():
      issues.append('Dataset Node Missing')
    elif value_counter['primary_dataset']>1:
      issues.append('More than one Dataset Node found')

    g = Graph(len(graph["nodes"]))
    graph_dict = {}
    for i in graph["nodes"]:
        graph_dict[(i["data"]["name"])] = i
    map = {}
    j = 0
    while j < (len(graph["nodes"])):
        for i in graph["nodes"]:
            map[(i["id"])] = j
            j += 1
  
    for i in graph["edges"]:
        g.addEdge(map[i["source"]], map[i["target"]])

    if g.isCyclic() == 1:
        issues.append("Graph contains cycle")
    else:
        pass

    return issues
