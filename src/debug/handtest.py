
#this is for my own sanity and to cross check results

temp1 = open("value_ids_20210307-130329", "r")
test1 = json.loads(temp1.read())
temp1.close()

temp2 = open("value_ids_20210307-130450", "r")
test2 = json.loads(temp2.read())
temp2.close()

temp3 = open("value_ids_20210307-130602", "r")
test3 = json.loads(temp3.read())
temp3.close()

if test1.keys() == test2.keys() == test3.keys():
    print("PASS")
else:
    print("FAILED")

# THIS FAILED FOR MOST RECENT TESTS