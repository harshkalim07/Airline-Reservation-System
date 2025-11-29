import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import PageTransition from "../components/PageTransition";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import { calculateDynamicPrice } from "../utils/dynamicPricing";

export default function RoundTripSelect() {
  const { outboundId } = useParams();
  const [outbound, setOutbound] = useState(null);
  const [returnFlights, setReturnFlights] = useState([]);
  const [selectedReturn, setSelectedReturn] = useState(null);

  useEffect(() => {
    const flights = JSON.parse(localStorage.getItem("flights") || "[]");

    const ob = flights.find(f => f.id === outboundId);
    setOutbound(ob);

    // Return flights: reverse direction
    const inbound = flights.filter(
      f =>
        f.source.toLowerCase() === ob.destination.toLowerCase() &&
        f.destination.toLowerCase() === ob.source.toLowerCase()
    );

    setReturnFlights(inbound);
  }, [outboundId]);

  if (!outbound) return <div>Loading...</div>;

  return (
    <PageTransition>
      <div className="max-w-3xl mx-auto">

        {/* OUTBOUND SECTION */}
        <div className="card mb-8">
          <h2 className="text-2xl font-bold mb-3">Selected Outbound Flight</h2>

          <div className="flex items-center gap-4">
            <img
              src={getAirlineLogo(outbound.airline)}
              className="w-16 h-16 object-contain"
            />
            <div>
              <p className="font-bold">{outbound.airline}</p>
              <p>{outbound.source} → {outbound.destination}</p>
              <p className="text-gray-500 text-sm">
                {outbound.departure_time} - {outbound.arrival_time}
              </p>
              <p className="text-green-600 font-bold mt-1">₹{calculateDynamicPrice(outbound)}</p>
            </div>
          </div>
        </div>

        {/* RETURN SELECTION */}
        <h2 className="text-2xl font-bold mb-4">Choose Return Flight</h2>

        <div className="space-y-5">
          {returnFlights.map(f => {
            const price = calculateDynamicPrice(f);
            const isSelected = selectedReturn?.id === f.id;

            return (
              <div
                key={f.id}
                onClick={() => setSelectedReturn(f)}
                className={`card cursor-pointer transition border-2 
                  ${isSelected ? "border-blue-600 shadow-lg" : "border-transparent"}`}
              >
                <div className="flex items-center gap-6">
                  <img
                    src={getAirlineLogo(f.airline)}
                    className="w-16 h-16 object-contain"
                  />

                  <div className="flex-1">
                    <h3 className="text-xl font-bold">{f.airline}</h3>
                    <p className="text-gray-600">{f.source} → {f.destination}</p>
                    <p className="text-sm text-gray-500">
                      {f.departure_time} - {f.arrival_time}
                    </p>
                    <p className="mt-2 text-lg font-bold text-green-600">₹{price}</p>
                  </div>

                  {isSelected && (
                    <span className="text-blue-600 font-semibold">Selected ✓</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* PROCEED BUTTON */}
        {selectedReturn && (
          <Link
            to={`/roundtrip/book/${outbound.id}/${selectedReturn.id}`}
            className="btn-primary w-full block text-center mt-6"
          >
            Continue to Passenger Details
          </Link>
        )}

      </div>
    </PageTransition>
  );
}
