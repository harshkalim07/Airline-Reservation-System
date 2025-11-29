import { useParams, useNavigate } from "react-router-dom";
import useToast from "../hooks/useToast";

export default function PaymentPage() {
  const { flightId, seat, passenger } = useParams();
  const navigate = useNavigate();

  const { showToast, ToastContainer } = useToast();

  function handlePayment(success) {
    const pnr = "PNR" + Math.floor(Math.random() * 999999);

    if (success) {
      showToast("Payment successful!", "success");

      const bookings = JSON.parse(localStorage.getItem("bookings") || "[]");

      bookings.push({
        pnr,
        passenger,
        seat,
        flightId,
        status: "confirmed",
        date: new Date().toISOString()
      });

      localStorage.setItem("bookings", JSON.stringify(bookings));

      navigate(`/ticket/${pnr}`);
      return;
    }

    showToast("Payment failed!", "error");
  }

  return (
    <div className="max-w-md mx-auto card text-center">
      <h2 className="text-2xl font-bold mb-4">Payment</h2>

      <p className="mb-4">Passenger: <strong>{passenger}</strong></p>
      <p>Seat: <strong>{seat}</strong></p>

      <div className="mt-6 space-y-3">
        <button className="btn-success w-full" onClick={() => handlePayment(true)}>Pay Now</button>
        <button className="btn-danger w-full" onClick={() => handlePayment(false)}>Simulate Failure</button>
      </div>

      <ToastContainer />
    </div>
  );
}
