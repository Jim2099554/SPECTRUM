// Tabla básica de LADA (códigos de área) de México con coordenadas aproximadas (ciudad principal)
// Puedes ampliar esta lista según necesidad
export interface LadaInfo {
  lada: string;
  ciudad: string;
  estado: string;
  lat: number;
  lng: number;
}

export const LADAS: LadaInfo[] = [
  // Ciudad de México y área metropolitana
  { lada: '55', ciudad: 'Ciudad de México', estado: 'CDMX', lat: 19.432608, lng: -99.133209 },
  { lada: '56', ciudad: 'Ciudad de México', estado: 'CDMX', lat: 19.432608, lng: -99.133209 },
  
  // Jalisco
  { lada: '33', ciudad: 'Guadalajara', estado: 'Jalisco', lat: 20.659698, lng: -103.349609 },
  { lada: '376', ciudad: 'Puerto Vallarta', estado: 'Jalisco', lat: 20.653407, lng: -105.225113 },
  
  // Nuevo León
  { lada: '81', ciudad: 'Monterrey', estado: 'Nuevo León', lat: 25.686614, lng: -100.316116 },
  
  // Guerrero
  { lada: '744', ciudad: 'Acapulco', estado: 'Guerrero', lat: 16.853109, lng: -99.823653 },
  { lada: '762', ciudad: 'Chilpancingo', estado: 'Guerrero', lat: 17.550819, lng: -99.500441 },
  
  // Puebla
  { lada: '222', ciudad: 'Puebla', estado: 'Puebla', lat: 19.041297, lng: -98.2062 },
  
  // Yucatán
  { lada: '999', ciudad: 'Mérida', estado: 'Yucatán', lat: 20.96737, lng: -89.592585 },
  
  // Querétaro
  { lada: '442', ciudad: 'Querétaro', estado: 'Querétaro', lat: 20.588793, lng: -100.389888 },
  
  // Guanajuato
  { lada: '477', ciudad: 'León', estado: 'Guanajuato', lat: 21.122119, lng: -101.68406 },
  { lada: '473', ciudad: 'Guanajuato', estado: 'Guanajuato', lat: 21.017654, lng: -101.257066 },
  { lada: '462', ciudad: 'Irapuato', estado: 'Guanajuato', lat: 20.674143, lng: -101.356415 },
  
  // Veracruz
  { lada: '229', ciudad: 'Veracruz', estado: 'Veracruz', lat: 19.173773, lng: -96.134224 },
  { lada: '228', ciudad: 'Xalapa', estado: 'Veracruz', lat: 19.544180, lng: -96.910012 },
  
  // Chiapas
  { lada: '961', ciudad: 'Tuxtla Gutiérrez', estado: 'Chiapas', lat: 16.751914, lng: -93.113751 },
  
  // Oaxaca
  { lada: '951', ciudad: 'Oaxaca', estado: 'Oaxaca', lat: 17.073184, lng: -96.726608 },
  
  // Baja California
  { lada: '664', ciudad: 'Tijuana', estado: 'Baja California', lat: 32.514948, lng: -117.038208 },
  { lada: '686', ciudad: 'Mexicali', estado: 'Baja California', lat: 32.624630, lng: -115.452778 },
  
  // Baja California Sur
  { lada: '612', ciudad: 'La Paz', estado: 'Baja California Sur', lat: 24.142220, lng: -110.312738 },
  { lada: '624', ciudad: 'Cabo San Lucas', estado: 'Baja California Sur', lat: 22.890533, lng: -109.916737 },
  
  // Sonora
  { lada: '662', ciudad: 'Hermosillo', estado: 'Sonora', lat: 29.072967, lng: -110.955919 },
  
  // Chihuahua
  { lada: '614', ciudad: 'Chihuahua', estado: 'Chihuahua', lat: 28.632996, lng: -106.069103 },
  { lada: '656', ciudad: 'Ciudad Juárez', estado: 'Chihuahua', lat: 31.693680, lng: -106.424547 },
  
  // Coahuila
  { lada: '844', ciudad: 'Saltillo', estado: 'Coahuila', lat: 25.423889, lng: -100.995556 },
  { lada: '871', ciudad: 'Torreón', estado: 'Coahuila', lat: 25.542321, lng: -103.406189 },
  
  // Durango
  { lada: '618', ciudad: 'Durango', estado: 'Durango', lat: 24.027730, lng: -104.653100 },
  
  // Sinaloa
  { lada: '667', ciudad: 'Culiacán', estado: 'Sinaloa', lat: 24.809065, lng: -107.394012 },
  { lada: '669', ciudad: 'Mazatlán', estado: 'Sinaloa', lat: 23.249415, lng: -106.411142 },
  
  // Nayarit
  { lada: '311', ciudad: 'Tepic', estado: 'Nayarit', lat: 21.504200, lng: -104.894500 },
  
  // Aguascalientes
  { lada: '449', ciudad: 'Aguascalientes', estado: 'Aguascalientes', lat: 21.880487, lng: -102.296706 },
  
  // Zacatecas
  { lada: '492', ciudad: 'Zacatecas', estado: 'Zacatecas', lat: 22.770850, lng: -102.583190 },
  
  // San Luis Potosí
  { lada: '444', ciudad: 'San Luis Potosí', estado: 'San Luis Potosí', lat: 22.156471, lng: -100.985504 },
  
  // Tamaulipas
  { lada: '834', ciudad: 'Tampico', estado: 'Tamaulipas', lat: 22.233053, lng: -97.861099 },
  { lada: '899', ciudad: 'Reynosa', estado: 'Tamaulipas', lat: 26.080890, lng: -98.297730 },
  
  // Michoacán
  { lada: '443', ciudad: 'Morelia', estado: 'Michoacán', lat: 19.706200, lng: -101.195300 },
  
  // Colima
  { lada: '312', ciudad: 'Colima', estado: 'Colima', lat: 19.245200, lng: -103.725100 },
  
  // Estado de México
  { lada: '722', ciudad: 'Toluca', estado: 'Estado de México', lat: 19.282800, lng: -99.655700 },
  
  // Morelos
  { lada: '777', ciudad: 'Cuernavaca', estado: 'Morelos', lat: 18.921400, lng: -99.234100 },
  
  // Hidalgo
  { lada: '771', ciudad: 'Pachuca', estado: 'Hidalgo', lat: 20.120900, lng: -98.732900 },
  
  // Tlaxcala
  { lada: '246', ciudad: 'Tlaxcala', estado: 'Tlaxcala', lat: 19.318154, lng: -98.237392 },
  
  // Tabasco
  { lada: '993', ciudad: 'Villahermosa', estado: 'Tabasco', lat: 17.989557, lng: -92.947472 },
  
  // Campeche
  { lada: '981', ciudad: 'Campeche', estado: 'Campeche', lat: 19.830492, lng: -90.534914 },
  
  // Quintana Roo
  { lada: '998', ciudad: 'Cancún', estado: 'Quintana Roo', lat: 21.161908, lng: -86.851528 },
  { lada: '984', ciudad: 'Playa del Carmen', estado: 'Quintana Roo', lat: 20.627728, lng: -87.079384 },
];

