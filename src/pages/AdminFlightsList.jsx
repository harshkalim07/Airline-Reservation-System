import { useEffect, useState } from "react";
import useToast from "../hooks/useToast";

export default function AdminFlightsList() {
  const [flights, setFlights] = useState([]);

  const { showToast, ToastContainer } = useToast();

  useEffect(() => {
    const allFlights = JSON.parse(localStorage.getItem("flights") || "[]");
    setFlights(allFlights);
  }, []);

  function deleteFlight(id) {
    const updated = flights.filter(f => f.id !== id);
    localStorage.setItem("flights", JSON.stringify(updated));
    setFlights(updated);

    showToast("Flight deleted", "success");
  }

  return (
    <div className="max-w-3xl mx-auto card">
      <h2 className="text-2xl font-bold mb-4">Manage Flights</h2>

      {flights.length === 0 ? (
        <p>No flights available.</p>
      ) : (
        <ul className="space-y-4">
          {flights.map(f => (
            <li key={f.id} className="p-4 bg-gray-100 rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold">{f.airline}</h3>

              <p>{f.source} → {f.destination}</p>

              <p className="text-sm text-gray-600 mt-1">
                Dep: {f.departure_time} <br />
                Arr: {f.arrival_time}
              </p>

              <div className="mt-3 flex gap-3">
                <button
                  className="btn-danger flex-1"
                  onClick={() => deleteFlight(f.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      <ToastContainer />
    </div>
  );
}
