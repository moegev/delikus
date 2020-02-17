import requests
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("src_file", help="the .txt file with the relevant users, datatsets and filenames.")
parser.add_argument("level", help="The level at which you want the files edited.")

args = parser.parse_args()
##import data 

users = {}
url_endings = []
url_endings.append(".com")

with open(args.src_file, 'r') as f:
    for line in f:
        line = line.strip()
        end = line[-4:]
        if end in url_endings:
            user = line
        elif end == "-dts":
            dataset = line
            dataset = dataset[:-4]
        else:
            users.setdefault(user, {}).setdefault(dataset, []).append(line)
##send the data
print(users)

headers = {
    'Content-Type': 'application/json',
}

auth = (
    'moe@hotpepper.deepgram.com',
    'makati2019!1'
)
lvl = args.level

data_string = "'user':{user}, 'file':'{file}', 'dataset':{dataset}, 'level':{level}, 'status':'available'"
for user, user_data in users.items():
    json_string = json.dumps(user_data)
    for element, value in user_data.items():
        for item in value:
            data = {"user": user, "file":item, "level":lvl, "dataset":element}
            r = requests.patch('https://hotpepper.deepgram.com/ui/file-status', headers=headers, json=data, auth=auth)
            print(r.status_code)