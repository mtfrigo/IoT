import json
datastore = { 
   "devices":  [
      { 
         "mac": "00:b3:62:b9:7b:97",
         "description": "Phone",
         "owner": "Pedro"
      },
      { 
         "mac": "2c:6f:c9:66:11:b7",
         "description": "Notebook",
         "owner": "Matheus"
      },
   ]
} 


json_string = json.dumps(datastore)

datastore = json.loads(json_string)
 
def writeJSON():
   with open('devices.txt', 'w') as outfile:
      json.dump(datastore, outfile)

      outfile.close()


def readJSON():
   #prompt the user for a file to import
   with open('devices.txt') as json_file:
      data = json.load(json_file)
      for d in data['devices']:
         print('Owner: ' + d['owner'])
         print('mac: ' + d['mac'])
         print('Description: ' + d['description'])
         print('')

      json_file.close()

def main():
   writeJSON()
   readJSON()

if __name__ == "__main__":
   main()