# Crypto Price API

Simple REST API for fetching and storing cryptocurrency prices from KuCoin.

## Quick Start

1. Install & Setup:
```bash
git clone https://github.com/komabaa/crypto_api.git
cd crypto_api
pip install -e .

# Create database
sudo -u postgres psql
CREATE DATABASE crypto_db;
\q

# Configure database in .env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/crypto_db
```

2. Run:
```bash

gunicorn crypto_api.app:app --config gunicorn.conf.py
```

## API Routes

```bash
# Get current price
GET /price/BTC
GET /price/ETH

# Get price history (paginated, 10 per page)
GET /price/history?page=1

# Delete all history
DELETE /price/history
```

Example:
```bash
curl http://localhost:8080/price/BTC
```

## API Endpoints

### Get Current Price
```bash
GET /price/{currency}
```
Fetches current price for the specified currency from KuCoin and saves it to database.

Example:
```bash
curl http://localhost:8080/price/BTC
```

Response:
```json
{
    "currency": "BTC",
    "price": 65000.00,
    "timestamp": "2024-03-06T14:30:00"
}
```

### Get Price History
```bash
GET /price/history?page={page_number}
```
Returns paginated price history (10 items per page).

Example:
```bash
curl http://localhost:8080/price/history?page=1
```

Response:
```json
[
    {
        "id": 1,
        "currency": "BTC",
        "price": "65000.00",
        "date": "2024-03-06T14:30:00"
    }
]
```

### Delete Price History
```bash
DELETE /price/history
```
Deletes all price history records.

Example:
```bash
curl -X DELETE http://localhost:8080/price/history
```

## Error Handling

- Invalid currency: Returns 400 status code
- Currency not found: Returns 400 status code
- Database errors: Returns 400 status code with error message

## Project Structure
```
crypto_api/
├── app.py              # Main application file
├── config.py          # Configuration handling
├── .env              # Environment variables
├── gunicorn.conf.py  # Gunicorn configuration
├── controllers/
│   └── price_controller.py  # API endpoint handlers
├── models/
│   └── currency.py    # Database models
└── middleware/
    └── error_handling.py    # Error handling middleware
```

## Configuration

### gunicorn.conf.py
```python
bind = "0.0.0.0:8080"
workers = 4
worker_class = "aiohttp.worker.GunicornWebWorker"
```


