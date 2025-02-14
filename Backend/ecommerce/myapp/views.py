from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from bson import ObjectId
from .models import test_collection
import json, random
from query_translator import QueryTranslator

def home(request):
    pass

def add_person(request):
    record : dict = {
        'name' : 'zezo',
        'price' : 123
    }

    test_collection.insert_one(record)
    return HttpResponse(f"{record}")

def show_person(request):
    temp = test_collection.find({ "price": { "$lt": 500 } })
    # temp = test_collection.find({ "price": { "$eq": 150 } })
    # temp = test_collection.find({ "price": { "$ne": 150 } })
    # temp = test_collection.find({ "price": { "$lte": 150 } })
    # temp = test_collection.find({ "price": { "$gt": 150 } })
    # temp = test_collection.find({ "price": { "$gte": 150 } })
    # temp = test_collection.find({ "price": { "$in": [100, 150, 200] } })
    # temp = test_collection.find({ "price": { "$nin": [100, 150] } })
    return HttpResponse(temp)

# Create your views here.
def Homepage(request)  -> JsonResponse:
    '''
    Function to search for 20 random products at the homepage of the website
    '''
    if request.method == "GET":
        try:
            # Return Filtered products based on search
           #temp = random.sample(list(test_collection.find()), 20)
            temp = list(test_collection.aggregate([{"$sample": {"size": 50}}]))


            # Convert ObjectIds to strings (important!)
            results = []
            for item in temp:
                item_dict = {}  # Create a dictionary for each item
                for key, value in item.items():
                    if isinstance(value, ObjectId):  # Check if value is an ObjectId
                        item_dict[key] = str(value)   # Convert ObjectId to string
                    else:
                        item_dict[key] = value
                results.append(item_dict)

            print(results)
            return JsonResponse(results, safe=False) # safe=False because you're serializing a list 
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def AIsearch_view(request) -> JsonResponse:
    '''
    Function to search using the PROMPT 
    '''
    if request.method == "GET":
        try:
            #data = json.loads(request.body.decode("utf-8"))  # Read and decode JSON
            #query = data.get("query", "")  # Extract query parameter
            query = request.GET.get("query", "")

            if not query:
                return JsonResponse({"error": "Query parameter is missing"}, status=400)

            print("User searched for:", query)  # Debugging output

            # Return Filtered products based on search
            #temp = list(test_collection.find({ "price": { "$lt": int(query) } }))
            QueryTranslator_obj = QueryTranslator()
            QueryTranslator_obj.test_connection()
            query = QueryTranslator_obj.execute_query(query)
            query_json = json.loads(query)
            print(query_json)
            print('##############################################')
            #temp = list(test_collection.find({ "description": { "$regex": query, "$options": "i" } }))
            temp = test_collection.find(query_json)

            # Convert ObjectIds to strings (important!)
            results = []
            for item in temp:
                item_dict = {}  # Create a dictionary for each item
                for key, value in item.items():
                    if isinstance(value, ObjectId):  # Check if value is an ObjectId
                        item_dict[key] = str(value)   # Convert ObjectId to string
                    else:
                        item_dict[key] = value
                results.append(item_dict)

            return JsonResponse(results, safe=False) # safe=False because you're serializing a list        
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def Normalsearch_view(request) -> JsonResponse:
    '''
    Function to search using the search bar
    '''
    if request.method == "GET":
        try:
            query = request.GET.get("query", "")

            if not query:
                return JsonResponse({"error": "Query parameter is missing"}, status=400)

            print("User searched for:", query, type(query))  # Debugging output

            # Return Filtered products based on search
            #temp = list(test_collection.find({ "price": { "$lt": int(query) } }))
            #temp = list(test_collection.find())
            temp = list(test_collection.find(
                {
                "$or": [
                            { "description": { "$regex": query, "$options": "i" } },
                            {"category": { "$regex": query, "$options": "i" }}
                       ]
                }
            )
            )

            #print(temp)

            # Convert ObjectIds to strings (important!)
            results = []
            for item in temp:
                item_dict = {}  # Create a dictionary for each item
                for key, value in item.items():
                    if isinstance(value, ObjectId):  # Check if value is an ObjectId
                        item_dict[key] = str(value)   # Convert ObjectId to string
                    else:
                        item_dict[key] = value
                results.append(item_dict)

            print(results)
            return JsonResponse(results, safe=False) # safe=False because you're serializing a list 
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
def Categorysearch_view(request) -> JsonResponse:
    '''
    Function to search using the search bar
    '''
    if request.method == "GET":
        try:
            query = request.GET.get("query", "")

            if not query:
                return JsonResponse({"error": "Query parameter is missing"}, status=400)

            print("User searched for:", query, type(query))  # Debugging output

            # Return Filtered products based on search
            temp = list(test_collection.find({ "category": { "$regex": query, "$options": "i" } }))

            #print(temp)
            # Convert ObjectIds to strings (important!)
            results = []
            for item in temp:
                item_dict = {}  # Create a dictionary for each item
                for key, value in item.items():
                    if isinstance(value, ObjectId):  # Check if value is an ObjectId
                        item_dict[key] = str(value)   # Convert ObjectId to string
                    else:
                        item_dict[key] = value
                results.append(item_dict)

            print(results)
            return JsonResponse(results, safe=False) # safe=False because you're serializing a list 
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)    