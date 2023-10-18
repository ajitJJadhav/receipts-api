
# Information
Django (using django-rest-framework) was used to complete the task. Dockerfile was created for the project. The project can be run locally using the docker image on the 8000 port.

# Steps for running the project

## Clone the github repository
```
git clone https://github.com/ajitJJadhav/receipts-api.git
```


## Change the directory to the project directory
```
cd receipts-api
```

## Build the Docker image
```
docker build -t receipts-api-app .
```

## Run the Docker container
```
docker run -p 8000:8000 receipts-api-app
```

After running these commands, both the get and post apis can be tested.

# Sample test case for the apis

## POST api

API Details:

* Path: `/receipts/process`
* Method: `POST`
* Payload: Receipt JSON
* Response: JSON containing an id for the receipt.

Example receipt information:
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```

Command to test the example receipt:

```
curl --location 'http://127.0.0.1:8000/receipts/process' \
--header 'Content-Type: application/json' \
--data '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
```

Example Response:
```json
{
    "id": 1
}
```

## Get api

After running the above post request, we will have one entry for the receipt with id 1 for which we can calculate the score using the get api shown below.

API Details:
* Path: `/receipts/{id}/points`
* Method: `GET`
* Response: A JSON object containing the number of points awarded.

Command to test for receipt id 1:

```
curl --location 'http://127.0.0.1:8000/receipts/1/points'
```

Example Response:
```json
{"points": 28}
```
