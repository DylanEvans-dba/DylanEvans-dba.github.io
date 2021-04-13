#!/usr/bin/python
import json
from bson import json_util
from bson.json_util import dumps
import bottle
from bottle import route, run, request, abort
#imports for database
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']
collection_comp = db['company']



# set up URI paths for REST service
@route('/createStock/<ticker>', method='POST')
def createStock(ticker):
  data = request.json
  data.update( {'Ticker' : ticker} ) #add Ticker key and its value to the passed dictionary.
  print(data)
  for item in data:
    print(data[item])
  record_created = collection.insert(data) #insert data to the collection
  added_doc = collection.find_one({"_id":record_created})
  stars = "*" * 0+"\n"
  return stars+ "Created Document \n "+dumps(added_doc)+"\n\n "+stars #return inserted document.


#Update stock with put
@route('/updateStock/<ticker>', method='PUT')
def createStock(ticker):
  data = request.json #obtain the request data
  print(data) #print data
  query = { "Ticker" :ticker} #formulates query
  #the below for loop take an value of the key and set it 
  #to the key in the collection
  for item in data:
    print(data[item])
    new_update =  { "$set":{item:data[item]}}
    collection.update(query,new_update)
  updated_doc = collection.find({"Ticker":ticker}) # find all the updated documents returns a list of document objects
  stars = "*" * 50 +"\n" #a lineof 50 stars strings
  result = dumps(updated_doc) #
  return stars+"\n"+str(result)+"\n"+stars
  


#when creating the query
@route('/getStock/<Ticker>', method='GET')
def get_data(Ticker):
  found_doc = collection.find({"Ticker":Ticker}) #finds all documenst whose ticker value is equal to the one
  #provided
  return dumps(found_doc)


@route('/deleteStock/<Ticker>', method='GET')
def get_update(Ticker):
  query = {"Ticker" :Ticker} #formulates query
  print(query) #print the query not necessary just for testing
  result = collection.delete_many(query) #delete all the documents whose Ticker value is equal to the provided Ticker value
  return "document with Ticker "+Ticker+" Has beed deleted from the stocks Collection" #return results to the user.

@route('/stockReport', method='POST')
def run_create(): 
  mylist = request.json.get('list') #retrieves the value of the list key in the url data
  mylist = mylist.replace("[","") #removes [
  mylist = mylist.replace("]","") #removes ]
  mylist = list(mylist.split(",")) #create a list from the remaining list
  items = list()
  print(mylist)
  #This for loop uses each ticker in the list,
  #get ist summer and add the summery to the items list
  for name in mylist:
    print(name)
    item = getReport(name)
    print(item)
    items.append("Report For Ticker "+name+" \n"+item+"\n\n")
  return items #return a lit of items

#some industry names contain spaces
#passing them with spaces result to errors, therefore we add semi colons to the spacesthe first method then removes
#them to obtain the original industry name
@route('/industryReport/<industry>', method='GET')
def run_create(industry):
  industry = industry.replace("_"," ")
  print(industry)
  #stage one specifies values to be included in the next stages of the pipeline
  stage_one = { '$project': {'Industry':1, 'Ticker':1,'Performance (YTD)':1,'Performance (Week)':1,'Shares Outstanding':1,'Volume':1 } }
  #stage two specifies the types of documens to deal with i.e the documents whose industry is given.
  stage_two = { '$match': { "Industry": industry } }
  #stage three uses group and other operators to obtain summery of the documents
  stage_three = { '$group': { '_id': "$Industry", 'Total Shares Outstanding': {'$sum': "$Shares Outstanding" },
                           'Average Performance (YTD)':{'$avg':"$Performance (YTD)"},
                           'Average Performance (Week)':{'$avg':'$Performance (Week)'},
                           'Max Shares Outstanding':{'$max':'$Shares Outstanding'},
                           'Total Volume':{'$sum':'$Volume'} } }
  #stage four detrmines number of items to deal with
  stage_four = { '$limit' : 5 }
  query = [stage_one,stage_two,stage_three,stage_four]
  #perform the agregation
  result=collection.aggregate(query)
  result = dumps(result)
  #print results to user.
  return "-------- \n Portfolio Report For The First Five "+industry+" Industries \n\n "+result+" \n-------- \n\n"


@route('/portfolio/<company>', method='GET')
def run_create(company):
  company = company.replace("_"," ") #removes underscore form the string
  print(company)
  query = {"Company":company} #formulates query
  result=collection.find(query) #find documents using the query
  result = dumps(result)
  return "-------- \n Portfolio Report For "+company+" Company \n\n "+result+" \n-------- \n\n"
    
    

def getReport(ticker):
  #stage one specifies the fields to be passed to the next stages
  stage_one = { '$project': { 'Ticker':1,'Performance (YTD)':1,'Performance (Week)':1,'Shares Outstanding':1,'Volume':1 } }
  #specifies the documenst to deal with
  stage_two = { '$match': { "Ticker": ticker } }
  #stage three uses group to group and find sum, avg and other operations
  stage_three = { '$group': { '_id': "$Ticker", 'Total Shares Outstanding': {'$sum': "$Shares Outstanding" },
                           'Average Performance (YTD)':{'$avg':"$Performance (YTD)"},
                           'Average Performance (Week)':{'$avg':'$Performance (Week)'},
                           'Max Shares Outstanding':{'$max':'$Shares Outstanding'},
                           'Total Volume':{'$sum':'$Volume'} } }
  query = [stage_one,stage_two,stage_three] #formlates query
  result=collection.aggregate(query) #performs aggregation
  result = dumps(result)
  return result
  
if __name__ == '__main__':
  run(debug=True,reloader = True)
  #run(host='localhost', port=8080)