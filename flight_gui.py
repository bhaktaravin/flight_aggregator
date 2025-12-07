"""
Flight Aggregator GUI using Tkinter
Interactive interface to search and compare flight offers
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime, timedelta
from flight_aggregator import FlightAggregator
from tkcalendar import DateEntry


class FlightSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Aggregator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize the flight aggregator
        try:
            self.aggregator = FlightAggregator()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize API: {e}\n\nPlease check your .env file.")
            self.root.destroy()
            return
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Bind Enter key to search
        self.root.bind('<Return>', lambda e: self.search_flights())
    
    def setup_styles(self):
        """Configure the application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Search.TButton', font=('Arial', 10, 'bold'), padding=10)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="✈️ Flight Search & Comparison", style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Search Form
        self.create_search_form(main_frame)
        
        # Search Button
        self.search_button = ttk.Button(
            main_frame, 
            text="Search Flights", 
            command=self.search_flights,
            style='Search.TButton'
        )
        self.search_button.grid(row=5, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Results area
        results_label = ttk.Label(main_frame, text="Search Results:", style='Header.TLabel')
        results_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=('Courier', 10)
        )
        self.results_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def create_search_form(self, parent):
        """Create the search form fields"""
        row = 1
        
        # Origin with example
        origin_frame = ttk.Frame(parent)
        origin_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        origin_frame.columnconfigure(1, weight=1)
        
        ttk.Label(origin_frame, text="From (Airport Code):").grid(row=0, column=0, sticky=tk.W)
        self.origin_entry = ttk.Entry(origin_frame, width=40, font=('Arial', 11))
        self.origin_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.origin_entry.insert(0, "JFK")
        ttk.Label(origin_frame, text="Examples: JFK, LAX, ORD, ATL", font=('Arial', 8), foreground='gray').grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        row += 1
        
        # Destination with example
        dest_frame = ttk.Frame(parent)
        dest_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        dest_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dest_frame, text="To (Airport Code):").grid(row=0, column=0, sticky=tk.W)
        self.destination_entry = ttk.Entry(dest_frame, width=40, font=('Arial', 11))
        self.destination_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        self.destination_entry.insert(0, "LAX")
        ttk.Label(dest_frame, text="Examples: LAX, MIA, DFW, SEA", font=('Arial', 8), foreground='gray').grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        row += 1
        
        # Dates frame
        dates_frame = ttk.Frame(parent)
        dates_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        dates_frame.columnconfigure(1, weight=1)
        dates_frame.columnconfigure(3, weight=1)
        
        # Departure date with calendar picker
        ttk.Label(dates_frame, text="Departure Date:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        default_departure = datetime.now() + timedelta(days=14)
        self.departure_cal = DateEntry(
            dates_frame, 
            width=18, 
            background='darkblue',
            foreground='white', 
            borderwidth=2,
            font=('Arial', 11),
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now(),
            year=default_departure.year,
            month=default_departure.month,
            day=default_departure.day
        )
        self.departure_cal.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(dates_frame, text="📅 Click to open calendar", font=('Arial', 8), foreground='gray').grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Return date with calendar picker
        ttk.Label(dates_frame, text="Return Date:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.return_cal = DateEntry(
            dates_frame, 
            width=18, 
            background='darkblue',
            foreground='white', 
            borderwidth=2,
            font=('Arial', 11),
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        self.return_cal.grid(row=0, column=3, sticky=tk.W, padx=5)
        # Don't set default date for return - leave it as today but make it optional
        ttk.Label(dates_frame, text="📅 Optional for round trip", font=('Arial', 8), foreground='gray').grid(row=1, column=3, sticky=tk.W, padx=5)
        
        # Add checkbox to enable/disable return date
        self.return_enabled = tk.BooleanVar(value=False)
        return_check = ttk.Checkbutton(dates_frame, text="Round trip", variable=self.return_enabled)
        return_check.grid(row=0, column=4, sticky=tk.W, padx=5)
        
        row += 1
        
        # Options frame
        options_frame = ttk.Frame(parent)
        options_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        options_frame.columnconfigure(5, weight=1)
        
        # Adults
        ttk.Label(options_frame, text="Number of Passengers:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.adults_spinbox = ttk.Spinbox(options_frame, from_=1, to=9, width=10, font=('Arial', 11))
        self.adults_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.adults_spinbox.set(1)
        
        # Max results
        ttk.Label(options_frame, text="Show up to:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.max_results_spinbox = ttk.Spinbox(options_frame, from_=5, to=50, width=10, font=('Arial', 11))
        self.max_results_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
        self.max_results_spinbox.set(10)
        ttk.Label(options_frame, text="results", font=('Arial', 9)).grid(row=0, column=3, sticky=tk.W, padx=(80, 5))
        
        # Currency
        ttk.Label(options_frame, text="Currency:").grid(row=0, column=4, sticky=tk.W, padx=(20, 5))
        self.currency_combo = ttk.Combobox(options_frame, values=['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY'], width=10, font=('Arial', 11), state='readonly')
        self.currency_combo.grid(row=0, column=5, sticky=tk.W, padx=5)
        self.currency_combo.set('USD')
        row += 1
        
        # Non-stop checkbox - larger and more visible
        self.non_stop_var = tk.BooleanVar()
        self.non_stop_check = ttk.Checkbutton(
            parent, 
            text="✈️ Show only non-stop flights (no layovers)", 
            variable=self.non_stop_var
        )
        self.non_stop_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=10)
    
    def search_flights(self):
        """Perform flight search in a separate thread"""
        # Validate inputs
        origin = self.origin_entry.get().strip().upper()
        destination = self.destination_entry.get().strip().upper()
        
        if not origin or not destination:
            messagebox.showwarning("Input Error", "Please fill in Origin and Destination")
            return
        
        if len(origin) != 3 or len(destination) != 3:
            messagebox.showwarning("Input Error", "Airport codes must be 3 letters (e.g., JFK, LAX)")
            return
        
        # Disable search button during search
        self.search_button.config(state='disabled')
        self.status_label.config(text="Searching flights...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔍 Searching for flights...\n\n")
        
        # Run search in separate thread to keep GUI responsive
        thread = threading.Thread(target=self._perform_search)
        thread.daemon = True
        thread.start()
    
    def _perform_search(self):
        """Internal method to perform the actual search"""
        try:
            # Get search parameters
            origin = self.origin_entry.get().strip().upper()
            destination = self.destination_entry.get().strip().upper()
            departure_date = self.departure_cal.get_date().strftime('%Y-%m-%d')
            
            # Get return date if round trip is enabled
            return_date = None
            if self.return_enabled.get():
                return_date = self.return_cal.get_date().strftime('%Y-%m-%d')
            
            adults = int(self.adults_spinbox.get())
            max_results = int(self.max_results_spinbox.get())
            currency = self.currency_combo.get()
            non_stop = self.non_stop_var.get()
            
            # Perform search
            flights = self.aggregator.compare_flights(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                max_results=max_results,
                currency=currency,
                non_stop=non_stop
            )
            
            # Update GUI in main thread
            self.root.after(0, self._display_results, flights)
            
        except Exception as e:
            self.root.after(0, self._display_error, str(e))
    
    def _display_results(self, flights):
        """Display search results in the GUI"""
        self.results_text.delete(1.0, tk.END)
        
        if not flights:
            self.results_text.insert(tk.END, "❌ No flights found.\n\n")
            self.results_text.insert(tk.END, "Possible reasons:\n")
            self.results_text.insert(tk.END, "• Invalid airport codes\n")
            self.results_text.insert(tk.END, "• No flights available for selected dates\n")
            self.results_text.insert(tk.END, "• Date is in the past\n")
            self.results_text.insert(tk.END, "• Non-stop filter is too restrictive\n")
            self.status_label.config(text="No flights found")
        else:
            self.results_text.insert(tk.END, f"✅ Found {len(flights)} flights (sorted by price)\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            for i, flight in enumerate(flights, 1):
                self._format_flight(flight, i)
                self.results_text.insert(tk.END, "-" * 80 + "\n\n")
            
            self.status_label.config(text=f"Found {len(flights)} flights")
        
        # Re-enable search button
        self.search_button.config(state='normal')
    
    def _format_flight(self, flight, index):
        """Format a single flight for display"""
        self.results_text.insert(tk.END, f"Flight #{index}\n", 'bold')
        self.results_text.insert(tk.END, f"💰 Price: {flight['price']['total']} {flight['price']['currency']}\n\n")
        
        for i, itinerary in enumerate(flight['itineraries']):
            trip_type = "🛫 Outbound" if i == 0 else "🛬 Return"
            self.results_text.insert(tk.END, f"{trip_type} Journey (Duration: {itinerary['duration']})\n")
            
            for j, segment in enumerate(itinerary['segments']):
                self.results_text.insert(tk.END, f"  ✈️  Segment {j+1}: ")
                self.results_text.insert(tk.END, f"{segment['carrier']}{segment['flight_number']}\n")
                self.results_text.insert(tk.END, f"      {segment['departure']['airport']} → {segment['arrival']['airport']}\n")
                self.results_text.insert(tk.END, f"      Depart: {segment['departure']['time']}\n")
                self.results_text.insert(tk.END, f"      Arrive: {segment['arrival']['time']}\n")
                self.results_text.insert(tk.END, f"      Duration: {segment['duration']}\n")
            self.results_text.insert(tk.END, "\n")
    
    def _display_error(self, error_message):
        """Display error message in the GUI"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"❌ Error: {error_message}\n")
        self.status_label.config(text="Error occurred")
        self.search_button.config(state='normal')


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = FlightSearchGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
