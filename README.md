# Flight Aggregator

A Python application to search and compare flight information using the Amadeus API.

## Setup

1. **Get Amadeus API Credentials**
   - Visit [Amadeus for Developers](https://developers.amadeus.com/)
   - Create a free account
   - Go to your workspace and get your API Key and API Secret

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your Amadeus API credentials:
   ```
   AMADEUS_API_KEY=your_api_key_here
   AMADEUS_API_SECRET=your_api_secret_here
   ```

## Usage

### Basic Example

```python
from flight_aggregator import FlightAggregator

# Initialize the aggregator
aggregator = FlightAggregator()

# Search for flights
flights = aggregator.compare_flights(
    origin='NYC',
    destination='LAX',
    departure_date='2025-12-20',
    adults=1,
    max_results=5
)

# Display results
for i, flight in enumerate(flights, 1):
    aggregator.display_flight(flight, i)
```

### Round Trip Search

```python
flights = aggregator.compare_flights(
    origin='NYC',
    destination='LAX',
    departure_date='2025-12-20',
    return_date='2025-12-27',
    adults=2,
    max_results=10
)
```

### Non-Stop Flights Only

```python
flights = aggregator.compare_flights(
    origin='JFK',
    destination='LHR',
    departure_date='2025-12-20',
    non_stop=True,
    currency='EUR'
)
```

## Running the Application

### GUI Version (Recommended)

```bash
python flight_gui.py
```

This opens an interactive window where you can:
- Enter search parameters in form fields
- Click "Search Flights" button
- View results in a scrollable text area
- Search multiple times without restarting

### Command Line Version

```bash
python flight_aggregator.py
```

Interactive terminal-based interface with text prompts.

## Features

- Search for one-way and round-trip flights
- Compare prices across multiple airlines
- Filter by non-stop flights
- Sort results by price
- Support for multiple passengers
- Currency conversion support

## API Rate Limits

The free Amadeus API tier has rate limits. For production use, consider upgrading to a paid plan.

## Airport Codes

Use standard IATA airport codes:
- NYC (All New York airports)
- JFK (John F. Kennedy International)
- LAX (Los Angeles International)
- LHR (London Heathrow)
- etc.
# flight_aggregator
