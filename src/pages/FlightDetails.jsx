import { useState, useEffect } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import api from "../services/api";
import PageTransition from "../components/PageTransition";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import AnimatedSeatMap from "../components/AnimatedSeatMap";

export default function FlightDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [flight, setFlight] = useState(location.state?.flight || null);
  const [loading, setLoading] = useState(!location.state?.flight);
  const [error, setError] = useState("");
  const [showSeatMap, setShowSeatMap] = useState(false);
  const [selectedSeat, setSelectedSeat] = useState(null);
  const [availableSeats, setAvailableSeats] = useState([]);

  useEffect(() => {
    if (!flight) {
      fetchFlightDetails();
    } else {
      fetchAvailableSeats();
    }
  }, [id]);

  async function fetchFlightDetails() {
    try {
      setLoading(true);
      setError("");
      
      const response = await api.get(`/flights/${id}`);
      setFlight(response.data.flight);
      fetchAvailableSeats();
      
    } catch (err) {
      console.error('Error fetching flight:', err);
      setError(err.response?.data?.error || 'Flight not found');
    } finally {
      setLoading(false);
    }
  }

  async function fetchAvailableSeats() {
    try {
      const response = await api.get(`/flights/${id}/seats`);
      setAvailableSeats(response.data.available_seats || []);
    } catch (err) {
      console.error('Error fetching seats:', err);
    }
  }

  function handleProceedToBook() {
    setShowSeatMap(true);
  }

  function handleSeatSelect(seat) {
  console.log('🎫 Seat selected:', seat, typeof seat);
  setSelectedSeat(seat);
}

  function handleConfirmSeat() {
    if (!selectedSeat) {
      alert('Please select a seat');
      return;
    }
    navigate(`/book/${flight.flight_id}/${selectedSeat}`, {
      state: { flight } 
    });
  }

  if (loading) {
    return (
      <PageTransition>
        <div className="card max-w-2xl mx-auto text-center">
          <p className="text-gray-600">Loading flight details...</p>
        </div>
      </PageTransition>
    );
  }

  if (error || !flight) {
    return (
      <PageTransition>
        <div className="card max-w-2xl mx-auto text-center">
          <h2 className="text-2xl font-semibold mb-4 text-red-600">
            {error || "Flight not found."}
          </h2>
          <button 
            onClick={() => navigate('/search')}
            className="btn-primary"
          >
            Back to Search
          </button>
        </div>
      </PageTransition>
    );
  }

  const departureDate = new Date(flight.departure_time);
  const arrivalDate = new Date(flight.arrival_time);
  const duration = Math.round((arrivalDate - departureDate) / (1000 * 60));
  const hours = Math.floor(duration / 60);
  const minutes = duration % 60;

  if (showSeatMap) {
    // Convert seats object from backend format to component format
    const seatsMap = {};
    Object.keys(flight.seats || {}).forEach(seatKey => {
      const seat = flight.seats[seatKey];
      seatsMap[seatKey] = seat.status === 'available' ? 'available' : 'booked';
    });

    return (
      <PageTransition>
        <div className="card max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-4">Select Your Seat</h2>
          
          <div className="mb-4 p-4 bg-blue-50 rounded">
            <p className="text-sm text-gray-700">
              <strong>{flight.airline}</strong> - {flight.source} → {flight.destination}
            </p>
            <p className="text-sm text-gray-600">
              Selected Seat: <strong>{selectedSeat || 'None'}</strong>
            </p>
          </div>

          <AnimatedSeatMap
            rows={30}
            seatsMap={seatsMap}
            basePrice={flight.price}
            selected={selectedSeat}
            onSelect={handleSeatSelect}
          />

          <div className="flex gap-4 mt-6">
            <button
              onClick={() => setShowSeatMap(false)}
              className="btn-secondary flex-1"
            >
              Back to Details
            </button>
            <button
              onClick={handleConfirmSeat}
              className="btn-primary flex-1"
              disabled={!selectedSeat}
            >
              Confirm Seat
            </button>
          </div>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="card max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-center">Flight Details</h2>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          {/* Airline Info */}
          <div className="flex items-center gap-4 mb-6 pb-6 border-b">
            <img 
              src={getAirlineLogo(flight.airline)} 
              alt={flight.airline}
              className="w-16 h-16 object-contain"
            />
            <div>
              <h3 className="text-2xl font-semibold">{flight.airline}</h3>
              <p className="text-gray-600">Flight {flight.flight_id || flight.id}</p>
            </div>
          </div>

          {/* Route Info */}
          <div className="grid md:grid-cols-3 gap-6 mb-6">
            <div>
              <p className="text-sm text-gray-500 mb-1">From</p>
              <p className="text-2xl font-bold">{flight.source}</p>
              <p className="text-sm text-gray-600">
                {departureDate.toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </p>
              <p className="text-xs text-gray-500">
                {departureDate.toLocaleDateString()}
              </p>
            </div>

            <div className="text-center flex flex-col justify-center">
              <p className="text-sm text-gray-500 mb-2">Duration</p>
              <div className="flex items-center justify-center gap-2">
                <div className="h-px bg-gray-300 flex-1"></div>
                <span className="text-gray-600 font-semibold">
                  {hours}h {minutes}m
                </span>
                <div className="h-px bg-gray-300 flex-1"></div>
              </div>
              <p className="text-xs text-gray-500 mt-2">Non-stop</p>
            </div>

            <div className="text-right">
              <p className="text-sm text-gray-500 mb-1">To</p>
              <p className="text-2xl font-bold">{flight.destination}</p>
              <p className="text-sm text-gray-600">
                {arrivalDate.toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </p>
              <p className="text-xs text-gray-500">
                {arrivalDate.toLocaleDateString()}
              </p>
            </div>
          </div>

          {/* Price and Seats */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-600 mb-1">Price per person</p>
                <p className="text-3xl font-bold text-indigo-600">
                  ₹{flight.price?.toFixed(2) || 'N/A'}
                </p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 mb-1">Available Seats</p>
                <p className="text-2xl font-semibold text-green-600">
                  {availableSeats.length || 0}
                </p>
              </div>
            </div>
          </div>

          {/* Amenities */}
          <div className="mb-6">
            <h4 className="font-semibold mb-3">Amenities</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="flex items-center gap-2 text-sm">
                <span>✓</span>
                <span>Cabin Baggage</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span>✓</span>
                <span>Check-in Baggage</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span>✓</span>
                <span>In-flight Meals</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span>✓</span>
                <span>WiFi Available</span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/search')}
              className="btn-secondary flex-1"
            >
              Back to Search
            </button>
            <button
              onClick={handleProceedToBook}
              className="btn-primary flex-1"
              disabled={!availableSeats.length}
            >
              {availableSeats.length > 0 ? 'Select Seat & Book' : 'Sold Out'}
            </button>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}