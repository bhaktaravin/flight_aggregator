"""
Flight Aggregator using Amadeus API
Searches and compares flight offers from multiple airlines
"""

import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Optional


class FlightAggregator:
    def __init__(self):
        """Initialize the Amadeus client with API credentials"""
        load_dotenv()
        
        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("API credentials not found. Please set AMADEUS_API_KEY and AMADEUS_API_SECRET in .env file")
        
        self.amadeus = Client(
            client_id=api_key,
            client_secret=api_secret
        )
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        return_date: Optional[str] = None,
        max_results: int = 10,
        currency: str = "USD",
        non_stop: bool = False
    ) -> List[Dict]:
        """
        Search for flight offers
        
        Args:
            origin: Origin airport IATA code (e.g., 'NYC', 'JFK')
            destination: Destination airport IATA code (e.g., 'LAX', 'LHR')
            departure_date: Departure date in YYYY-MM-DD format
            adults: Number of adult passengers (default: 1)
            return_date: Return date in YYYY-MM-DD format for round trip (optional)
            max_results: Maximum number of results to return (default: 10)
            currency: Currency code for prices (default: 'USD')
            non_stop: Only return non-stop flights (default: False)
        
        Returns:
            List of flight offers with details
        """
        try:
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': adults,
                'max': max_results,
                'currencyCode': currency,
                'nonStop': non_stop
            }
            
            if return_date:
                params['returnDate'] = return_date
            
            print(f"\nAPI Request parameters: {params}")
            
            response = self.amadeus.shopping.flight_offers_search.get(**params)
            
            print(f"API Response status: {response.status_code}")
            print(f"Number of results: {len(response.data) if response.data else 0}")
            
            if not response.data:
                print("\nAPI returned empty results. This could mean:")
                print("- No flights available for these dates")
                print("- Invalid airport codes")
                print("- Date is too far in the future or in the past")
                print("- Non-stop filter is too restrictive")
            
            return response.data
            
        except ResponseError as error:
            print(f"\n❌ API Error: {error}")
            if hasattr(error, 'response'):
                print(f"Status Code: {error.response.status_code}")
                print(f"Error Details: {error.response.body}")
            return []
    
    def parse_flight_offer(self, offer: Dict) -> Dict:
        """
        Parse a flight offer into a more readable format
        
        Args:
            offer: Raw flight offer from Amadeus API
        
        Returns:
            Parsed flight information
        """
        parsed = {
            'id': offer.get('id'),
            'price': {
                'total': offer.get('price', {}).get('total'),
                'currency': offer.get('price', {}).get('currency')
            },
            'itineraries': []
        }
        
        for itinerary in offer.get('itineraries', []):
            segments = []
            for segment in itinerary.get('segments', []):
                segments.append({
                    'departure': {
                        'airport': segment.get('departure', {}).get('iataCode'),
                        'time': segment.get('departure', {}).get('at'),
                        'terminal': segment.get('departure', {}).get('terminal')
                    },
                    'arrival': {
                        'airport': segment.get('arrival', {}).get('iataCode'),
                        'time': segment.get('arrival', {}).get('at'),
                        'terminal': segment.get('arrival', {}).get('terminal')
                    },
                    'carrier': segment.get('carrierCode'),
                    'flight_number': segment.get('number'),
                    'aircraft': segment.get('aircraft', {}).get('code'),
                    'duration': segment.get('duration')
                })
            
            parsed['itineraries'].append({
                'duration': itinerary.get('duration'),
                'segments': segments
            })
        
        return parsed
    
    def compare_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        **kwargs
    ) -> List[Dict]:
        """
        Search and compare flights, returning them sorted by price
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            departure_date: Departure date in YYYY-MM-DD format
            **kwargs: Additional parameters for search_flights
        
        Returns:
            List of parsed and sorted flight offers
        """
        offers = self.search_flights(origin, destination, departure_date, **kwargs)
        
        if not offers:
            print("No flights found")
            return []
        
        parsed_offers = [self.parse_flight_offer(offer) for offer in offers]
        
        # Sort by price
        parsed_offers.sort(key=lambda x: float(x['price']['total']))
        
        return parsed_offers
    
    def display_flight(self, flight: Dict, index: int = None):
        """
        Display flight information in a readable format
        
        Args:
            flight: Parsed flight offer
            index: Optional index number to display
        """
        prefix = f"{index}. " if index is not None else ""
        print(f"\n{prefix}Flight {flight['id']}")
        print(f"Price: {flight['price']['total']} {flight['price']['currency']}")
        
        for i, itinerary in enumerate(flight['itineraries']):
            print(f"\n  {'Outbound' if i == 0 else 'Return'} Journey (Duration: {itinerary['duration']})")
            
            for j, segment in enumerate(itinerary['segments']):
                print(f"    Segment {j+1}:")
                print(f"      {segment['carrier']}{segment['flight_number']}")
                print(f"      {segment['departure']['airport']} → {segment['arrival']['airport']}")
                print(f"      Depart: {segment['departure']['time']}")
                print(f"      Arrive: {segment['arrival']['time']}")
                print(f"      Duration: {segment['duration']}")


def main():
    """Interactive flight search with user input"""
    try:
        aggregator = FlightAggregator()
        
        print("=" * 50)
        print("Flight Aggregator - Search & Compare Flights")
        print("=" * 50)
        
        # Get user input
        origin = input("\nOrigin airport code (e.g., NYC, JFK): ").strip().upper()
        destination = input("Destination airport code (e.g., LAX, LHR): ").strip().upper()
        departure_date = input("Departure date (YYYY-MM-DD): ").strip()
        
        # Optional return date
        return_date_input = input("Return date (YYYY-MM-DD, or press Enter for one-way): ").strip()
        return_date = return_date_input if return_date_input else None
        
        # Number of passengers
        adults_input = input("Number of adult passengers (default: 1): ").strip()
        adults = int(adults_input) if adults_input else 1
        
        # Non-stop preference
        non_stop_input = input("Non-stop flights only? (y/n, default: n): ").strip().lower()
        non_stop = non_stop_input == 'y'
        
        # Max results
        max_results_input = input("Maximum number of results (default: 10): ").strip()
        max_results = int(max_results_input) if max_results_input else 10
        
        # Currency
        currency_input = input("Currency code (default: USD): ").strip().upper()
        currency = currency_input if currency_input else "USD"
        
        print(f"\nSearching for flights from {origin} to {destination}...")
        
        flights = aggregator.compare_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
            max_results=max_results,
            currency=currency,
            non_stop=non_stop
        )
        
        if flights:
            print(f"\nFound {len(flights)} flights (sorted by price):\n")
            print("=" * 50)
            for i, flight in enumerate(flights, 1):
                aggregator.display_flight(flight, i)
                print("-" * 50)
        else:
            print("No flights found. Please check your search parameters.")
            
    except ValueError as e:
        print(f"Invalid input: {e}")
    except KeyboardInterrupt:
        print("\n\nSearch cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
