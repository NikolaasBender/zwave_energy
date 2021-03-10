import time
import json
import os

path = "../notes/value_ids_raw"
directories = os.listdir( path )
data = {}
# This would print all the files and directories
for file in directories:
    f = open(path + '/' + file)
    data[file] = sorted(json.loads(f.read()).keys())
    f.close()

similarities = data[directories[0]]

for d in range(0, len(directories)):
    for g in range(0, len(directories)):
        if data[directories[d]] != data[directories[g]]:
            print(directories[d], directories[g], "not equal")
            between = list(set(data[directories[d]]).intersection(set(data[directories[g]])))
            similarities = list(set(between).intersection(set(similarities)))
    print(similarities, len(similarities))

f = open("useful_ids.txt", "w")
for e in similarities:
    f.write(e)
    f.write('\n')
f.close()