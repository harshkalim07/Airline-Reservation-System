import { useParams, Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import PageTransition from "../components/PageTransition";
import useToast from "../hooks/useToast";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import { calculateDynamicPrice } from "../utils/dynamicPricing";

export default function RoundTripPayment() {
  const { outId, outSeat, inId, inSeat, passenger } = useParams();
  const { showToast, ToastContainer } = useToast();
  const navigate = useNavigate();

  const [outbound, setOutbound] = useState(null);
  const [inbound, setInbound] = useState(null);

  useEffect(() => {
    const flights = JSON.parse(localStorage.getItem("flights") || "[]");

    setOutbound(flights.find(f => f.id === outId));
    setInbound(flights.find(f => f.id === inId));
  }, [outId, inId]);

  if (!outbound || !inbound) return <div>Loading...</div>;

  const priceOut = calculateDynamicPrice(outbound);
  const priceIn = calculateDynamicPrice(inbound);
  const totalPrice = priceOut + priceIn;

  function generatePNR() {
    return "RT" + Math.random().toString(36).substring(2, 10).toUpperCase();
  }

  function processPayment(status) {
    if (status === "success") {
      const pnr = generatePNR();

      const booking = {
        pnr,
        passenger,
        type: "roundtrip",
        outbound: {
          ...outbound,
          seat: outSeat,
          paid: priceOut,
        },
        inbound: {
          ...inbound,
          seat: inSeat,
          paid: priceIn,
        },
        total: totalPrice,
        date: new Date().toISOString(),
      };

      // save to localStorage
      const history = JSON.parse(localStorage.getItem("bookings") || "[]");
      history.push(booking);
      localStorage.setItem("bookings", JSON.stringify(history));

      // Update seat map
      const flights = JSON.parse(localStorage.getItem("flights") || "[]");

      flights.forEach(f => {
        if (f.id === outbound.id) {
          f.seats = f.seats || {};
          f.seats[outSeat] = "booked";
        }
        if (f.id === inbound.id) {
          f.seats = f.seats || {};
          f.seats[inSeat] = "booked";
        }
      });

      localStorage.setItem("flights", JSON.stringify(flights));

      showToast("Payment Successful!", "success");

      setTimeout(() => {
        navigate(`/ticket/${pnr}`);
      }, 900);
    } else {
      showToast("Payment Failed!", "error");
    }
  }

  function FlightSummary({ flight, seat, title }) {
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
            <p className="mt-1 text-green-600 font-bold">₹{calculateDynamicPrice(flight)}</p>
            <p className="mt-1 text-sm">Seat Selected: <strong>{seat}</strong></p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <div className="max-w-3xl mx-auto">

        {/* Outbound */}
        <FlightSummary
          flight={outbound}
          seat={outSeat}
          title="Outbound Flight"
        />

        {/* Inbound */}
        <FlightSummary
          flight={inbound}
          seat={inSeat}
          title="Return Flight"
        />

        {/* Passenger */}
        <div className="card mb-5">
          <h3 className="text-xl font-semibold mb-1">Passenger</h3>
          <p className="text-gray-700">{passenger}</p>
        </div>

        {/* Total */}
        <div className="card text-center mb-5">
          <h2 className="text-2xl font-bold mb-2">Total Amount</h2>
          <p className="text-green-600 text-3xl font-bold">₹{totalPrice}</p>
        </div>

        {/* Payment Buttons */}
        <div className="flex gap-4">
          <button
            onClick={() => processPayment("success")}
            className="btn-success w-full"
          >
            Pay Now
          </button>

          <button
            onClick={() => processPayment("failed")}
            className="btn-danger w-full"
          >
            Fail Payment
          </button>
        </div>

        <ToastContainer />
      </div>
    </PageTransition>
  );
}
