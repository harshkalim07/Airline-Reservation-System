import { useState } from "react";
import Input from "../components/Input";
import useToast from "../hooks/useToast";

export default function AdminAddFlight() {
  const [form, setForm] = useState({
    airline: "",
    source: "",
    destination: "",
    departure_time: "",
    arrival_time: "",
    price: ""
  });

  const { showToast, ToastContainer } = useToast();

  function handleSubmit(e) {
    e.preventDefault();

    // Validation
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

    const flights = JSON.parse(localStorage.getItem("flights") || "[]");

    const newFlight = {
      id: "FL" + Math.floor(Math.random() * 999999),
      ...form,
      seats: {}, // empty seat map
    };

    flights.push(newFlight);
    localStorage.setItem("flights", JSON.stringify(flights));

    showToast("Flight added successfully!", "success");

    setForm({
      airline: "",
      source: "",
      destination: "",
      departure_time: "",
      arrival_time: "",
      price: "",
    });
  }

  return (
    <div className="max-w-xl mx-auto card">
      <h2 className="text-2xl font-bold mb-4 text-center">Add New Flight</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Airline" value={form.airline} onChange={v => setForm({ ...form, airline: v })} />
        <Input label="Source" value={form.source} onChange={v => setForm({ ...form, source: v })} />
        <Input label="Destination" value={form.destination} onChange={v => setForm({ ...form, destination: v })} />

        <Input type="datetime-local" label="Departure Time" value={form.departure_time} onChange={v => setForm({ ...form, departure_time: v })} />

        <Input type="datetime-local" label="Arrival Time" value={form.arrival_time} onChange={v => setForm({ ...form, arrival_time: v })} />

        <Input label="Base Price" type="number" value={form.price} onChange={v => setForm({ ...form, price: v })} />

        <button className="btn-primary w-full mt-3">Add Flight</button>
      </form>

      <ToastContainer />
    </div>
  );
}
