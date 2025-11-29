export function getSeatClass(seatNumber) {
  seatNumber = Number(seatNumber);

  if (seatNumber >= 1 && seatNumber <= 6) return "Business";
  if (seatNumber >= 7 && seatNumber <= 14) return "Premium Economy";
  return "Economy";
}

export function getSeatClassColor(cls) {
  switch (cls) {
    case "Business":
      return "bg-yellow-500 hover:bg-yellow-600 text-white";

    case "Premium Economy":
      return "bg-blue-600 hover:bg-blue-700 text-white";

    case "Economy":
    default:
      return "bg-gray-200 hover:bg-gray-300";
  }
}

export function seatPriceMultiplier(cls) {
  switch (cls) {
    case "Business": return 1.8;
    case "Premium Economy": return 1.4;
    default: return 1.0;
  }
}
