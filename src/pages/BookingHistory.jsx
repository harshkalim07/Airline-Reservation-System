import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import useToast from "../hooks/useToast";
import api from "../services/api";
import PageTransition from "../components/PageTransition";

export default function BookingHistory() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { showToast, ToastContainer } = useToast();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const response = await api.get("/bookings");
      
      // Parse response if it's a string
      const data = typeof response.data === 'string' ? JSON.parse(response.data) : response.data;
      
      console.log('Parsed data:', data);
      console.log('data.bookings:', data.bookings);
      
      const bookingsList = data?.bookings || [];
      console.log('Final bookingsList:', bookingsList);
      console.log('Bookings count:', bookingsList.length);
      
      setBookings(bookingsList);
      
      if (bookingsList.length === 0) {
        showToast("No bookings found", "info");
      }
      
    } catch (error) {
      console.error("Error fetching bookings:", error);
      showToast(
        error.response?.data?.error || "Failed to load bookings",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (pnr) => {
    if (!confirm("Are you sure you want to cancel this booking?")) {
      return;
    }

    try {
      await api.put(`/bookings/${pnr}/cancel`);
      showToast("Booking cancelled successfully", "success");
      fetchBookings();
    } catch (error) {
      console.error("Error cancelling booking:", error);
      showToast(
        error.response?.data?.error || "Failed to cancel booking",
        "error"
      );
    }
  };

  if (loading) {
    return (
      <PageTransition>
        <div className="max-w-4xl mx-auto p-6">
          <div className="text-center mt-10">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading bookings...</p>
          </div>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6">My Bookings</h2>
          
          {bookings.length === 0 ? (
            <div className="text-center py-8">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
              <p className="mt-4 text-gray-600">No bookings yet.</p>
              <Link
                to="/search"
                className="mt-4 inline-block btn-primary"
              >
                Search Flights
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((booking) => (
                <div
                  key={booking.pnr}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="font-semibold text-lg">
                        {booking.flight_id}
                      </h3>
                      <p className="text-sm text-gray-600">
                        PNR: {booking.pnr}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        booking.status === "confirmed"
                          ? "bg-green-100 text-green-800"
                          : booking.status === "cancelled"
                          ? "bg-red-100 text-red-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {booking.status.charAt(0).toUpperCase() +
                        booking.status.slice(1)}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div>
                      <p className="text-gray-600">Passenger</p>
                      <p className="font-medium">{booking.passenger_name}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Seat</p>
                      <p className="font-medium">{booking.seat_number}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Booking Date</p>
                      <p className="font-medium">
                        {new Date(booking.booking_date).toLocaleDateString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600">Payment</p>
                      <p className="font-medium capitalize">
                        {booking.payment_status}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <Link
                      to={`/ticket/${booking.pnr}`}
                      className="btn-primary flex-1 text-center"
                    >
                      View Ticket
                    </Link>
                    {booking.status === "confirmed" && (
                      <button
                        onClick={() => handleCancelBooking(booking.pnr)}
                        className="btn-danger flex-1"
                      >
                        Cancel Booking
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        <ToastContainer />
      </div>
    </PageTransition>
  );
}