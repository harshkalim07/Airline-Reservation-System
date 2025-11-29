import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import PageTransition from "../components/PageTransition";
import useToast from "../hooks/useToast";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import { calculateDynamicPrice } from "../utils/dynamicPricing";

export default function RoundTripBooking() {
  const { outboundId, returnId } = useParams();
  const { showToast, ToastContainer } = useToast();

  const [outbound, setOutbound] = useState(null);
  const [inbound, setInbound] = useState(null);
  const [outSeat, setOutSeat] = useState(null);
  const [inSeat, setInSeat] = useState(null);

  useEffect(() => {
    const flights = JSON.parse(localStorage.getItem("flights") || "[]");

    const ob = flights.find(f => f.id === outboundId);
    const ib = flights.find(f => f.id === returnId);

    setOutbound(ob);
    setInbound(ib);
  }, [outboundId, returnId]);

  if (!outbound || !inbound) return <div className="text-center">Loading...</div>;

  // Generic seat generator
  function renderSeats(flight, selectedSeat, setSeat) {
    const seats = flight.seats || {};

    return (
      <div className="grid grid-cols-5 gap-3 mb-4">
        {Array.from({ length: 30 }).map((_, i) => {
          const seat = i + 1;
          const isBooked = seats[seat] === "booked";

          return (
            <button
              key={seat}
              disabled={isBooked}
              onClick={() => {
                setSeat(seat);
                showToast(`Seat ${seat} selected`, "success");
              }}
              className={`p-3 rounded-lg text-center shadow-sm transition
                ${isBooked ? "bg-red-600 text-white cursor-not-allowed" :
                selectedSeat === seat ? "bg-blue-600 text-white" :
                "bg-gray-200 hover:bg-gray-300"}`}
            >
              {seat}
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="max-w-4xl mx-auto space-y-10">

        {/* OUTBOUND */}
        <div className="card">
          <h2 className="text-2xl font-bold mb-2">Outbound Flight</h2>

          <div className="flex gap-4">
            <img src={getAirlineLogo(outbound.airline)} className="w-20 h-20 object-contain" />

            <div>
              <p className="font-bold">{outbound.airline}</p>
              <p>{outbound.source} → {outbound.destination}</p>
              <p className="text-gray-500">
                {outbound.departure_time} - {outbound.arrival_time}
              </p>

              <p className="mt-1 font-bold text-green-600">
                ₹{calculateDynamicPrice(outbound)}
              </p>
            </div>
          </div>

          <h3 className="text-xl font-semibold mt-4 mb-2">Select Seat</h3>

          {renderSeats(outbound, outSeat, setOutSeat)}
        </div>

        {/* RETURN */}
        <div className="card">
          <h2 className="text-2xl font-bold mb-2">Return Flight</h2>

          <div className="flex gap-4">
            <img src={getAirlineLogo(inbound.airline)} className="w-20 h-20 object-contain" />

            <div>
              <p className="font-bold">{inbound.airline}</p>
              <p>{inbound.source} → {inbound.destination}</p>
              <p className="text-gray-500">
                {inbound.departure_time} - {inbound.arrival_time}
              </p>

              <p className="mt-1 font-bold text-green-600">
                ₹{calculateDynamicPrice(inbound)}
              </p>
            </div>
          </div>

          <h3 className="text-xl font-semibold mt-4 mb-2">Select Seat</h3>

          {renderSeats(inbound, inSeat, setInSeat)}
        </div>

        {/* PROCEED BUTTON */}
        {(outSeat && inSeat) ? (
          <Link
            to={`/roundtrip/passenger/${outbound.id}/${outSeat}/${inbound.id}/${inSeat}`}
            className="btn-primary block text-center w-full"
          >
            Continue to Passenger Details
          </Link>
        ) : (
          <p className="text-center text-gray-600">
            Select seats in both flights to continue.
          </p>
        )}

        <ToastContainer />
      </div>
    </PageTransition>
  );
}
