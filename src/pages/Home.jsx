import PageTransition from "../components/PageTransition";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <PageTransition>
      {/* HERO SECTION */}
      <section className="relative w-full h-[60vh] rounded-2xl overflow-hidden shadow-lg">

        {/* Background Image */}
        <img
          src="https://images.unsplash.com/photo-1529074963764-98f45c47344b?auto=format&fit=crop&w=1600&q=80"
          className="w-full h-full object-cover"
        />

        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>

        {/* Hero Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center text-white px-6">
          <h1 className="text-5xl font-extrabold mb-4 tracking-tight">
            Fly Smarter. Book Faster.
          </h1>

          <p className="text-lg text-gray-200 max-w-xl">
            Search and book flights instantly with a realistic airline-style booking experience.
          </p>

          <Link
            to="/search"
            className="mt-6 px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-lg font-semibold shadow-lg transition"
          >
            Search Flights
          </Link>
        </div>
      </section>

      {/* SERVICES / FEATURE GRID */}
      <section className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">

        {/* Card 1 */}
        <div className="card flex items-start gap-4">
          <div className="text-blue-600 text-3xl">✈️</div>
          <div>
            <h3 className="text-xl font-bold mb-1">Realistic Booking Flow</h3>
            <p className="text-gray-600 text-sm">
              Simulated airline-style seat selection, booking, payment, and ticket generation.
            </p>
          </div>
        </div>

        {/* Card 2 */}
        <div className="card flex items-start gap-4">
          <div className="text-green-600 text-3xl">💺</div>
          <div>
            <h3 className="text-xl font-bold mb-1">Smart Seat Layout</h3>
            <p className="text-gray-600 text-sm">
              30-seat layout with availability, selection glow, and booking lock system.
            </p>
          </div>
        </div>

        {/* Card 3 */}
        <div className="card flex items-start gap-4">
          <div className="text-yellow-500 text-3xl">💳</div>
          <div>
            <h3 className="text-xl font-bold mb-1">Secure Payment Simulation</h3>
            <p className="text-gray-600 text-sm">
              Fake payment system with success/failure logic to mimic real-world workflows.
            </p>
          </div>
        </div>

      </section>

      {/* FOOTER */}
      <footer className="text-center text-gray-500 py-10 mt-16">
        © {new Date().getFullYear()} Flight Booking Simulator  
      </footer>
    </PageTransition>
  );
}
