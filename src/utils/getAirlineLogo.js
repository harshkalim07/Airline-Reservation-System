const airlineLogos = {
  indigo: "https://upload.wikimedia.org/wikipedia/commons/8/89/IndiGo_logo.svg",
  "air india": "https://upload.wikimedia.org/wikipedia/en/6/6d/Air_India_Logo.svg",
  vistara: "https://upload.wikimedia.org/wikipedia/en/0/0d/Vistara_logo.svg",
  spicejet: "https://upload.wikimedia.org/wikipedia/en/7/74/SpiceJet_Logo.svg",
  akasa: "https://upload.wikimedia.org/wikipedia/commons/6/65/Akasa_Air_logo.svg",
  gofirst: "https://upload.wikimedia.org/wikipedia/en/2/27/Go_First_logo.svg",
  airasia: "https://upload.wikimedia.org/wikipedia/commons/8/89/AirAsia_New_Logo.svg",

  emirates: "https://upload.wikimedia.org/wikipedia/commons/b/b0/Emirates_logo.svg",
  qatar: "https://upload.wikimedia.org/wikipedia/en/5/5e/Qatar_Airways_Logo.svg",
  etihad: "https://upload.wikimedia.org/wikipedia/commons/5/5b/Etihad_Airways_logo_%282019%29.svg",
  lufthansa: "https://upload.wikimedia.org/wikipedia/commons/4/44/Lufthansa_Logo_2018.svg",
  british: "https://upload.wikimedia.org/wikipedia/en/d/d1/British_Airways_Logo.svg",
  delta: "https://upload.wikimedia.org/wikipedia/commons/0/06/Delta_Air_Lines_logo.svg",
  united: "https://upload.wikimedia.org/wikipedia/commons/d/d1/United_Airlines_logo.svg",
};

export function getAirlineLogo(airline) {
  if (!airline) return null;

  const name = airline.toLowerCase().trim();

  // Exact match
  if (airlineLogos[name]) return airlineLogos[name];

  // Partial match (e.g., "Air India Express")
  const match = Object.keys(airlineLogos).find(key => name.includes(key));
  if (match) return airlineLogos[match];

  // Fallback — generic airplane icon
  return "https://cdn-icons-png.flaticon.com/512/34/34627.png";
}
