import pandas as pd
import pathlib
from pandas import DataFrame
import json


def CreateCSVDataFrame(user_dataframe: DataFrame):
    agent_data = {
        "task_id": [],
        "agent_id": [],
        "agent_data_dir": [],
        "agent_meta_dir": [],
        "assign_data_dir": [],
    }

    for i in range(user_dataframe.shape[0]):
        agent_data["task_id"].append(int(user_dataframe["task_id"][i]))
        agent_data["agent_id"].append(int(user_dataframe["user_id"][i]))
        agent_data["agent_data_dir"].append(user_dataframe["agent_data_dir"][i])
        agent_data["agent_meta_dir"].append(user_dataframe["agent_meta_dir"][i])
        agent_data["assign_data_dir"].append(user_dataframe["assign_data_dir"][i])

    agent_data_dataframe = pd.DataFrame(data=agent_data)
    agent_data_dataframe.sort_values(
        ["task_id", "agent_id"], ascending=[True, True], inplace=True
    )

    return agent_data_dataframe


def GetAgentsInput(csv_dataframe: DataFrame):
    agent_data_list = list(csv_dataframe["agent_data_dir"])
    agent_inputs_list = list()
    output_df = pd.DataFrame.assign(csv_dataframe)

    for file in agent_data_list:
        try:
            json_file = open(file)
        except:
            agent_inputs_list.append(None)
            continue
        data: dict = json.load(json_file)
        # Currently leave as string
        agent_inputs_list.append(str(data.get("inputs")))

    output_df["agent_inputs"] = agent_inputs_list

    return output_df


def GetAgentsOutput(csv_dataframe: DataFrame):
    agent_data_list = csv_dataframe["agent_data_dir"]

    outputs = []
    indices = []
    for index, file in agent_data_list.items():
        try:
            json_file = open(file)
        except:
            continue
        data: dict = json.load(json_file)
        outputs_dict: dict = data.get("outputs")
        if outputs_dict == None:
            continue
        else:
            unnested_dict = {}
            for key, value in outputs_dict.items():
                if isinstance(value, dict):
                    for k, v in value:
                        unnested_dict[f"{key}.{k}"] = v
                else:
                    unnested_dict[f"outputs.{key}"] = value
            outputs.append(unnested_dict)
            indices.append(index)

    output_df = pd.DataFrame.from_records(outputs, index=indices)
    csv_dataframe = csv_dataframe.join(output_df)

    return csv_dataframe


def GetAgentMetaData(csv_dataframe: DataFrame):
    agent_meta_list = list(csv_dataframe["agent_meta_dir"])
    outputs = []

    for file in agent_meta_list:
        try:
            json_file = open(file)
        except:
            continue
        data: dict = json.load(json_file)
        for k, v in data.items():
            if isinstance(v, list):
                data[k] = str(v)

        outputs.append(data)

    outputs_df = pd.DataFrame.from_records(outputs)

    return csv_dataframe.join(outputs_df)


def GetAssignData(csv_dataframe: DataFrame):
    assign_data_list = list(csv_dataframe["assign_data_dir"])
    outputs = []

    for file in assign_data_list:
        try:
            json_file = open(file)
        except:
            continue
        data: dict = json.load(json_file)
        for k, v in data.items():
            if isinstance(v, list):
                data[k] = str(v)

        outputs.append(data)

        outputs_df = pd.DataFrame.from_records(outputs)

    return csv_dataframe.join(outputs_df)


def CreateCSVFile(dataframe: DataFrame, folder_link, type):
    # Check if csv_dir exists if not create new folder
    if not pathlib.Path(folder_link).exists():
        pathlib.Path(folder_link).mkdir(parents=True, exist_ok=True)

    csv_dir = pathlib.PurePath(folder_link).joinpath(f"{type}.csv")
    dataframe.to_csv(csv_dir)
    return
