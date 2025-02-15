from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor
import gc
from typing import Dict, Union

class JumiaPageObjectModel:
    def __init__(self):
        # Enhanced Chrome options for better performance
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        self.chrome_options.add_argument("--disable-extensions")  # Disable extensions
        self.chrome_options.add_argument("--disable-software-rasterizer")
        
        # Initialize WebDriver with options
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Initialize data storage with batch processing
        self.data = []
        self.batch_size = 50  # Process data in batches
        self.current_batch = []

    def save_batch(self):
        """Save current batch and clear memory"""
        if self.current_batch:
            self.data.extend(self.current_batch)
            with open("data_36.json", "w", encoding='utf-8') as json_file:
                json.dump(self.data, json_file, indent=4, ensure_ascii=False)
            self.current_batch = []
            gc.collect()  # Force garbage collection

    def process_product(self, product) :
        """Process a single product with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Extract Name with wait
                name_element = WebDriverWait(product, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//h3[@class='name']"))
                )
                name = name_element.text.strip()

                # Extract Price with wait
                price_element = WebDriverWait(product, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@class='prc']"))
                )
                price_text = price_element.text.strip()
                price_numbers = re.sub(r"[^\d.]", "", price_text)
                price = int(float(price_numbers)) if price_numbers else None

                # Extract Image with wait
                image_element = WebDriverWait(product, 3).until(
                    EC.presence_of_element_located((By.XPATH, ".//img[@class='img']"))
                )
                image_url = image_element.get_attribute("data-src") or image_element.get_attribute("src")
                
                try:
                    # Find rating element with the specific class
                    rating_element = product.find_element(By.XPATH, ".//div[contains(@class, 'stars _s')]")
                    rating_text = rating_element.text.strip()  # Will get "4.3 out of 5" format
                    
                    # Extract the rating and ensure it's a float
                    rating_match = re.search(r"(\d+\.?\d*)", rating_text)
                    if rating_match:
                        # Convert to float and round to 1 decimal place for consistency
                        rating = round(int(rating_match.group(1)), 1)
                    else:
                        rating = 0  # Default value as float
                except NoSuchElementException:
                    rating = 0  # Default value as float
                except (ValueError, AttributeError):
                    # Handle any conversion errors
                    rating = 0  # Default value as float
                    
                return {
                    "description": name,
                    "price": price,
                    "image": image_url,
                    "category": ["Computing", "Computers & Accessories", "Desktops & Laptops"],
                    "rating": rating,  # Now returns integer 0-100
                    "units_available": 0,
                    "Offers": False
                }

            except (StaleElementReferenceException, TimeoutException):
                if attempt == max_retries - 1:
                    return None
                time.sleep(1)
            except Exception:
                return None
        return None

    def land_first_page(self):
        """Land on first page with improved error handling"""
        try:
            self.driver.get("https://www.jumia.com.eg/computers-tablets/")
            
            # Handle popup more efficiently
            try:
                close_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='cls']"))
                )
                close_button.click()
            except TimeoutException:
                pass  # Skip if no popup

            # Verify page loaded successfully
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article[not(@data-tst='prod')]"))
            )
        except Exception as e:
            print(f"Error landing on first page: {str(e)}")
            return None

    def scrape_products(self):
        """Scrape products with improved memory management"""
        try:
            # Get products with wait
            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//article[not(@data-tst='prod')]"))
            )

            # Process products in parallel
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(self.process_product, products))

            # Filter out None results and add to batch
            valid_results = [r for r in results if r is not None]
            self.current_batch.extend(valid_results)

            # Save batch if size threshold reached
            if len(self.current_batch) >= self.batch_size:
                self.save_batch()

        except Exception as e:
            print(f"Error scraping products: {str(e)}")
            self.save_batch()  # Save current batch in case of error

    def get_next_page(self):
        """Get next page with improved reliability"""
        try:
            next_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next Page']"))
            )
            
            # Scroll into view with JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)  # Short pause for stability
            
            # Click with JavaScript instead of ActionChains
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(1)  # Wait for page load
            
            return True
        except Exception:
            return False

    def scrape_all_pages(self, max_pages=None):
        """Scrape all pages with page limit option"""
        page_count = 0
        
        while True:
            page_count += 1
            print(f"Scraping page {page_count}...")
            
            self.scrape_products()
            
            if max_pages and page_count >= max_pages:
                break
                
            if not self.get_next_page():
                break
        
        # Save any remaining items in the final batch
        self.save_batch()

    def close_browser(self):
        """Clean up resources"""
        try:
            self.driver.quit()
        except Exception:
            pass
        gc.collect()

if __name__ == "__main__":
    scraper = JumiaPageObjectModel()
    try:
        if scraper.land_first_page():
            scraper.scrape_all_pages(max_pages=50)  # Limit to 10 pages for testing
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        scraper.close_browser()
