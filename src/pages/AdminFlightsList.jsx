import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import useToast from "../hooks/useToast";
import api from "../services/api";

export default function AdminFlightsList() {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);

  const { showToast, ToastContainer } = useToast();

  useEffect(() => {
    fetchFlights();
  }, []);

  async function fetchFlights() {
    try {
      setLoading(true);
      const response = await api.get('/flights');
      setFlights(response.data.flights || []);
    } catch (error) {
      console.error('Fetch flights error:', error);
      showToast("Failed to load flights", "error");
    } finally {
      setLoading(false);
    }
  }

  async function deleteFlight(flightId) {
    if (!confirm(`Are you sure you want to delete flight ${flightId}?`)) {
      return;
    }

    try {
      await api.delete(`/flights/${flightId}`);
      showToast("Flight deleted", "success");
      fetchFlights();
    } catch (error) {
      console.error('Delete flight error:', error);
      showToast(
        error.response?.data?.error || "Failed to delete flight",
        "error"
      );
    }
  }

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto card">
        <p className="text-center">Loading flights...</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto card">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Manage Flights</h2>
        <Link to="/admin/add-flight" className="btn-primary">
          Add New Flight
        </Link>
      </div>

      {flights.length === 0 ? (
        <p>No flights available.</p>
      ) : (
        <ul className="space-y-4">
          {flights.map(f => (
            <li key={f.flight_id} className="p-4 bg-gray-100 rounded-lg shadow-sm">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-semibold">{f.airline} ({f.flight_id})</h3>
                  <p>{f.source} → {f.destination}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    Dep: {new Date(f.departure_time).toLocaleString()} <br />
                    Arr: {new Date(f.arrival_time).toLocaleString()}
                  </p>
                  <p className="text-sm font-medium mt-1">Price: ₹{f.price}</p>
                </div>
                <button
                  className="btn-danger"
                  onClick={() => deleteFlight(f.flight_id)}
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