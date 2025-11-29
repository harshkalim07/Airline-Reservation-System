import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import useToast from "../hooks/useToast";
import PageTransition from "../components/PageTransition";
import BoardingPass from "../components/BoardingPass";
import api from "../services/api";

export default function TicketPage() {
  const { pnr } = useParams();
  const navigate = useNavigate();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const { showToast, ToastContainer } = useToast();

  useEffect(() => {
    fetchBooking();
  }, [pnr]);

  const fetchBooking = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/bookings/${pnr}`);
      setBooking(response.data);
    } catch (error) {
      console.error("Error fetching booking:", error);
      showToast(
        error.response?.data?.error || "Failed to load ticket",
        "error"
      );
      // Redirect to bookings page after 2 seconds
      setTimeout(() => navigate("/bookings"), 2000);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <PageTransition>
        <div className="text-center mt-10">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading ticket...</p>
        </div>
      </PageTransition>
    );
  }

  if (!booking) {
    return (
      <PageTransition>
        <div className="text-center mt-10 text-gray-600">
          <p>Ticket not found</p>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        {/* Booking Confirmation Header */}
        <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-green-500"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800">
                Booking Confirmed! Your PNR is: <strong>{booking.pnr}</strong>
              </p>
            </div>
          </div>
        </div>

        {/* Boarding Pass */}
        <BoardingPass ticket={booking} />

        {/* Booking Details */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Booking Details</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600 text-sm">PNR Number</p>
              <p className="font-semibold">{booking.pnr}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Status</p>
              <p className="font-semibold capitalize">{booking.status}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Passenger Name</p>
              <p className="font-semibold">{booking.passenger_name}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Seat Number</p>
              <p className="font-semibold">{booking.seat_number}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Booking Date</p>
              <p className="font-semibold">
                {new Date(booking.booking_date).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Payment Status</p>
              <p className="font-semibold capitalize">
                {booking.payment_status}
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center">
          <button
            className="btn-primary"
            onClick={() => window.print()}
          >
            Download Ticket (PDF)
          </button>
          <button
            className="btn-secondary"
            onClick={() => navigate("/bookings")}
          >
            View All Bookings
          </button>
        </div>

        <ToastContainer />
      </div>
    </PageTransition>
  );
}