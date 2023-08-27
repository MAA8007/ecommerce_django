# Django E-commerce Project  

  ## Table of Contents  
  
  - [Overview](#overview) 
  - [Features](#features) 
  - [Technologies Used](#technologies-used) 
  - [Screenshots](#screenshots) 
  - [Installation & Setup](#installation--setup) 
  - [Usage](#usage) 
  - [Contributing](#contributing) 
  - [License](#license)

    
  ## Overview  
  
  This is a Django-based e-commerce platform designed to provide a seamless shopping experience. Users can browse products by various categories, add items to their cart, and proceed through an easy checkout process. The platform also includes user authentication features and an admin panel for simplified backend management.  

  
  ## Features  
  
  - **User Authentication**: Secure login and registration features. 
  - **Product Browsing**: Browse products by categories like Suits, Jeans, Shirts, etc. 
  - **Detailed Product View**: View detailed information about a product, including different sizes. 
  - **Shopping Cart**: Add and remove items to and from the cart. - **Checkout Process**: Fill in personal information and proceed to payment. 
  - **Admin Panel**: Secure and user-friendly admin panel for managing products and orders.    

  
  ## Technologies Used 
  
  - **Backend**: Django, Python 
  - **Frontend**: HTML, CSS, Bootstrap5
  - **Database**: SQLite

  
  ## Screenshots  
  
  ### Home Page <img width="1440" alt="Screenshot 2023-08-27 at 11 04 16 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/77b475c6-922b-411c-851a-f06116692ec0">
<img width="1440" alt="Screenshot 2023-08-27 at 11 04 29 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/11894e46-dd95-482c-9451-063d456e4bcb">
*Screenshots of Home Page showing various product categories.*  
  
  ### Product List<img width="1440" alt="Screenshot 2023-08-27 at 11 05 24 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/74d78e60-388b-44ac-ba7c-22789703af50">
 *List of all available products.*  

### Product Categories <img width="1440" alt="Screenshot 2023-08-27 at 11 05 37 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/de4037c0-f671-4ced-8b00-686e0376fbe8">
 *List of Products in that specific category* 
    
  ### Shopping Cart <img width="1440" alt="Screenshot 2023-08-27 at 11 09 17 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/51d5ac45-a6c2-4a84-b92c-2cc06376aa5d">
 *Shopping cart with items.*  

  ### Checkout Page <img width="1440" alt="Screenshot 2023-08-27 at 11 09 42 PM" src="https://github.com/MAA8007/ecommerce_django/assets/106858270/052dc644-0904-4fe1-a388-3b7a8ffbebad">
 *Checkout page with form validation.*  
 
  
  ## Installation & Setup  
  
  ### Clone the Repository  
  ```bash git clone https://github.com/yourusername/django-ecommerce.git ```  

  
  ### Install Dependencies  
  
  Activate your virtual environment and install the required packages.  
  ```bash pip install -r requirements.txt ```  

  
  ### Database Setup  
  
  Run the following commands to apply the database migrations.  
  ```bash python manage.py makemigrations python manage.py migrate ```  
  
  
  ### Create Superuser  
  Create a superuser to manage the backend.  
  ```bash python manage.py createsuperuser ```  
  
  
  ### Run Development Server  
  ```bash python manage.py runserver ``` 
   Navigate to `http://127.0.0.1:8000/` to view the application.  
   
   
   ## Usage  
   
   - **Home Page**: Browse different categories and featured products. 
   - **Product List**: View or filter products by category. 
   - **Product Detail**: Detailed view of each product, including size options. 
   - **Shopping Cart**: View cart items, update their quantity, or remove them. 
   - **Checkout**: Complete the order by filling in details and choosing a payment method.
   - 
   
   ## Contributing  Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  

   
   ## License  This project is licensed under the MIT License. 
