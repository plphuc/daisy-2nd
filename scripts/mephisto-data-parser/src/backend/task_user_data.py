import os
import json
import pathlib
import pandas as pd

from .database_handle import GetStatusOfAgentId, ConnectDatabse
from pandas import DataFrame


# Get list of all tasks
def CreateTaskDirList(folder_link: pathlib.PurePath):
    task_dir_list = []
    for subdir, dirs, files in os.walk(folder_link):
        current_dir = pathlib.PurePath(subdir)
        current_folder = pathlib.PurePath(current_dir).name
        try:
            int(current_folder)
        except ValueError:
            continue
        if current_dir != folder_link and current_dir.parent not in task_dir_list:
            task_dir_list.append(current_dir)

    return task_dir_list


# Function finding a list of user directory for each assignment
def CreateUserDirList(assignment_dir):
    user_dir_list = []

    for subdir, dirs, files in os.walk(assignment_dir):
        current_dir = pathlib.PurePath(subdir)
        if current_dir == assignment_dir:
            for dir in dirs:
                if dir.isdigit():
                    user_dir_list.append(current_dir.joinpath(dir))
        else:
            continue

    return user_dir_list


def GetOutputsResults(json_dir):
    try:
        file_dir = pathlib.PurePath(json_dir).joinpath("agent_data.json")
        json_file = open(file_dir)
    except:
        return False
    data: dict = json.load(json_file)
    if data.get("outputs") != None:
        return True
    else:
        return False


def GetTaskOrUserNumber(user_or_task_dir):
    return pathlib.PurePath(user_or_task_dir).name


# Function for getting snapped User Number
def GetSnappedUser(user_list: list):
    maximum_user_number = 0
    snapped_user_arr = []

    for user in user_list:
        if user > maximum_user_number:
            maximum_user_number = user

    for i in range(1, maximum_user_number + 1):
        if i not in user_list:
            snapped_user_arr.append(i)

    return snapped_user_arr


def CreateTaskDir(task_number, folder_link):
    return pathlib.PurePath.joinpath(folder_link, str(task_number))


# Create a data frame for user
def CreateUserDataFrame(folder_link, database_path):
    task_dir_list = CreateTaskDirList(folder_link)

    user_data = {
        "user_id": [],
        "task_id": [],
        "user_dir": [],
        "agent_data_dir": [],
        "agent_meta_dir": [],
        "assign_data_dir": [],
        "user_status": [],
        "data_base_status": [],
    }

    for task_dir in task_dir_list:
        user_dir_list = CreateUserDirList(task_dir)
        for user_dir in user_dir_list:
            user_data["user_id"].append(int(GetTaskOrUserNumber(user_dir)))
            user_data["task_id"].append(int(GetTaskOrUserNumber(task_dir)))
            user_data["user_dir"].append(user_dir)
            user_data["agent_data_dir"].append(
                pathlib.PurePath(user_dir).joinpath("agent_data.json")
            )
            user_data["agent_meta_dir"].append(
                pathlib.PurePath(user_dir).joinpath("agent_meta.json")
            )
            user_data["assign_data_dir"].append(
                pathlib.PurePath(user_dir).joinpath("assign_data.json")
            )
            user_data["user_status"].append(GetOutputsResults(user_dir))
            user_data["data_base_status"].append(
                GetStatusOfAgentId(
                    ConnectDatabse(database_path), GetTaskOrUserNumber(user_dir)
                )
            )

    user_dataframe = pd.DataFrame(data=user_data)

    sorted_user_dataframe = user_dataframe.sort_values("task_id")

    return sorted_user_dataframe


def PrintTaskInformation(user_dataframe: DataFrame):
    for task_id in list(user_dataframe["task_id"].unique()):
        print(f"Task:{task_id}")
        number_of_user = len(user_dataframe[user_dataframe["task_id"] == task_id])
        user_did_assignment = list(
            user_dataframe.loc[
                (user_dataframe["task_id"] == task_id)
                & (user_dataframe["user_status"] == True)
            ]["user_id"]
        )

        user_did_not_do_assignment = list(
            user_dataframe.loc[
                (user_dataframe["task_id"] == task_id)
                & (user_dataframe["user_status"] == False)
            ]["user_id"]
        )
        print(
            f"Total agents: {number_of_user} - Agent did the assignment:{user_did_assignment}  - Agent did not do the assignment: {user_did_not_do_assignment} "
        )
    return
