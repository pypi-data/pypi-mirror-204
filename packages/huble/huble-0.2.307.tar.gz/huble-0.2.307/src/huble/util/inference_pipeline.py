def inference_pip(graph):
    id = "0"
    prediction_id = ""
    for node in graph["nodes"]:
        if node["data"]["node_type"] == "primary_dataset":
            node["data"]["name"] = "Web API"
        elif node["data"]["name"] == "Train-Test Split":
            prediction_id = node["id"]
            node["data"]["name"] = "Predictions"
            node["data"]["value"] = "Predictions"
            node["data"]["inputParameters"]["types"].append("Trained Model")
            node.pop("target")
            node["data"].pop("outputParameters")
            node["data"]["color"] = "green.400"
        elif node["data"]["name"] == "Train Model":
            id = node["id"]
        elif node["data"]["node_type"] == "essential":
            graph["nodes"].remove(node)

    for node in graph["nodes"]:
        if (
            node["data"]["node_type"] == "classification_model"
            or node["data"]["node_type"] == "regression_model"
            or node["data"]["node_type"] == "clusterring_model"
        ):
            # get node id and make an edge to predictions wala node
            node["data"]["name"] = "Trained " + node["data"]["name"]
            node["data"]["outputParameters"]["types"] = ["Trained Model"]
            node["data"]["color"] = "teal.600"
            graph["edges"].append(
                {
                    "source": node["id"],
                    "target": prediction_id,
                    "sourceHandle": "output_0_Trained Model",
                    "targetHandle": "input_1_Trained Model",
                    "type": "custom",
                    "id": f"reactflow_edge-{node['id']}output_0_Trained Model-{prediction_id}input_1_Trained Model",
                    "data": {
                        "sourceColor": "teal.600",
                        "targetColor": "green.400",
                        "target": prediction_id + "_input_1_Trained Model",
                        "source": node["id"] + "_output_0_Trained Model",
                    },
                }
            )

    graph["edges"] = [edge for edge in graph["edges"] if edge["target"] not in ["998", id]]
    graph["nodes"] = [
        node
        for node in graph["nodes"]
        if node["data"]["node_type"]
        in [
            "primary_dataset",
            "preprocess",
            "essential",
            "classification_model",
            "clusterring_model",
            "regression_model",
        ]
    ]

    return graph
