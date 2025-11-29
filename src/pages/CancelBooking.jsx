import { useParams, useNavigate } from "react-router-dom";
import useToast from "../hooks/useToast";

export default function CancelBooking() {
  const { pnr } = useParams();
  const navigate = useNavigate();

  const { showToast, ToastContainer } = useToast();

  function handleCancel() {
    const bookings = JSON.parse(localStorage.getItem("bookings") || "[]");

    const updated = bookings.map(b =>
      b.pnr === pnr ? { ...b, status: "cancelled" } : b
    );

    localStorage.setItem("bookings", JSON.stringify(updated));

    showToast("Booking cancelled!", "success");
    navigate("/history");
  }

  return (
    <div className="max-w-md mx-auto card text-center">
      <h2 className="text-xl font-bold mb-4">Cancel Booking</h2>

      <button onClick={handleCancel} className="btn-danger w-full">
        Confirm Cancellation
      </button>

      <ToastContainer />
    </div>
  );
}
