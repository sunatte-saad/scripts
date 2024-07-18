import os
import json
import random
import string


def get_folder_info(folder_path):
    folder_info = {}

    for root, dirs, files in os.walk(folder_path):
        current_folder_name = os.path.relpath(root, folder_path)

        if current_folder_name == '.':
            current_folder_info = {'files': files, 'subfolders': {}}
        else:
            current_folder_info = {'files': {current_folder_name: files}, 'subfolders': {}}

            for subfolder in dirs:
                subfolder_path = os.path.join(root, subfolder)
                subfolder_info = get_folder_info(subfolder_path)
                current_folder_info['subfolders'].update(subfolder_info)

        folder_info.update({current_folder_name: current_folder_info})

    return folder_info

def save_to_json(data, json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    folder_path = input("Enter the path of the main folder: ")

    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        folder_info = get_folder_info(folder_path)

        json_file_name = input("Enter the name of the JSON file (e.g., output.json): ")
        json_file_path = os.path.join(folder_path, json_file_name)

        save_to_json(folder_info, json_file_path)

        print(f"Information saved to {json_file_path}")
    else:
        print("Invalid folder path. Please provide a valid path.")

if __name__ == "__main__":
    main()