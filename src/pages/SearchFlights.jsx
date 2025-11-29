import { useState } from "react";
import { Link } from "react-router-dom";
import Input from "../components/Input";
import PageTransition from "../components/PageTransition";
import { calculateDynamicPrice } from "../utils/dynamicPricing";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import api from "../services/api";

export default function SearchFlights() {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [tripType, setTripType] = useState("oneway");  
  const [departDate, setDepartDate] = useState("");
  const [returnDate, setReturnDate] = useState("");
  const [outboundFlights, setOutboundFlights] = useState([]);
  const [returnFlights, setReturnFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      // Search outbound flights
      const outboundResponse = await api.get('/flights/search', {
        params: {
          source,
          destination,
          date: departDate,
          passengers: 1
        }
      });
      
      setOutboundFlights(outboundResponse.data.flights || []);
      
      // If round trip, search return flights
      if (tripType === "roundtrip" && returnDate) {
        const returnResponse = await api.get('/flights/search', {
          params: {
            source: destination,  // Swap source and destination
            destination: source,
            date: returnDate,
            passengers: 1
          }
        });
        
        setReturnFlights(returnResponse.data.flights || []);
      } else {
        setReturnFlights([]);
      }
      
    } catch (err) {
      console.error('Search error:', err);
      setError(err.response?.data?.error || 'Failed to search flights');
      setOutboundFlights([]);
      setReturnFlights([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageTransition>
      <div className="card max-w-3xl mx-auto">
        <h2 className="text-2xl font-semibold mb-4">Search Flights</h2>
        
        {/* Trip Type Selection */}
        <div className="flex gap-4 mb-4">
          <label className="flex items-center gap-2">
            <input
              type="radio"
              value="oneway"
              checked={tripType === "oneway"}
              onChange={(e) => setTripType(e.target.value)}
            />
            One-way
          </label>
          <label className="flex items-center gap-2">
            <input
              type="radio"
              value="roundtrip"
              checked={tripType === "roundtrip"}
              onChange={(e) => setTripType(e.target.value)}
            />
            Round Trip
          </label>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Input 
              label="From" 
              value={source} 
              onChange={setSource}
              placeholder="e.g., Mumbai" 
              required
            />
            <Input 
              label="To" 
              value={destination} 
              onChange={setDestination}
              placeholder="e.g., Delhi" 
              required
            />
          </div>
          
          <div className="grid md:grid-cols-2 gap-4">
            <Input 
              label="Departure Date" 
              type="date" 
              value={departDate} 
              onChange={setDepartDate}
              required
            />
            {tripType === "roundtrip" && (
              <Input 
                label="Return Date" 
                type="date" 
                value={returnDate} 
                onChange={setReturnDate}
                required
              />
            )}
          </div>
          
          <button 
            className="btn-primary w-full" 
            disabled={loading}
          >
            {loading ? 'Searching...' : 'Search Flights'}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Outbound Flights Results */}
        {outboundFlights.length > 0 && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-3">
              {tripType === "oneway" ? "Available Flights" : "Outbound Flights"}
            </h3>
            <div className="space-y-3">
              {outboundFlights.map((flight) => (
                <div key={flight.id} className="border p-4 rounded flex justify-between items-center hover:bg-gray-50">
                  <div className="flex items-center gap-4">
                    <img 
                      src={getAirlineLogo(flight.airline)} 
                      alt={flight.airline}
                      className="w-12 h-12 object-contain"
                    />
                    <div>
                      <p className="font-semibold">{flight.airline}</p>
                      <p className="text-sm text-gray-600">
                        {flight.source} → {flight.destination}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(flight.departure_time).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-indigo-600">
                      ₹{flight.price?.toFixed(2) || 'N/A'}
                    </p>
                    <p className="text-xs text-gray-500">
                      {flight.available_seats} seats left
                    </p>
                    <Link 
                      to={`/flight/${flight.flight_id}`}
                      state={{ flight }}
                      className="btn-secondary mt-2 inline-block text-sm px-4 py-1"
                    >
                      Select
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Return Flights Results */}
        {tripType === "roundtrip" && returnFlights.length > 0 && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-3">Return Flights</h3>
            <div className="space-y-3">
              {returnFlights.map((flight) => (
                <div key={flight.id} className="border p-4 rounded flex justify-between items-center hover:bg-gray-50">
                  <div className="flex items-center gap-4">
                    <img 
                      src={getAirlineLogo(flight.airline)} 
                      alt={flight.airline}
                      className="w-12 h-12 object-contain"
                    />
                    <div>
                      <p className="font-semibold">{flight.airline}</p>
                      <p className="text-sm text-gray-600">
                        {flight.source} → {flight.destination}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(flight.departure_time).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-indigo-600">
                      ₹{flight.price?.toFixed(2) || 'N/A'}
                    </p>
                    <p className="text-xs text-gray-500">
                      {flight.available_seats} seats left
                    </p>
                    <Link 
                      to={`/flight/${flight.flight.id}`}
                      state={{ flight }}
                      className="btn-secondary mt-2 inline-block text-sm px-4 py-1"
                    >
                      Select
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!loading && outboundFlights.length === 0 && !error && departDate && (
          <div className="mt-6 text-center text-gray-500">
            No flights found. Try different dates or destinations.
          </div>
        )}
      </div>
    </PageTransition>
  );
}