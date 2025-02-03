from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json
from typing import Optional, List, Dict, Any
import logging

load_dotenv(find_dotenv())

db_password =os.environ.get("MONGODB_PASSWORD") 

connection_string = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
dbs = client.list_database_names()
# print(dbs)
e_commerce_dbs = client.e_commerce
products_collection = e_commerce_dbs.products_collection
# collections = e_commerce_dbs.list_collection_names()
# print(collections)

printer  = pprint.PrettyPrinter()

class MongoDBHandler:
    def __init__(self, connection_string: str, database_name: str):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection URL
            database_name: Name of the database to use
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    # Function to insert json file into products collection
    def insert_from_json(self, collection_name: str, json_file_path: str, batch_size: int = 100) -> Dict[str, Any]:
        """
        Insert documents from a JSON file into MongoDB collection
        
        Args:
            collection_name: Name of the collection to insert into
            json_file_path: Path to the JSON file containing documents
            batch_size: Number of documents to insert in each batch
            
        Returns:
            Dictionary containing insertion results
        """
        try:
            # Get collection
            collection = self.db[collection_name]
            
            # Initialize counters
            total_documents = 0
            inserted_documents = 0
            failed_documents = 0
            
            # Read JSON file
            self.logger.info(f"Reading JSON file: {json_file_path}")
            with open(json_file_path, 'r', encoding='utf-8') as file:
                documents = json.load(file)
                
            # Ensure documents is a list
            if not isinstance(documents, list):
                documents = [documents]
                
            total_documents = len(documents)
            
            # Process in batches
            for i in range(0, total_documents, batch_size):
                batch = documents[i:i + batch_size]
                try:
                    # Insert batch
                    result = collection.insert_many(batch, ordered=False)
                    inserted_documents += len(result.inserted_ids)
                    
                    # Log progress
                    self.logger.info(f"Progress: {inserted_documents}/{total_documents} documents processed")
                    
                except Exception as e:
                    failed_documents += len(batch)
                    self.logger.error(f"Error inserting batch: {str(e)}")
            
            # Prepare result summary
            result = {
                "total_documents": total_documents,
                "inserted_documents": inserted_documents,
                "failed_documents": failed_documents,
                "success_rate": round((inserted_documents / total_documents) * 100, 2) if total_documents > 0 else 0
            }
            
            self.logger.info("Insertion complete!")
            self.logger.info(f"Results: {json.dumps(result, indent=2)}")
            
            return result
            
        except FileNotFoundError:
            self.logger.error(f"JSON file not found: {json_file_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON format in file: {json_file_path}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise
        finally:
            self.client.close()
     
    
    # function to create a validation scheme for collection        
    def create_products_collection(self, collection_name: str):
        products_validator = {
            "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["description", "price", "image", "category", "rating", "units_available", "Offers"],
                    "properties": {
                        "description": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                        },
                        "price": {
                            "bsonType": "int",
                            "minimum": 0,
                            "description": "must be an integer greater than 0 and is required"
                        },
                        "image": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                        },
                        "category": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        },
                        "rating": {
                            "bsonType": "int",
                            "minimum": 0,
                            "maximum": 5,
                            "description": "must be a double greater than 0 and less than 5 and is required"
                        },
                        "units_available": {
                            "bsonType": "int" ,
                            "minimum": 0,
                            "description": " must be an integer greater than 0 and is required" 
                        },
                        # "Shipping_date": {
                        #     "bsonType": "date",
                        #     "description": "must be a date and is required"
                        # },
                        "Offers": {
                            "bsonType": "bool",
                            "description": "must be a bool and is required"
                        }
                        
                }
            }
        }

        # # Get collection
        # collection = self.db[collection_name]
        try:
            self.db.create_collection(collection_name)
            # collection = self.db[collection_name]
        except Exception as e:
            print(e)
        self.db.command("collMod", collection_name, validator=products_validator)



    def get_price_range(self, input_data, min_price=0, max_price=500000):
        """
        Filter products by price range. Works with both MongoDB collections and cursor results.
        
        Args:
            input_data: Either a collection name (str) or a MongoDB cursor from previous query
            min_price: Minimum price (default: 0)
            max_price: Maximum price (default: 500000)
        """
        price_query = {"$and": [
            {"price": {"$gte": min_price}},
            {"price": {"$lte": max_price}}
        ]}
        
        # If input_data is a string, treat it as collection name
        if isinstance(input_data, str):
            products_collection = self.db[input_data]
            products = products_collection.find(price_query, {
                "_id": 0,
                "description": 1,
                "price": 1,
                "image": 1,
                "rating": 1,
                "units_available": 1,
                "Offers": 1
            })
        
        # If input_data is a cursor (from previous query like search_products)
        else:
            # Convert cursor to list and filter in memory
            products = [
                product for product in input_data
                if min_price <= product.get('price', 0) <= max_price
            ]
        
        # Print results
        for product in products:
            printer.pprint(product)
        
        # Return the results for potential further processing
        return products

    def search_products(self, collection_name: str, search_term: str):
        """
        Search for products where the search term appears in the product name or any category.
        
        Args:
            collection_name: Name of the MongoDB collection
            search_term: Term to search for in product description or category
            
        Returns:
            MongoDB cursor containing the search results
        """
        # Case-insensitive regex pattern for partial matching
        search_regex = {"$regex": search_term, "$options": "i"}
        
        # Query to search in 'description' (product name) and inside the 'category' array
        query = {
            "$or": [
                {"description": search_regex},  # Match product name
                {"category": search_regex}  # Match any element inside the category array
            ]
        }
        
        # get collection name
        products_collection = self.db[collection_name]
        
        # Execute the search query
        results = products_collection.find(query, {
            "_id": 0,
            "description": 1,
            "price": 1,
            "image": 1,
            "rating": 1,
            "units_available": 1,
            "Offers": 1
        })

        # Optional: Print results for debugging/monitoring
        for product in results:
            printer.pprint(product)

        # Return the cursor for further processing
        return results
    
    # function to get rating
    def get_rting_range(self, input_data, min_rating=0, max_rating=5):
        """
        Filter products by price range. Works with both MongoDB collections and cursor results.
        
        Args:
            input_data: Either a collection name (str) or a MongoDB cursor from previous query
            min_price: Minimum price (default: 0)
            max_price: Maximum price (default: 500000)
        """
        rating_query = {"$and": [
            {"price": {"$gte": min_rating}},
            {"price": {"$lte": max_rating}}
        ]}
        
        # If input_data is a string, treat it as collection name
        if isinstance(input_data, str):
            products_collection = self.db[input_data]
            products = products_collection.find(rating_query, {
                "_id": 0,
                "description": 1,
                "price": 1,
                "image": 1,
                "rating": 1,
                "units_available": 1,
                "Offers": 1
            })
        
        # If input_data is a cursor (from previous query like search_products)
        else:
            # Convert cursor to list and filter in memory
            products = [
                product for product in input_data
                if min_rating <= product.get('price', 0) <= max_rating
            ]
        
        # Print results
        for product in products:
            printer.pprint(product)
        
        # Return the results for potential further processing
        return products


    def remove_data(self, collection_name: str):
        
        # Get collection
        collection = self.db[collection_name]
        collection.delete_many({})
        
    


# Example usage
if __name__ == "__main__":
    # MongoDB connection details
    MONGO_CONNECTION_STRING = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME = "e_commerce"
    COLLECTION_NAME = "products_collection"
    JSON_FILE_PATH = "data_16.json"
    
    mongo_handler = MongoDBHandler(MONGO_CONNECTION_STRING, DATABASE_NAME)
    # mongo_handler.search_products(collection_name=COLLECTION_NAME,search_term="smartphones")
    # mongo_handler.create_products_collection(collection_name=COLLECTION_NAME)
    #mongo_handler.remove_data(COLLECTION_NAME)
    # Search for products and then filter by price
    # search_results = mongo_handler.search_products(COLLECTION_NAME, "XIAOMI")
    # filtered_results = mongo_handler.get_price_range(search_results, 1000, 7000)
    # for product in filtered_results:
    #     printer.pprint(product)
    
    # Delete all documents where category contains "Smartphones"
    # delete_result = products_collection.delete_many({"category": "Cases"})

    # print(f"Deleted {delete_result.deleted_count} documents.")

    # # Or do everything in one line
    # filtered_results = mongo_handler.get_price_range(db.search_products("products", "laptop"), 10, 100)