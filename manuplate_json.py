import json
 
# Creating a dictionary
Dictionary ={1:'Welcome', 2:'to',
            3:'Geeks', 4:'for',
            5:'Geeks'}
  
# Converts input dictionary into
# string and stores it in json_string
json_string = json.dumps(Dictionary)
print('Equivalent json string of input dictionary:',
      json_string)
data_string = json.dumps(Dictionary, indent=2, default=str)
print("data_string: {}".format(data_string))
 
# Checking type of object
# returned by json.dumps
print(type(json_string))