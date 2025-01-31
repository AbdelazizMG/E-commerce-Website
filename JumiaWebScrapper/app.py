from flask import Flask, request, jsonify
from JumiaPageObjectModel import JumiaPageObjectModel

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Initialize the scraper
    scraper = JumiaPageObjectModel()
    scraper.landfirstpage()
    scraper.search(query)
    time.sleep(3)  # Wait for the page to load

    # Scrape data
    names = scraper.scrapProductsName()
    prices = scraper.scrapProductsPrice()
    images = scraper.scrapProductsImage()

    # Prepare response
    products = []
    for index in range(len(names)):
        product = {
            "name": names[index],
            "price": prices[index],
            "image": images[index],
            "category": "Electronics"
        }
        products.append(product)

    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)