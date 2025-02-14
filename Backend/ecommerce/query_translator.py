# query_translator.py
import os, json,re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import login
from requests.exceptions import Timeout
#login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))  # Authenticate

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN") 

class QueryTranslator:
    def __init__(self):
        self.llm = self._initialize_llm()
        self.chain = self._create_chain()
        
    def _initialize_llm(self):
        """Initialize free google/flan-t5-largemodel via Hugging Face Hub"""
        return HuggingFaceHub(
            #repo_id="google/flan-t5-large",
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            model_kwargs={
                "temperature": 0.1,
                "max_new_tokens": 150,
                "top_p": 0.95
            }
        )

    def _create_chain(self):
        """Create LangChain conversion pipeline"""
        template = """<s>[INST] Convert this product query to MongoDB JSON. Use ONLY these fields: {fields}.
        Rules:
        1. Use $lt/$gt for numeric comparisons
        2. Use $regex with $options:"i" for text
        3. Return ONLY valid MongodB query in your response without any extra English explanations after the JSON.
        
        Example Input: "Gaming laptops under 30000 L.E"
        Output: {{"description": {{"$regex": "laptop"}}, "price": {{"$lt": 30000}}}}
        
        Input: {query} [/INST]</s>"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query", "fields"],
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)

    @lru_cache(maxsize=128)
    def _generate_mongo_query(self, query: str) -> dict:
        """Convert natural language to MongoDB query with caching"""
        try:
            #response = self.chain.run(query=query)
            response = self.chain.invoke(
                {"query": query, "fields": {"price","description"}},
                config={"timeout": 15}
                )
            
            # Extract JSON from model response
            #json_match = re.search(r'{.*?}', response, re.DOTALL)
            #print("====================================")
            #print(f"response: {response['text']}")
            #print("====================================")
            json_str = response["text"]
            json_match = re.findall(r'<\/s>({.+})', json_str, re.DOTALL)[0]
            #print(f"json_match: {json_match}")        
            if not json_match:
                raise ValueError("No JSON found in model response")
                
            #query_str = json_match.group()
            #query_dict = json.loads(query_str.replace("'", '"'))
            
            return json_match
        except Timeout:
            raise RuntimeError("Hugging Face API timeout")
        except Exception as e:
            raise RuntimeError(f"Query generation failed: {str(e)}")

    def _validate_query(self, query: dict):
        """Security validation for MongoDB query"""
        # Check allowed fields
        # Validate price ranges
        if "price" in query:
            price_query = query["price"]
            for op, value in price_query.items():
                if op not in ["$lt", "$gt"]:
                    raise ValueError(f"Invalid price operator: {op}")

    def execute_query(self, english_query: str) -> list:
        """Main function: Input English, output MongoDB results"""
        try:
            # Generate and validate query
            print(english_query)
            mongo_query = self._generate_mongo_query(english_query.strip().lower())
            print(mongo_query)
            #self._validate_query(mongo_query)
            
            # Execute query
           # db = self.mongo_client[CONFIG["db_name"]]
            #collection = db[CONFIG["collection"]]
            
            return mongo_query
            
        except Exception as e:
            return {"error": str(e)}
        
    def test_connection(self):
        try:
            test_response = self.llm.generate(["ping"])
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
        

# Usage Example
if __name__ == "__main__":
    translator = QueryTranslator()
    
    connection = translator.test_connection()
    if connection:
        print("Connection test passed")
    else:
        print("Connection test failed")
    # Test query
    #test_query = "Gaming laptops under 30000 L.E with Dell brand"
    #test_query = "Samsung Laptop above 20000 L.E"
    test_query = "a balck t-shirt with price less than 200"
    results = translator.execute_query(test_query)
    
    print(f"Generated Query Result: {results}")
   # print(json.dumps(results[:2], indent=2))  # Print first 2 results