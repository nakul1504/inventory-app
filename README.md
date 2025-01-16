# Inventory App

An Inventory Management Application built with **Django** and **MongoDB Cloud** to manage products, suppliers, stock movements, and sales orders efficiently. The project follows an intuitive and user-friendly UI powered by Bootstrap.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Key Functionalities](#key-functionalities)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)

---

## Features
- **Products Management:** Add and view products.
- **Supplier Management:** Add and view suppliers.
- **Stock Movement:** Handle stock movements (incoming and outgoing).
- **Sales Orders:** Create, complete, or cancel sales orders with automatic stock level updates.
- **MongoDB Integration:** Cloud-based NoSQL database for scalability and performance.
- **Data Validation:** Form-level validation for all inputs (e.g., email format, stock levels).
- **Bootstrap UI:** Responsive and user-friendly web interface.
- **Environment Configuration:** Secure connection to MongoDB Cloud using `.env`.

---

## Installation

### Prerequisites
1. **Python 3.10+**
2. **pipenv** (or use virtualenv)
3. **MongoDB Cloud**

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/nakul1504/inventory-app.git
   cd inventory-app
   
2. Create and Activate Virtual Environment
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   
4. Running the Project Locally
    ```bash
    python manage.py runserver
   
---

## Environment Variables

Create a `.env` file in the root directory and add the following variables:

```dotenv
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_CLUSTER=your_cluster.mongodb.net
SECRET_KEY=your_django_secret_key
DEBUG=True
```

---

## Project Structure

### `inventory_management/`
Contains the main Django project configuration files.
- **`settings.py`**: Project settings, including database, middleware, and static files configurations.
- **`urls.py`**: Root URL routing for the project.
- **`wsgi.py`**: Configuration for WSGI (Web Server Gateway Interface).
- **`asgi.py`**: Configuration for ASGI (Asynchronous Server Gateway Interface).

### `inventory/`
The main app for managing inventory, products, suppliers, and sale orders.
- **`forms.py`**: Contains Django forms for input validation and dynamic field choices.
- **`views.py`**: Contains view logic to handle HTTP requests.
- **`models.py`**: Defines database models for products, suppliers, and related entities.
- **`urls.py`**: URL routing specific to the `inventory` app.
- **`templates/`**: Contains HTML templates for rendering views.

### `.env`
File to store environment-specific variables like database credentials and secret keys.

### `requirements.txt`
Lists all the Python dependencies required for the project.

### `manage.py`
Django CLI utility to manage the project (e.g., running the server, migrations).

### `README.md`
Project documentation, including setup instructions, features, and API details.

---

## Key Functionalities

### Products Management
- Add new products with details such as name, description, category, price, and stock quantity.
- View a list of all products in the inventory.
- Provided a filter by category for product list.
- Dynamically fetch supplier names for new product creation.

### Suppliers Management
- Add new suppliers with details like name, email, phone number, and address.
- View a list of all registered suppliers.

### Stock Management
- Record stock movements (incoming or outgoing).
- Automatically adjust stock levels based on sale orders and stock movements.

### Sale Orders
- Create sale orders with product details and quantity.
- View a list of all sale orders with their status (Pending, Completed, or Canceled).
- Provided a filter by order-status for all sale orders.
- Complete or cancel sale orders with appropriate stock adjustments.

### Data Validation
- Ensure input validation for email, phone numbers, stock levels, and other fields.
- Prevent actions like creating orders with insufficient stock.

### MongoDB Integration
- Utilize MongoDB Atlas for data storage and retrieval.
- Dynamically fetch data such as suppliers and products for dropdowns.

### User-Friendly Interface
- Responsive web pages designed with Bootstrap.
- Intuitive navigation and user-friendly templates for seamless interaction.

### Deployment-Ready
- Fully configured for deployment on platforms like Render or Railway.
- Environment-specific configurations managed through `.env` files.

---

## API Endpoints

### Products
- **List Products**: `/product-list/`  
  Retrieves a list of all products in the inventory.  

- **Create Product**: `/add-product/`  
  Endpoint to add a new product.



### Suppliers
- **List Suppliers**: `/suppliers/`  
  Retrieves a list of all suppliers.  

- **Create Supplier**: `/add-suppliers/`  
  Endpoint to add a new supplier.



### Stock Movements
- **Record Movement**: `/add-stock-movement/`  
  Endpoint to record stock adjustments (incoming or outgoing).

- **Stock Level Check**: `/stock-level-check/`
  Endpoint to check stock levels


### Sale Orders
- **List Orders**: `/sale-order-list/`  
  Retrieves a list of all sale orders.  

- **Create Order**: `/create-sale-order/`  
  Endpoint to create a new sale order.  

- **Complete Order**: `/complete-sale-order/<str:sale_order_id>/`  
  Marks a sale order as completed.  

- **Cancel Order**: `cancel-sale-order/<str:sale_order_id>/`  
  Marks a sale order as canceled.

---

## Deployment