import React from "react";
import { getSeatClass, getSeatClassColor, seatPriceMultiplier } from "../utils/seatClass";

export default function AnimatedSeatMap({
  rows = 10,
  seatsMap = {},
  basePrice = 5000,
  selected = null,
  onSelect = () => {},
  className = "",
}) {
  const seatCols = ["A", "B", "C", "D", "E", "F"];

  function renderSeatLabel(row, col) {
    return `${row}${col}`;      // visual label
  }

  function numericSeat(label) {
    return label.replace(/\D/g, "");   // backend expects numeric only
  }

  function seatState(label) {
    const num = numericSeat(label);
    return seatsMap[num] === "booked" ? "booked" : "available";
  }

  function seatClassLabel(seatIndex) {
    return getSeatClass(seatIndex);
  }

  function priceForSeat(seatIndex) {
    const cls = seatClassLabel(seatIndex);
    const mul = seatPriceMultiplier(cls);
    return Math.round(basePrice * mul);
  }

  return (
    <div className={`space-y-3 ${className}`}>
      
      {/* Legend */}
      <div className="flex gap-4 items-center text-sm">
        <LegendItem colorClass="bg-yellow-500" label="Business" />
        <LegendItem colorClass="bg-blue-600" label="Premium Economy" />
        <LegendItem colorClass="bg-gray-200 border" label="Economy" />
        <div className="ml-auto text-xs text-gray-500">Hover to see price</div>
      </div>

      {/* Seat Map */}
      <div className="w-full overflow-x-auto">
        <div className="inline-block">
          
          {Array.from({ length: rows }).map((_, r) => {
            const rowNum = r + 1;

            return (
              <div key={rowNum} className="flex items-center gap-3 mb-2">

                <div className="w-8 text-sm text-gray-600">{rowNum}</div>

                {/* Left ABC */}
                <div className="flex gap-2">
                  {seatCols.slice(0, 3).map((col, ci) => {
                    const seatIndex = r * 6 + (ci + 1);
                    const label = renderSeatLabel(rowNum, col);
                    const numSeat = numericSeat(label);
                    const state = seatState(label);
                    const cls = seatClassLabel(seatIndex);
                    const colorClass = getSeatClassColor(cls);
                    const isSelected = selected === label;

                    return (
                      <SeatButton
                        key={label}
                        label={label}
                        numeric={numSeat}
                        state={state}
                        colorClass={colorClass}
                        isSelected={isSelected}
                        price={priceForSeat(seatIndex)}
                        onClick={() => state === "available" && onSelect(label)}
                      />
                    );
                  })}
                </div>

                {/* Aisle */}
                <div className="w-8">
                  <div className="h-6 border-l border-dashed border-gray-300 ml-2" />
                </div>

                {/* DEF */}
                <div className="flex gap-2">
                  {seatCols.slice(3, 6).map((col, ci) => {
                    const seatIndex = r * 6 + (3 + ci + 1);
                    const label = renderSeatLabel(rowNum, col);
                    const numSeat = numericSeat(label);
                    const state = seatState(label);
                    const cls = seatClassLabel(seatIndex);
                    const colorClass = getSeatClassColor(cls);
                    const isSelected = selected === label;

                    return (
                      <SeatButton
                        key={label}
                        label={label}
                        numeric={numSeat}
                        state={state}
                        colorClass={colorClass}
                        isSelected={isSelected}
                        price={priceForSeat(seatIndex)}
                        onClick={() => state === "available" && onSelect(label)}
                      />
                    );
                  })}
                </div>

              </div>
            );
          })}

        </div>
      </div>
    </div>
  );
}

function LegendItem({ colorClass, label }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`w-4 h-4 rounded ${colorClass} border`}></span>
      <span className="text-sm">{label}</span>
    </div>
  );
}

function SeatButton({ label, numeric, state, colorClass, isSelected, onClick, price }) {
  const booked = state === "booked";

  const baseClasses =
    "w-12 h-10 flex flex-col items-center justify-center rounded-lg text-xs transition transform";

  const bookedClasses = "bg-red-600 text-white opacity-80 cursor-not-allowed scale-100";
  const selectedClasses = "bg-green-600 text-white scale-105 shadow-lg";
  const availableClasses = `${colorClass} text-black hover:scale-105 cursor-pointer`;

  return (
    <button
      type="button"
      title={booked ? `${label} — Booked` : `${label} — ₹${price}`}
      onClick={onClick}
      disabled={booked}
      className={`${baseClasses} ${booked ? bookedClasses : isSelected ? selectedClasses : availableClasses}`}
      style={{ transitionDuration: "160ms" }}
    >
      <div className="text-xs font-medium">{label}</div>
      <div className="text-[10px] opacity-75">{booked ? "X" : ""}</div>
    </button>
  );
}
