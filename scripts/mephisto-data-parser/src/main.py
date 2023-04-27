import pathlib
from backend.task_user_data import *
from backend.database_handle import *
from backend.csv_handle import *
import sys

if __name__ == "__main__":
    # Load data from .env file

    # Folder link for tracking
    user_input_path = sys.argv[1]

    # Path to database
    database_folder_path = sys.argv[2]

    # Path to export CSV
    csv_folder_path = sys.argv[3]

    folder_link = pathlib.PurePath(user_input_path)
    csv_folder = pathlib.Path(csv_folder_path)

    # Create a user data frame (5 columns: user_id, task_id, user_dir, agent_data_dir, user_status, user_status in database)
    user_dataframe = CreateUserDataFrame(folder_link, database_folder_path)

    total_task = len(user_dataframe["task_id"].unique())

    total_user = user_dataframe.count()[0]
    if total_user == 0:
        print("No user found in the database")
        exit()

    user_have_outputs = user_dataframe["user_status"].value_counts()[True]

    user_do_not_have_outputs = user_dataframe["user_status"].value_counts()[False]

    # Create a dataframe for csv file include task_id, agent_id, agent_data_dir, agent_meta_dir
    csv_dataframe = CreateCSVDataFrame(user_dataframe)

    # Add input to data frame
    agent_data_dataframe = GetAgentsInput(csv_dataframe)

    # Add input to dataframe

    agent_data_dataframe = GetAgentsOutput(agent_data_dataframe)

    # Create dataframe for meta data

    agent_meta_dataframe = GetAgentMetaData(csv_dataframe)

    # Create dataframe for assign data

    assign_data_df = GetAssignData(csv_dataframe)

    PrintTaskInformation(user_dataframe)

    print(f"Total task: {total_task}")

    print(f"Total user: {total_user}")

    print(f"User that is snapped {GetSnappedUser(list(user_dataframe['user_id']))}")

    print(
        f"Number of user did the assignment: {user_have_outputs} - Account for: {round(user_have_outputs/total_user*100,2)}%"
    )
    print(
        f"Number of user did not do the assignment: {user_do_not_have_outputs} - Account for: {round(user_do_not_have_outputs/total_user*100,2)}%"
    )

    CompareFolderWithDatabase(user_dataframe)

    CreateCSVFile(agent_data_dataframe, csv_folder, "agent_data")

    CreateCSVFile(agent_meta_dataframe, csv_folder, "agent_meta")

    CreateCSVFile(assign_data_df, csv_folder, "assign_data")

    print("CSV File Created !!!!")
