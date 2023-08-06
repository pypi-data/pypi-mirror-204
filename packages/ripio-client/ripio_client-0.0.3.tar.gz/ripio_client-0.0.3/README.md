# Ripio Client for Python
###  ALPHA SOFTWARE


This is a lightweight library that works as a client to [Ripio](https://www.ripio.com) Services

## Installation
```bash
pip install ripio-client
```

## Usage example
```python
from ripio.trade.client import Client

# API key is required for user data endpoints
client = Client(api_key='<api_key>')

# Get balance information
print(client.balance())

# Create a market order
params = {
	'pair': 'BTC_USDC',
	'side': 'buy',
	'amount': 0.01,
	'type': 'market'
}
response = client.create_order(**params)
print(response)

# Create a limit buy order
params = {
	'pair': 'BTC_USDC',
	'side': 'buy',
	'amount': 0.0002,
	'type': 'limit',
	'price': 27471.65
}
response = client.create_order(**params)
print(response)

# Create a limit sell order
params = {
	'pair': 'BTC_USDC',
	'side': 'sell',
	'amount': 0.0002,
	'type': 'limit',
	'price': 27470
}
response = client.create_order(**params)
print(response)

```
