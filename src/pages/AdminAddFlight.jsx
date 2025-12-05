import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../components/Input";
import useToast from "../hooks/useToast";
import api from "../services/api";

export default function AdminAddFlight() {
  const [form, setForm] = useState({
    airline: "",
    source: "",
    destination: "",
    departure_time: "",
    arrival_time: "",
    price: ""
  });
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { showToast, ToastContainer } = useToast();

  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !form.airline ||
      !form.source ||
      !form.destination ||
      !form.departure_time ||
      !form.arrival_time ||
      !form.price
    ) {
      showToast("Please fill all fields", "error");
      return;
    }

    try {
      setLoading(true);

      // Convert datetime-local to ISO format
      const departureISO = new Date(form.departure_time).toISOString();
      const arrivalISO = new Date(form.arrival_time).toISOString();

      await api.post('/flights', {
        airline: form.airline,
        source: form.source,
        destination: form.destination,
        departure_time: departureISO,
        arrival_time: arrivalISO,
        price: parseFloat(form.price)
      });

      showToast("Flight added successfully!", "success");

      setTimeout(() => {
        navigate('/admin/flights');
      }, 1000);

    } catch (error) {
      console.error('Add flight error:', error);
      showToast(
        error.response?.data?.error || "Failed to add flight",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto card">
      <h2 className="text-2xl font-bold mb-4 text-center">Add New Flight</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Airline" 
          value={form.airline} 
          onChange={v => setForm({ ...form, airline: v })}
          disabled={loading}
        />
        <Input 
          label="Source" 
          value={form.source} 
          onChange={v => setForm({ ...form, source: v })}
          disabled={loading}
        />
        <Input 
          label="Destination" 
          value={form.destination} 
          onChange={v => setForm({ ...form, destination: v })}
          disabled={loading}
        />
        <Input 
          type="datetime-local" 
          label="Departure Time" 
          value={form.departure_time} 
          onChange={v => setForm({ ...form, departure_time: v })}
          disabled={loading}
        />
        <Input 
          type="datetime-local" 
          label="Arrival Time" 
          value={form.arrival_time} 
          onChange={v => setForm({ ...form, arrival_time: v })}
          disabled={loading}
        />
        <Input 
          label="Base Price" 
          type="number" 
          value={form.price} 
          onChange={v => setForm({ ...form, price: v })}
          disabled={loading}
        />

        <button 
          className="btn-primary w-full mt-3"
          disabled={loading}
        >
          {loading ? 'Adding...' : 'Add Flight'}
        </button>
      </form>

      <ToastContainer />
    </div>
  );
}