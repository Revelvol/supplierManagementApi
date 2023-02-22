# Supplier Management API

This API provides functionality for managing suppliers, supplier contacts, ingredients, and associated functions. The API is designed to allow users to upload necessary documents for ingredients and suppliers, and to manage their information and relationships in a centralized and organized manner.

![image](https://user-images.githubusercontent.com/111274957/220533050-6b6a341f-781d-4d39-9a6d-de8694c4aecf.png)

## Features
- Manage suppliers and supplier contacts
- Manage ingredients and their associated documents
- Upload and manage documents for suppliers and ingredients
- Centralized and organized management of supplier and ingredient information

## API Documentation
API documentation is available on the Swagger UI, which can be accessed by visiting the API endpoint and navigating to the Swagger UI page. The Swagger UI provides a comprehensive and interactive documentation of the API endpoints and their functionality.

## Getting Started
To start using the Supplier Management API, follow the steps below:

1. Register an account on the API.
2. Obtain an API key.
3. Use the API key to obtain a Django Token Authentication token.
4. Use the Django Token Authentication token in the header of subsequent requests to the API.
5. Use the API endpoints to manage suppliers, supplier contacts, ingredients, and associated functions as desired.

## Endpoints
The following endpoints are available for use in the Supplier Management API:
![image](https://user-images.githubusercontent.com/111274957/220532891-24f6d30a-eed4-437b-8b89-dad6115c973a.png)
- `/api/suppliers` - Manage suppliers
- `/api/pic's` - Manage supplier contacts
- `/api/ingredients` - Manage Ingredients
- `/api/units` - Manage Ingredient Units 
- `/api/function` - Manage Ingredient Function 
- `/api/user` - Manage user
- `/api/suppliers/{id}/upload-documents` - Upload supplier document to the suplier.id
- `/api/ingredients/{id}/upload-documents` - Upload ingredients document to the ingredient.id


Filtering could also be conducted based on the query parameters:
1. filter ingredient based on supplier id, function id
2. filter pic based on supplier id 
3. filter pic if they have supplier assigned or not 
4. filter ingredient if they have supplier and/or function or not 

## Request & Response Formats
The API uses standard HTTP request and response formats. Requests and responses are in JSON format.

## Authentication
The API uses Django Token Authentication for authentication. To access the write API, a Django Token Authentication token must be included in the header of each request.
Any request are valid for read request 

## Error Handling
In the event of an error, the API will return an error response in the json format: 

