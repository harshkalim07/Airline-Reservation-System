// src/components/BoardingPass.jsx
import { useEffect, useRef } from "react";
import { QRCodeSVG } from "qrcode.react";
import JsBarcode from "jsbarcode";
import { getAirlineLogo } from "../utils/getAirlineLogo";
import { getSeatClass, getSeatClassColor } from "../utils/seatClass";

export default function BoardingPass({ ticket, compact = false }) {
  const barcodeRef = useRef(null);

  const pnr = ticket.pnr || "UNKNOWN-PNR";
  const passenger = ticket.passenger || "Passenger";
  const isRoundTrip = ticket.type === "roundtrip";

  // Pick primary flight
  const primary =
    isRoundTrip
      ? ticket.outbound
      : ticket.flight || {
          airline: ticket.airline || "Unknown",
          source: ticket.source || "",
          destination: ticket.destination || "",
          departure_time: ticket.departure_time || "",
          arrival_time: ticket.arrival_time || "",
          paid: ticket.paid || ticket.total || 0,
          seat: ticket.seat,
        };

  const secondary = isRoundTrip ? ticket.inbound : null;

  // Generate barcode
  useEffect(() => {
    if (!barcodeRef.current) return;
    try {
      JsBarcode(barcodeRef.current, pnr, {
        format: "CODE128",
        displayValue: false,
        height: 42,
        width: 1.8,
        margin: 0,
      });
    } catch (e) {}
  }, [pnr]);

  const seatClass =
    (primary && primary.seatClass) || getSeatClass(Number(primary.seat || 0));

  const classColor = getSeatClassColor(seatClass);

  return (
    <div
      className={`w-full max-w-4xl mx-auto rounded-xl shadow-lg overflow-hidden bg-white text-gray-900 ${
        compact ? "text-sm" : "text-base"
      }`}
    >
      <div className="flex">
        {/* LEFT SIDE */}
        <div className="flex-1 p-6">

          {/* Airline header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <img
                src={getAirlineLogo(primary.airline)}
                alt={primary.airline}
                className="w-20 h-12 object-contain"
                onError={(e) => (e.target.style.display = "none")}
              />
              <div>
                <div className="font-semibold text-lg">{primary.airline}</div>
                <div className="text-sm text-gray-500">
                  {primary.source} → {primary.destination}
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="text-xs text-gray-400">PNR</div>
              <div className="font-bold text-xl text-blue-600">{pnr}</div>
            </div>
          </div>

          {/* Times */}
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div>
              <div className="text-xs text-gray-400">DEPART</div>
              <div className="text-lg font-semibold">
                {formatDateTime(primary.departure_time)}
              </div>
              <div className="text-sm text-gray-600">{primary.source}</div>
            </div>

            <div>
              <div className="text-xs text-gray-400">ARRIVE</div>
              <div className="text-lg font-semibold">
                {formatDateTime(primary.arrival_time)}
              </div>
              <div className="text-sm text-gray-600">{primary.destination}</div>
            </div>
          </div>

          {/* Passenger + seat */}
          <div className="mt-6 flex items-center gap-6">
            <div>
              <div className="text-xs text-gray-400">Passenger</div>
              <div className="font-semibold">{passenger}</div>
            </div>

            <div>
              <div className="text-xs text-gray-400">Seat</div>
              <div className="font-semibold">{primary.seat}</div>
            </div>

            <div>
              <div className="text-xs text-gray-400">Class</div>
              <div
                className="inline-block px-2 py-1 rounded text-white text-xs"
                style={{
                  background: classColorToHex(classColor),
                }}
              >
                {seatClass}
              </div>
            </div>

            <div className="ml-auto text-right">
              <div className="text-xs text-gray-400">Total Paid</div>
              <div className="font-semibold text-lg text-green-600">
                ₹{ticket.total ?? primary.paid}
              </div>
            </div>
          </div>

          {/* Barcode */}
          <div className="mt-6">
            <svg ref={barcodeRef} />
          </div>
        </div>

        {/* RIGHT SIDE STUB */}
        <div className="w-56 bg-gray-50 p-4 flex flex-col items-center justify-between border-l">
          <div className="text-center">
            <div className="text-xs text-gray-500">BOARDING</div>
            <div className="font-semibold text-lg my-2">
              {primary.source} → {primary.destination}
            </div>

            <div className="text-xs text-gray-600 text-left">
              <div>
                <strong>Flight:</strong> {primary.flightNumber || primary.id}
              </div>
              <div>
                <strong>Seat:</strong> {primary.seat}
              </div>
              <div>
                <strong>PNR:</strong> {pnr}
              </div>
            </div>
          </div>

          <div className="mt-4">
            <QRCodeSVG 
             value={`http://172.18.109.12:5173/ticket/${pnr}?public=true`}
             size={120} 
             level="H"
             />
          </div>

          <div className="text-xs text-gray-400 mt-4">
            Scan this QR/Barcode at boarding
          </div>
        </div>
      </div>

      {/* Return Flight Section */}
      {isRoundTrip && secondary && (
        <div className="p-4 border-t bg-gray-50">
          <div className="flex items-center gap-4">
            <img
              src={getAirlineLogo(secondary.airline)}
              alt={secondary.airline}
              className="w-16 h-10 object-contain"
              onError={(e) => (e.target.style.display = "none")}
            />

            <div>
              <div className="font-semibold">{secondary.airline} — Return</div>
              <div className="text-sm text-gray-600">
                {secondary.source} → {secondary.destination}
              </div>
            </div>

            <div className="ml-auto text-right">
              <div className="text-xs text-gray-400">Seat</div>
              <div className="font-semibold">{secondary.seat}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* HELPERS */

function formatDateTime(dt) {
  if (!dt) return "";
  try {
    const d = new Date(dt);
    return d.toLocaleString(undefined, {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return dt;
  }
}

function classColorToHex(tw) {
  if (!tw) return "#6b7280";
  if (tw.includes("yellow")) return "#f59e0b";
  if (tw.includes("blue")) return "#2563eb";
  if (tw.includes("gray")) return "#d1d5db";
  return "#2563eb";
}