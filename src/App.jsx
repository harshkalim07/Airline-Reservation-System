import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";

import ProtectedRoute from "./components/ProtectedRoute";
import AdminRoute from "./components/AdminRoute";

import Home from "./pages/Home";
import SearchFlights from "./pages/SearchFlights";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import AdminSignup from "./pages/AdminSignup";
import AdminLogin from "./pages/AdminLogin";
import FlightDetails from "./pages/FlightDetails";
import BookingPage from "./pages/BookingPage";
import PaymentPage from "./pages/PaymentPage";
import TicketPage from "./pages/TicketPage";
import BookingHistory from "./pages/BookingHistory";
import CancelBooking from "./pages/CancelBooking";
import BookingSuccess from "./pages/BookingSuccess";
import AdminAddFlight from "./pages/AdminAddFlight";
import AdminFlightsList from "./pages/AdminFlightsList";
import RoundTripBooking from "./pages/RoundTripBooking";
import RoundTripSelect from "./pages/RoundTripSelect"; // ✅ IMPORTANT NEW IMPORT
import RoundTripPassenger from "./pages/RoundTripPassenger";
import RoundTripPayment from "./pages/RoundTripPayment";


export default function App() {
  const { user, logout } = useContext(AuthContext);

  // Active link styling
  const navClass = ({ isActive }) =>
    isActive
      ? "text-blue-300 font-semibold transition"
      : "text-white hover:text-blue-300 transition";

  return (
    <BrowserRouter>

      {/* NAVBAR */}
      <header className="bg-gray-900 text-white shadow-lg sticky top-0 z-20">
        <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-6">

          <NavLink className={navClass} to="/">
            Home
          </NavLink>

          <NavLink className={navClass} to="/search">
            Search
          </NavLink>

          {/* NOT LOGGED IN */}
          {!user && (
            <>
              <NavLink className={navClass} to="/signup">
                Signup
              </NavLink>
              <NavLink className={navClass} to="/login">
                Login
              </NavLink>
              <NavLink className={navClass} to="/admin/signup">
                Admin Signup
              </NavLink>
              <NavLink className={navClass} to="/admin/login">
                Admin Login
              </NavLink>
            </>
          )}

          {/* USER LINKS */}
          {user?.role === "user" && (
            <NavLink className={navClass} to="/bookings">
              My Bookings
            </NavLink>
          )}

          {/* ADMIN LINKS */}
          {user?.role === "admin" && (
            <>
              <NavLink className={navClass} to="/admin/add-flight">
                Add Flight
              </NavLink>
              <NavLink className={navClass} to="/admin/flights">
                Manage Flights
              </NavLink>
            </>
          )}

          {/* RIGHT SIDE USER SECTION */}
          <div className="ml-auto flex items-center gap-3">
            {user ? (
              <>
                <span className="text-sm opacity-80">
                  {user.email} ({user.role})
                </span>

                <button
                  onClick={logout}
                  className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded-lg text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <span className="opacity-75 text-sm">Not Logged In</span>
            )}
          </div>

        </nav>
      </header>

      {/* MAIN PAGE CONTENT */}
      <main className="p-6 max-w-6xl mx-auto">

        <Routes>
          {/* ROUND TRIP */}
          <Route path="/roundtrip/select/:outboundId" element={<RoundTripSelect />} />

          {/* PUBLIC ROUTES */}
          <Route path="/roundtrip/pay/:outId/:outSeat/:inId/:inSeat/:passenger"element={<ProtectedRoute><RoundTripPayment /></ProtectedRoute>}/>
          <Route path="/roundtrip/passenger/:outId/:outSeat/:inId/:inSeat"element={<ProtectedRoute><RoundTripPassenger /></ProtectedRoute>}/>
          <Route  path="/roundtrip/book/:outboundId/:returnId" element={<RoundTripBooking />} />
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<SearchFlights />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin/signup" element={<AdminSignup />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/flight/:id" element={<FlightDetails />} />

          {/* USER PROTECTED ROUTES */}
          <Route
            path="/book/:flightId/:seat"
            element={
              <ProtectedRoute>
                <BookingPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/pay/:flightId/:seat/:passenger"
            element={
              <ProtectedRoute>
                <PaymentPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/ticket/:pnr"
            element={
              <ProtectedRoute>
                <TicketPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/bookings"
            element={
              <ProtectedRoute>
                <BookingHistory />
              </ProtectedRoute>
            }
          />

          <Route
            path="/booking/cancel/:pnr"
            element={
              <ProtectedRoute>
                <CancelBooking />
              </ProtectedRoute>
            }
          />

          <Route path="/booking/success/:pnr" element={<BookingSuccess />} />

          {/* ADMIN PROTECTED */}
          <Route
            path="/admin/add-flight"
            element={
              <AdminRoute>
                <AdminAddFlight />
              </AdminRoute>
            }
          />

          <Route
            path="/admin/flights"
            element={
              <AdminRoute>
                <AdminFlightsList />
              </AdminRoute>
            }
          />
        </Routes>

      </main>

      {/* FOOTER */}
      <footer className="text-center text-gray-500 py-6 mt-10 border-t">
        © {new Date().getFullYear()} Flight Booking Simulator. All Rights Reserved.
      </footer>

    </BrowserRouter>
  );
}
