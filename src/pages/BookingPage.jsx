import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../services/api";
import useToast from "../hooks/useToast";
import PageTransition from "../components/PageTransition";
import { getSeatClass, seatPriceMultiplier } from "../utils/seatClass";

export default function BookingPage() {
  const { flightId, seat } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useContext(AuthContext);

  const [flight, setFlight] = useState(location.state?.flight || null);
  const [passenger, setPassenger] = useState("");
  const [loading, setLoading] = useState(false);

  const { showToast, ToastContainer } = useToast();

  useEffect(() => {
    if (!flight) {
      fetchFlightDetails();
    }
  }, [flightId]);

  async function fetchFlightDetails() {
    try {
      const response = await api.get(`/flights/${flightId}`);
      setFlight(response.data.flight);
    } catch (error) {
      showToast("Failed to load flight details", "error");
      navigate('/search');
    }
  }

  if (!flight) return <div className="text-center p-8">Loading...</div>;

  const seatRow = seat.replace(/[A-Z]/g, '');
  const seatClass = getSeatClass(Number(seatRow));
  const multiplier = seatPriceMultiplier(seatClass);
  const finalPrice = Math.round(flight.price * multiplier);

  async function handleConfirm() {
    if (!passenger.trim()) {
      showToast("Please enter passenger name", "error");
      return;
    }

    if (!user) {
      showToast("Please login to continue", "error");
      navigate('/login');
      return;
    }

    try {
      setLoading(true);

      // Log the payload for debugging
      const payload = {
        flight_id: flightId,  // This is the flight_id string like "AI101" from URL
        passenger_name: passenger.trim(),
        seat_number: seat  // This is the seat like "1E" from URL
      };
      
      console.log('Booking payload:', payload);
      console.log('Flight object:', flight);

      const response = await api.post('/bookings', payload);
      
      console.log('Full response:', response);
      console.log('Response data:', response.data);
      console.log('Booking PNR:', response.data?.booking?.pnr);

      showToast("Booking successful!", "success");
      
      // Navigate to ticket page
      if (response.data?.booking?.pnr) {
        navigate(`/ticket/${response.data.booking.pnr}`);
      } else {
        console.error('No PNR in response!');
        showToast("Booking created but PNR missing. Check My Bookings.", "warning");
        navigate('/bookings');
      }

    } catch (error) {
      console.error('Booking error:', error);
      console.error('Error response:', error.response?.data);
      showToast(
        error.response?.data?.error || "Booking failed. Please try again.",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageTransition>
      <div className="max-w-lg mx-auto card">
        <h2 className="text-2xl font-bold mb-4">Confirm Booking</h2>

        <div className="bg-gray-50 p-4 rounded mb-4 space-y-2">
          <p><strong>Flight:</strong> {flight.airline} ({flightId})</p>
          <p><strong>Route:</strong> {flight.source} → {flight.destination}</p>
          <p><strong>Seat:</strong> {seat}</p>
          <p><strong>Class:</strong> {seatClass}</p>
          <p className="text-xl pt-2">
            <strong>Fare: ₹{finalPrice}</strong>
          </p>
        </div>

        <input
          type="text"
          placeholder="Passenger Name"
          className="input mt-4 w-full"
          value={passenger}
          onChange={(e) => setPassenger(e.target.value)}
          disabled={loading}
        />

        <button 
          onClick={handleConfirm} 
          className="btn-primary w-full mt-4"
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Confirm Booking'}
        </button>

        <ToastContainer />
      </div>
    </PageTransition>
  );
}