// Códigos de país internacionales con coordenadas de capitales
interface CountryInfo {
  code: string;
  country: string;
  capital: string;
  lat: number;
  lng: number;
}

const COUNTRY_CODES: CountryInfo[] = [
  { code: '1', country: 'USA/Canadá', capital: 'Washington DC', lat: 38.9072, lng: -77.0369 },
  { code: '52', country: 'México', capital: 'Ciudad de México', lat: 19.432608, lng: -99.133209 },
  { code: '34', country: 'España', capital: 'Madrid', lat: 40.4168, lng: -3.7038 },
  { code: '44', country: 'Reino Unido', capital: 'Londres', lat: 51.5074, lng: -0.1278 },
  { code: '33', country: 'Francia', capital: 'París', lat: 48.8566, lng: 2.3522 },
  { code: '49', country: 'Alemania', capital: 'Berlín', lat: 52.5200, lng: 13.4050 },
  { code: '39', country: 'Italia', capital: 'Roma', lat: 41.9028, lng: 12.4964 },
  { code: '55', country: 'Brasil', capital: 'Brasilia', lat: -15.8267, lng: -47.9218 },
  { code: '54', country: 'Argentina', capital: 'Buenos Aires', lat: -34.6037, lng: -58.3816 },
  { code: '56', country: 'Chile', capital: 'Santiago', lat: -33.4489, lng: -70.6693 },
  { code: '57', country: 'Colombia', capital: 'Bogotá', lat: 4.7110, lng: -74.0721 },
  { code: '51', country: 'Perú', capital: 'Lima', lat: -12.0464, lng: -77.0428 },
  { code: '58', country: 'Venezuela', capital: 'Caracas', lat: 10.4806, lng: -66.9036 },
  { code: '86', country: 'China', capital: 'Beijing', lat: 39.9042, lng: 116.4074 },
  { code: '81', country: 'Japón', capital: 'Tokio', lat: 35.6762, lng: 139.6503 },
  { code: '82', country: 'Corea del Sur', capital: 'Seúl', lat: 37.5665, lng: 126.9780 },
  { code: '91', country: 'India', capital: 'Nueva Delhi', lat: 28.6139, lng: 77.2090 },
];

export function getLadaInfo(numero: string): LadaInfo | null {
  // Limpiar el número (quitar espacios, guiones, paréntesis)
  const cleanNumber = numero.replace(/[\s\-\(\)]/g, '');
  
  // Intentar buscar LADA mexicana (ordenar por longitud descendente para buscar las más largas primero)
  const sortedLadas = [...LADAS].sort((a, b) => b.lada.length - a.lada.length);
  const ladaMatch = sortedLadas.find(l => cleanNumber.startsWith(l.lada));
  
  if (ladaMatch) {
    return ladaMatch;
  }
  
  // Si no es LADA mexicana, intentar detectar código de país internacional
  // Buscar si empieza con + o 00 (formato internacional)
  let numberToCheck = cleanNumber;
  if (cleanNumber.startsWith('+')) {
    numberToCheck = cleanNumber.substring(1);
  } else if (cleanNumber.startsWith('00')) {
    numberToCheck = cleanNumber.substring(2);
  }
  
  // Buscar código de país (ordenar por longitud descendente)
  const sortedCountries = [...COUNTRY_CODES].sort((a, b) => b.code.length - a.code.length);
  const countryMatch = sortedCountries.find(c => numberToCheck.startsWith(c.code));
  
  if (countryMatch) {
    // Convertir CountryInfo a LadaInfo para compatibilidad
    return {
      lada: countryMatch.code,
      ciudad: countryMatch.capital,
      estado: countryMatch.country,
      lat: countryMatch.lat,
      lng: countryMatch.lng
    };
  }
  
  return null;
}
