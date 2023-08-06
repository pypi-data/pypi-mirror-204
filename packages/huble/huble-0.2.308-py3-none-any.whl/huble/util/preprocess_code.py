from ..sklearn.process.handler import PreprocessHandler
from ..sklearn.graph import Graph
from .typed_params import get_typed_params

def preprocess_code_generation(graph, colab=False):
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
    map2 = {y: x for x, y in map.items()}
    for i in graph["edges"]:
        g.addEdge(map[i["source"]], map[i["target"]])
    res = g.topologicalSort()
    steps = []
    for i in res:
        steps.append(map2[i])
    steps_list = {}
    for i in steps:
        for j in range(len(graph["nodes"])):
            if i == graph["nodes"][j]["id"]:
                steps_list[(graph["nodes"][j]["data"]["name"])] = graph["nodes"][j][
                    "data"
                ]["node_type"]
    if colab:
        output_file = "/content/preprocess_code.py"
    else:
        output_file = "preprocess.py"
    preprocess_handler = PreprocessHandler()
    with open(output_file, "w") as f:
        f.write("import huble\n")
        f.write("def preprocess_code(data):\n")
        for i in steps_list:
            node = graph_dict[i]
            params = get_typed_params(node["data"]["parameters"])
            if steps_list[i] == "preprocess":
                f.write(
                    "\t"
                    + preprocess_handler.return_function(
                        function_name=node["data"]["name"], params=params
                    )
                )
                f.write("\n")

        f.write("\n\treturn data")
