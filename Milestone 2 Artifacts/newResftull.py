#!/usr/bin/python
import json # Imports JSON library to handle JSON files.
from bson import json_util # Imports json_util from bson, allowing for the 'dumps' function to be imported in the next line.
from bson.json_util import dumps
import bottle # Imports bottle library, allowing for the import of the route, run, request, and abort functions in the next line. 
from bottle import route, run, request, abort  

#imports for database
from pymongo import MongoClient 
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']
collection_comp = db['company']



# Configures URI paths for REST service
@route('/createStock/<ticker>', method='POST')
def createStock(ticker):
  data = request.json
  data.update( {'Ticker' : ticker} ) # Add Ticker key and its value to the passed dictionary.
  print(data)
  for item in data:
    print(data[item])
  record_created = collection.insert(data) # Insert data to the collection.
  added_doc = collection.find_one({"_id":record_created})
  stars = "*" * 0+"\n"
  return stars+ "Created Document \n "+dumps(added_doc)+"\n\n "+stars # Return inserted document.


# Update stock with put.
@route('/updateStock/<ticker>', method='PUT')
def createStock(ticker):
  data = request.json # Obtain the request data.
  print(data) # Print data.
  query = { "Ticker" :ticker} # Formulates query.
  #The below for loop take an value of the key and set it .
  #To the key in the collection.
  for item in data:
    print(data[item])
    new_update =  { "$set":{item:data[item]}}
    collection.update(query,new_update)
  updated_doc = collection.find({"Ticker":ticker}) # Find all the updated documents returns a list of document objects.
  stars = "*" * 50 +"\n" # A line of 50 asterisks as a string, followed by a new line command.
  result = dumps(updated_doc) #
  return stars+"\n"+str(result)+"\n"+stars
  


# When creating the query.
@route('/getStock/<Ticker>', method='GET')
def get_data(Ticker):
  found_doc = collection.find({"Ticker":Ticker}) # Finds all documenst whose ticker value is equal to the one provided.
  return dumps(found_doc)


@route('/deleteStock/<Ticker>', method='GET')
def get_update(Ticker):
  query = {"Ticker" :Ticker} # Formulates query.
  print(query) # Print the query not necessary just for testing.
  result = collection.delete_many(query) # Delete all the documents whose Ticker value is equal to the provided Ticker value.
  return "document with Ticker "+Ticker+" Has beed deleted from the stocks Collection" # Return results to the user.

@route('/stockReport', method='POST')
def run_create(): 
  mylist = request.json.get('list') # Retrieves the value of the list key in the url data.
  mylist = mylist.replace("[","") # Removes [ character from string.
  mylist = mylist.replace("]","") # Removes ] character from string. 
  mylist = list(mylist.split(",")) # Create a list from the remaining list.
  items = list()
  print(mylist)
  # This for loop uses each ticker in the list,
  # gets the summarry and adds the summery to the items list
  for name in mylist:
    print(name)
    item = getReport(name)
    print(item)
    items.append("Report For Ticker "+name+" \n"+item+"\n\n")
  return items # Return a lit of items.

# Some industry names contain spaces.
# Passing them with spaces result to errors, therefore we add semi colons to the spacesthe first method then removes.
# Them to obtain the original industry name.
@route('/industryReport/<industry>', method='GET')
def run_create(industry):
  industry = industry.replace("_"," ")
  print(industry)
  # Stage one specifies values to be included in the next stages of the pipeline.
  stage_one = { '$project': {'Industry':1, 'Ticker':1,'Performance (YTD)':1,'Performance (Week)':1,'Shares Outstanding':1,'Volume':1 } }
  # Stage two specifies the types of documens to deal with i.e the documents whose industry is given.
  stage_two = { '$match': { "Industry": industry } }
  # Stage three uses group and other operators to obtain summery of the documents.
  stage_three = { '$group': { '_id': "$Industry", 'Total Shares Outstanding': {'$sum': "$Shares Outstanding" },
                           'Average Performance (YTD)':{'$avg':"$Performance (YTD)"},
                           'Average Performance (Week)':{'$avg':'$Performance (Week)'},
                           'Max Shares Outstanding':{'$max':'$Shares Outstanding'},
                           'Total Volume':{'$sum':'$Volume'} } }
  # Stage four detrmines number of items to deal with.
  stage_four = { '$limit' : 5 }
  query = [stage_one,stage_two,stage_three,stage_four]
  # Perform the agregation.
  result=collection.aggregate(query)
  result = dumps(result)
  # Print results to user.
  return "-------- \n Portfolio Report For The First Five "+industry+" Industries \n\n "+result+" \n-------- \n\n"


@route('/portfolio/<company>', method='GET')
def run_create(company):
  company = company.replace("_"," ") # Removes underscore form the string.
  print(company)
  query = {"Company":company} # Formulates query.
  result=collection.find(query) # Find documents using the query.
  result = dumps(result)
  return "-------- \n Portfolio Report For "+company+" Company \n\n "+result+" \n-------- \n\n"
    
    

def getReport(ticker):
  # Stage one specifies the fields to be passed to the next stages.
  stage_one = { '$project': { 'Ticker':1,'Performance (YTD)':1,'Performance (Week)':1,'Shares Outstanding':1,'Volume':1 } }
  # Specifies the documenst to deal with.
  stage_two = { '$match': { "Ticker": ticker } }
  # Stage three uses group to group and find sum, avg and other operations.
  stage_three = { '$group': { '_id': "$Ticker", 'Total Shares Outstanding': {'$sum': "$Shares Outstanding" },
                           'Average Performance (YTD)':{'$avg':"$Performance (YTD)"},
                           'Average Performance (Week)':{'$avg':'$Performance (Week)'},
                           'Max Shares Outstanding':{'$max':'$Shares Outstanding'},
                           'Total Volume':{'$sum':'$Volume'} } }
  query = [stage_one,stage_two,stage_three] # Formlates query.
  result=collection.aggregate(query) # Performs aggregation.
  result = dumps(result)
  return result
  
if __name__ == '__main__':
  run(debug=True,reloader = True)
  #run(host='localhost', port=8080)