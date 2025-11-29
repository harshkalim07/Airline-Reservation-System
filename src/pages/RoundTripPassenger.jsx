import { useParams, Link } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import PageTransition from "../components/PageTransition";
import { AuthContext } from "../context/AuthContext";
import useToast from "../hooks/useToast";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import { calculateDynamicPrice } from "../utils/dynamicPricing";

export default function RoundTripPassenger() {
  const { outId, outSeat, inId, inSeat } = useParams();
  const { user } = useContext(AuthContext);
  const { showToast, ToastContainer } = useToast();

  const [outbound, setOutbound] = useState(null);
  const [inbound, setInbound] = useState(null);

  const [passenger, setPassenger] = useState({
    name: "",
    age: "",
    gender: "",
  });

  useEffect(() => {
    const flights = JSON.parse(localStorage.getItem("flights") || "[]");

    setOutbound(flights.find(f => f.id === outId));
    setInbound(flights.find(f => f.id === inId));
  }, [outId, inId]);

  if (!outbound || !inbound) return <div>Loading...</div>;

  function handleSubmit(e) {
    e.preventDefault();

    if (!passenger.name || !passenger.age || !passenger.gender) {
      showToast("Please fill all passenger details", "error");
      return;
    }

    showToast("Passenger Details Saved", "success");

    setTimeout(() => {
      window.location.href = `/roundtrip/pay/${outId}/${outSeat}/${inId}/${inSeat}/${passenger.name}`;
    }, 800);
  }

  function FlightCard({ flight, seat, title }) {
    const price = calculateDynamicPrice(flight);

    return (
      <div className="card mb-4">
        <h3 className="text-xl font-bold mb-2">{title}</h3>

        <div className="flex gap-4">
          <img src={getAirlineLogo(flight.airline)} className="w-20 h-20 object-contain" />

          <div>
            <p className="font-bold">{flight.airline}</p>
            <p>{flight.source} → {flight.destination}</p>
            <p className="text-gray-500 text-sm">
              {flight.departure_time} - {flight.arrival_time}
            </p>
            <p className="mt-1 text-green-600 font-bold">₹{price}</p>

            <p className="mt-1 text-sm">Seat Selected: <strong>{seat}</strong></p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="max-w-3xl mx-auto">

        {/* OUTBOUND SUMMARY */}
        <FlightCard
          flight={outbound}
          seat={outSeat}
          title="Outbound Flight"
        />

        {/* RETURN SUMMARY */}
        <FlightCard
          flight={inbound}
          seat={inSeat}
          title="Return Flight"
        />

        {/* PASSENGER FORM */}
        <div className="card mt-6">
          <h2 className="text-2xl font-bold mb-4">Passenger Details</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              className="input"
              placeholder="Full Name"
              value={passenger.name}
              onChange={e => setPassenger({ ...passenger, name: e.target.value })}
            />

            <input
              className="input"
              placeholder="Age"
              type="number"
              value={passenger.age}
              onChange={e => setPassenger({ ...passenger, age: e.target.value })}
            />

            <select
              className="input"
              value={passenger.gender}
              onChange={e => setPassenger({ ...passenger, gender: e.target.value })}
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>

            {/* Logged in user info */}
            {user && (
              <div className="text-sm mt-3 text-gray-700">
                <p>Email: <strong>{user.email}</strong></p>
                <p>Mobile: <strong>{user.mobile}</strong></p>
              </div>
            )}

            <button className="btn-primary w-full mt-4">
              Continue to Payment
            </button>
          </form>
        </div>

        <ToastContainer />
      </div>
    </PageTransition>
  );
}
