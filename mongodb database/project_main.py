from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json
from typing import Optional, List, Dict, Any
import logging
import random
from bson import ObjectId
import datetime


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
                            "bsonType": "double",
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


    def remove_data(self, collection_name: str):
        
        # Get collection
        collection = self.db[collection_name]
        collection.delete_many({})
        

    # Alternative method using bulk operations for better performance
    def remove_duplicates(self, collection_name: str, fields_to_check: List[str]):
        """
        Remove duplicate documents from a MongoDB collection based on specified fields.
        
        Args:
            collection_name: Name of the collection to deduplicate
            fields_to_check: List of field names to check for duplicates
            db: MongoDB database instance
        
        Returns:
            Dict containing the number of duplicates removed and status
        """
        try:
            # Create the aggregation pipeline
            pipeline = [
                # Group by the specified fields
                {
                    "$group": {
                        "_id": {field: f"${field}" for field in fields_to_check},
                        "unique_ids": {"$addToSet": "$_id"},
                        "count": {"$sum": 1}
                    }
                },
                # Filter only groups with more than one document (duplicates)
                {
                    "$match": {
                        "count": {"$gt": 1}
                    }
                }
            ]
            
            # Get the collection
            collection = self.db[collection_name]
            
            # Find all duplicate groups
            duplicate_groups = list(collection.aggregate(pipeline))
            
            total_removed = 0
            
            # Process each group of duplicates
            for group in duplicate_groups:
                # Sort unique_ids to consistently keep the first document
                document_ids = sorted(group['unique_ids'])
                
                # Keep the first document, remove the rest
                ids_to_remove = document_ids[1:]
                
                # Remove duplicate documents
                result = collection.delete_many({"_id": {"$in": ids_to_remove}})
                total_removed += result.deleted_count
                
            return {
                "success": True,
                "duplicates_removed": total_removed,
                "duplicate_groups_found": len(duplicate_groups)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

            
            

    def randomize_fields(self, collection_name: str) -> Dict[str, Any]:
        """
        Randomize rating, units_available, and offers fields for all documents.
        
        Args:
            collection_name: Name of the collection to update
        
        Returns:
            Dict containing the number of documents updated and status
        """
        try:
            collection = self.db[collection_name]
            documents = collection.find({})
            updated_count = 0
            
            
            for doc in documents:
                # Generate random values
                random_rating = round(random.uniform(0, 5), 1)  # Float between 0-5 with 1 decimal
                random_units = random.randint(0, 1000)  # Integer between 0-1000
                random_offers = random.choice([True, False])  # Boolean
               
                if doc.get("units_available") <= 0 :
                    # Update document
                    result = collection.update_one(
                        {"_id": doc["_id"]},
                        {
                            "$set": {
                                "rating": random_rating,
                                "units_available": random_units,
                                "Offers": random_offers
                            }
                        }
                    )
                    
                    if result.modified_count > 0:
                        updated_count += 1
            
            return {
                "success": True,
                "documents_updated": updated_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    

# Example usage
# if __name__ == "__main__":
#     # MongoDB connection details
#     MONGO_CONNECTION_STRING = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#     DATABASE_NAME = "e_commerce"
#     COLLECTION_NAME = "products_collection"
#     JSON_FILE_PATH = "data_36.json"
    
#     mongo_handler = MongoDBHandler(MONGO_CONNECTION_STRING, DATABASE_NAME)
#     # mongo_handler.search_products(collection_name=COLLECTION_NAME,search_term="smartphones")
    
#     # mongo_handler.create_products_collection(collection_name=COLLECTION_NAME)
    
#     #mongo_handler.remove_data(COLLECTION_NAME)
    
#     # Search for products and then filter by price
#     # search_results = mongo_handler.search_products(COLLECTION_NAME, "XIAOMI")
#     # filtered_results = mongo_handler.get_price_range(search_results, 1000, 7000)
#     # for product in filtered_results:
#     #     printer.pprint(product)
    
#     # Delete all documents where category contains "Smartphones"
#     # delete_result = products_collection.delete_many({"category": "Speakers"})

#     # print(f"Deleted {delete_result.deleted_count} documents.")

#     # # Or do everything in one line
#     # filtered_results = mongo_handler.get_price_range(db.search_products("products", "laptop"), 10, 100)
    

# # Remove duplicates based on email and name fields
#     # result = mongo_handler.remove_duplicates(
#     #     collection_name=COLLECTION_NAME,
#     #     fields_to_check=["description", "price", "image"],
#     # )

#     # print(f"Removed {result['duplicates_removed']} duplicate documents")

#     # print(result)
    
#     # Upload data from json file
    
#     # try:
#     #     # Initialize handler
#     #     # mongo_handler = MongoDBHandler(MONGO_CONNECTION_STRING, DATABASE_NAME)
        
#     #     # Insert documents
#     #     result = mongo_handler.insert_from_json(
#     #         collection_name=COLLECTION_NAME,
#     #         json_file_path=JSON_FILE_PATH,
#     #         batch_size=100
#     #     )
        
#     #     print(f"Insertion completed with {result['success_rate']}% success rate")
        
#     # except Exception as e:
#     #     print(f"Error: {str(e)}")
    
#     # rando,ize fields 
#     result = mongo_handler.randomize_fields(COLLECTION_NAME)
    
#     print(result)




class order_colletion_handler :
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
    # function to create a validation scheme for collection        
    def create_orders_collection(self, collection_name: str):
        products_validator = {
            "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["Products", "Address", "Mobile", "Cost", "Delivery_time", "Status"],
                    "properties": {
                        "Products": {
                            "bsonType": "object",
                            "reqired": ["product_id", "quantity"],
                            "properties": {
                                "product_id": {
                                    "bsonType": "objectId",
                                    "description": "must be an objectid and is required"
                                },
                                "quantity": {
                                    "bsonType": "int",
                                    "description": "must be an integer and is required"
                                }
                            }
                        },
                        "Address": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "Mobile": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                        },
                        "Cost": {
                            "bsonType": "int",
                            "description": "must be an integer and is required"
                            
                        },
                        "Delivery_time": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "Status": {
                            "enum": ["Preparing", "Prepared", "Shipping", "Shipped"] ,
                            "description": " can be only one of the enum valus and is required" 
                        }    
                }
            }
        }

        try:
            self.db.create_collection(collection_name)
        except Exception as e:
            print(e)
        self.db.command("collMod", collection_name, validator=products_validator)
    
    def create_order(self, collection_name: str, address: str, mobile: str, products_info: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create an order with the given products and customer information
        
        Args:
            collection_name: Name of the orders collection
            address: Customer's delivery address
            mobile: Customer's mobile number
            products_info: List of dictionaries containing product IDs and quantities
                        [{"product_id": "...", "quantity": 1}, ...]
        
        Returns:
            Dictionary containing order details or error information
        """
        try:
            orders_collection = self.db[collection_name]
            products_collection = self.db["products_collection"]
            total_cost = 0
            
            # Validate and process each product
            for product in products_info:
                # Convert string ID to ObjectId if needed
                if isinstance(product["product_id"], str):
                    product["product_id"] = ObjectId(product["product_id"])
                
                # Find product and check availability
                product_doc = products_collection.find_one({"_id": product["product_id"]})
                if not product_doc:
                    return {"success": False, "error": f"Product {product['product_id']} not found"}
                
                if product_doc["units_available"] < product["quantity"]:
                    return {
                        "success": False, 
                        "error": f"Insufficient stock for product {product_doc['description']}. Available: {product_doc['units_available']}"
                    }
                
                # Calculate cost
                total_cost += product_doc["price"] * product["quantity"]
                
                # Update product inventory
                result = products_collection.update_one(
                    {"_id": product["product_id"]},
                    {"$inc": {"units_available": -product["quantity"]}}
                )
                
                if result.modified_count != 1:
                    # Rollback previous inventory changes if this update fails
                    return {"success": False, "error": "Failed to update product inventory"}
            
            # Create order document
            order = {
                "Products": products_info,
                "Address": address,
                "Mobile": mobile,
                "Cost": total_cost,
                "Delivery_time": datetime.datetime.now() + datetime.timedelta(days=3),  # Delivery in 3 days
                "Status": "Preparing"
            }
            
            # Insert order
            result = orders_collection.insert_one(order)
            
            return {
                "success": True,
                "order_id": str(result.inserted_id),
                "status": "Preparing",
                "cost": total_cost,
                "delivery_time": order["Delivery_time"]	
            }
            
        except Exception as e:
            self.logger.error(f"Error creating order: {str(e)}")
            return {"success": False, "error": str(e)}
    
# Example usage
if __name__ == "__main__":
    MONGO_CONNECTION_STRING = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME = "e_commerce"
    COLLECTION_NAME = "orders_collection"

    # Initialize handler
    order_handler = order_colletion_handler(MONGO_CONNECTION_STRING, DATABASE_NAME)
    
    # Example order data
    address = "123 Main St, City"
    mobile = "+1234567890"
    products_to_order = [
        {"product_id": "679fd960d75ddf64947e771f", "quantity": 2},  # Replace with actual product ID
        {"product_id": "679fdc862187bc7fa03726a6", "quantity": 1}   # Replace with actual product ID
    ]
    
    # Create order
    result = order_handler.create_order("orders_collection", address, mobile, products_to_order)
    
    if result["success"]:
        print(f"Order created successfully!")
        print(f"Order ID: {result['order_id']}")
        print(f"Status: {result['status']}")
        print(f"Total Cost: ${result['cost']}")
    else:
        print(f"Error creating order: {result['error']}")