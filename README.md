# E-Commerce Website with ChatBot

This repository contains a fully functional e-commerce website developed using Vue.js for the frontend, Django for the backend, and MongoDB as the database. The website features a chatbot that allows users to interact with the platform using English statements to search for products.

## Features

- **Vue.js Frontend**: A simple, responsive UI for seamless user experience.
- **Django Backend**:  API endpoints, and business logic.
- **MongoDB Database**: Stores products information
- **ChatBot Integration**: Users can search for products by typing natural language queries.
- **Search Functionality**: Find products through both chatbot queries and a traditional search bar.
- **API**: Enables communication between frontend and backend.

## Technologies Used

- **Frontend**: Vue.js
- **Backend**: Django
- **Database**: MongoDB
- **ChatBot**: NLP-based interaction for product search
- **Deployment**: TBD (Cloud platforms such as AWS, GCP, or Azure)

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Node.js & npm
- Python 3.x & pip
- MongoDB

### Backend Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/AbdelazizMG/E-commerce-Website
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the Django server:
   ```sh
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the Vue.js development server:
   ```sh
   npm run dev
   ```


## Usage
- Open the frontend at `http://localhost:5173/`.
- Use the search bar or chatbot to find products.
- Chatbot understands queries like:
  - "Hi there, i want to buy a nice phone with less than 10000 LE. can you suggest a one?"
  - "Please find me a shirt that its cost doesn't exceed 500."
  - "I would like to buy a novel that costs less than 100"
- The chatbot will return relevant product results.

## Future Enhancements
- User authentication and profiles
- Order management system
- Recommendation engine for personalized shopping


## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For any inquiries, feel free to open an issue

 
