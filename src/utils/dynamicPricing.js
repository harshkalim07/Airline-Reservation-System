export function calculateDynamicPrice(flight) {
  const basePrice = Number(flight.price || 0);
  let price = basePrice;

  const seats = flight.seats || {};
  const totalSeats = Object.keys(seats).length || 6;
  const bookedSeats = Object.values(seats).filter((s) => s.status === "booked").length;
  const remainingPercent = ((totalSeats - bookedSeats) / totalSeats) * 100;

  if (remainingPercent < 50) price += basePrice * 0.2;
  if (remainingPercent < 20) price += basePrice * 0.35;

  const now = new Date();
  const departure = new Date(flight.departure_time);
  const diffHours = (departure - now) / (1000 * 60 * 60);

  if (diffHours < 48) price += basePrice * 0.15;
  if (diffHours < 24) price += basePrice * 0.30;

  const demandFactor = Math.random();
  if (demandFactor > 0.8) price += basePrice * 0.10;

  return Math.round(price);
}
