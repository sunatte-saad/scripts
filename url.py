import os
import json

def save_to_json(data, json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

#def read_files(folder_path, base_url="https://data.adictoai.com"):
def read_files(folder_path):

    result = []

    def recursive_read(current_path):
        current_result = []
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                subfolder_data = {}
                subfolder_data['title'] = item
                subfolder_data['data'] = recursive_read(item_path)
                current_result.append(subfolder_data)
            elif os.path.isfile(item_path) and item != ".DS_Store" and item != "Thumbs.db":
                #current_result.append(base_url + item_path[len(folder_path):].replace(os.path.sep, '/'))
                current_result.append(item_path[len(folder_path):].replace(os.path.sep, '/'))
                

        return current_result

    result = recursive_read(folder_path)
    return result

folder_path = "/Volumes/shared_folder/inamface/videos"
files_data = read_files(folder_path)

json_result = json.dumps(files_data, indent=4)
print(json_result)

save_to_json(files_data, "videos.json")
