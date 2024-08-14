# Spaarks Backend API


This project provides a backend API for managing restaurant data, including querying based on geolocation. The API is built using FastAPI and MongoDB and is containerized using Docker.


## Prerequisites


Before running the project, ensure you have the following installed on your machine:


- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)

- **Docker Compose** (Optional, if using Docker Compose): [Installation Guide](https://docs.docker.com/compose/install/)


## Running the Application


### Step 1: Pull the Docker Image


Pull the pre-built Docker image from Docker Hub:


```bash

docker pull exypnos2k3/spaarks-backend

```


### Step 2: Run the Docker Container


To run the Docker container, use the following command:


```bash

docker run -p 8000:8000 exypnos2k3/spaarks-backend

```


This command maps port `8000` on your local machine to port `8000` on the container, making the FastAPI application accessible at `http://localhost:8000`.


### Step 3: Access the API Documentation


FastAPI provides interactive API documentation that you can access in your web browser:


- **Swagger UI**: `http://localhost:8000/docs`

- **ReDoc**: `http://localhost:8000/redoc`


## Authentication


The API is secured with JWT-based authentication. To interact with the API, you first need to obtain an authentication token.


### Step 1: Obtain a JWT Token


Send a `POST` request to the `/token` endpoint with the default credentials:


- **Username**: `root`

- **Password**: `root`


Here’s how you can obtain the token using `curl`:


```bash

curl -X POST "http://localhost:8000/token" -d "username=root&password=root"

```


Or, using Postman:


1. Set the request method to `POST`.

2. Set the request URL to `http://localhost:8000/token`.

3. In the `Body` tab, select `x-www-form-urlencoded` and add the following key-value pairs:

   - `username`: `root`

   - `password`: `root`

4. Send the request.


The response will contain a JSON object with the `access_token`:


```json

{

  "access_token": "your_generated_token",

  "token_type": "bearer"

}

```


### Step 2: Use the JWT Token in API Requests


Once you have the `access_token`, include it in the `Authorization` header of your requests as a Bearer token.


For example, in `curl`:


```bash

curl -X GET "http://localhost:8000/restaurants/?lat=40.7128&lon=-74.0060&radius=500" \

-H "Authorization: Bearer your_generated_token"

```


Or, in Postman:


1. Set the request method to `GET`.

2. Set the request URL (e.g., `http://localhost:8000/restaurants/?lat=40.7128&lon=-74.0060&radius=500`).

3. Go to the `Authorization` tab.

4. Select `Bearer Token` as the type.

5. Paste the `access_token` into the token field.

6. Send the request.


## API Endpoints


### 1. Get Restaurants by Radius


Retrieve restaurants within a specified radius from a given latitude and longitude.


- **Endpoint**: `/restaurants/`

- **Method**: `GET`

- **Parameters**:

  - `lat`: Latitude of the center point (e.g., `40.7128`).

  - `lon`: Longitude of the center point (e.g., `-74.0060`).

  - `radius`: Search radius in meters (e.g., `500`).



**Example Request**:


```bash

curl -X GET "http://localhost:8000/restaurants/?lat=40.7128&lon=-74.0060&radius=500" \

-H "Authorization: Bearer your_generated_token"

```


### 2. Get Restaurants by Distance Range


Retrieve restaurants within a specified distance range from a given latitude and longitude.


- **Endpoint**: `/restaurants/range/`

- **Method**: `GET`

- **Parameters**:

  - `lat`: Latitude of the center point (e.g., `40.7128`).

  - `lon`: Longitude of the center point (e.g., `-74.0060`).

  - `min_distance`: Minimum distance from the center point in meters (e.g., `500`).

  - `max_distance`: Maximum distance from the center point in meters (e.g., `2000`).


**Example Request**:


```bash

curl -X GET "http://localhost:8000/restaurants/range/?lat=40.7128&lon=-74.0060&min_distance=500&max_distance=2000" \

-H "Authorization: Bearer your_generated_token"

```


## Testing the API


You can use tools like `curl`, Postman, or any HTTP client to interact with the API. Make sure to include the JWT token in the `Authorization` header when testing the secured endpoints.


## Customization and Development


If you want to customize or further develop the application:


1. Clone the GitHub repository:


   ```bash

   git clone https://github.com/Darkdriller/spaarks-backend.git

   ```


2. Navigate to the project directory:


   ```bash

   cd spaarks-backend

   ```


3. Build the Docker image:


   ```bash

   docker build -t your-dockerhub-username/spaarks-backend .

   ```


4. Run the container:


   ```bash

   docker run -p 8000:8000 your-dockerhub-username/spaarks-backend

   ```


## Troubleshooting


- **Cannot access the API**: Ensure Docker is running and the container is started on port 8000.

- **Authentication issues**: Verify that the JWT token is correctly included in the `Authorization` header.



