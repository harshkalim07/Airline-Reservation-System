import { useParams, Link } from "react-router-dom";

export default function BookingSuccess() {
  const { pnr } = useParams();
  return (
    <div className="card max-w-md mx-auto text-center">
      <h2 className="text-2xl font-semibold mb-4">Booking Successful</h2>
      <p className="text-lg font-bold mb-4">PNR: <span className="text-blue-700">{pnr}</span></p>
      <Link to="/history" className="btn-primary">View My Bookings</Link>
    </div>
  );
}
