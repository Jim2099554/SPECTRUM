import { worldMill } from "@react-jvectormap/world";
import { VectorMap } from "@react-jvectormap/core";
import React, { useMemo } from "react";

interface Marker {
  latLng: [number, number];
  name: string;
  style?: any;
}

interface CountryMapProps {
  markers?: Marker[];
}

// Coordenadas de México
// const MEXICO_BOUNDS = {
//   minLat: 14.5,
//   maxLat: 32.7,
//   minLng: -118.4,
//   maxLng: -86.7
// };

const CountryMap: React.FC<CountryMapProps> = ({ markers = [] }) => {
  // Configuración fija para centrar México perfectamente
  // Estos valores han sido probados y funcionan correctamente
  const focusConfig = useMemo(() => {
    // Siempre centrar en México
    // Valores ajustados para jVectorMap
    return { 
      x: 0.20,    // Posición horizontal ajustada hacia el oeste
      y: 0.5,     // Posición vertical (0-1, donde 0.5 es el centro) 
      scale: 7.2, // Nivel de zoom ajustado
      animate: false 
    };
  }, []);
  return (
    <VectorMap
      map={worldMill}
      backgroundColor="transparent"
      markerStyle={{
        initial: {
          fill: "#465FFF",
        },
      }}
      markersSelectable={true}
      markers={markers}
      zoomOnScroll={true}
      zoomMax={10}
      zoomMin={1.5}
      zoomAnimate={true}
      zoomStep={1.5}
      focusOn={focusConfig}
      regionStyle={{
        initial: {
          fill: "#D0D5DD",
          fillOpacity: 1,
          fontFamily: "Outfit",
          stroke: "none",
          strokeWidth: 0,
          strokeOpacity: 0,
        },
        hover: {
          fillOpacity: 0.7,
          cursor: "pointer",
          fill: "#465fff",
          stroke: "none",
        },
        selected: {
          fill: "#465FFF",
        },
        selectedHover: {},
      }}
      regionLabelStyle={{
        initial: {
          fill: "#35373e",
          fontWeight: 500,
          fontSize: "13px",
          stroke: "none",
        },
        hover: {},
        selected: {},
        selectedHover: {},
      }}
    />
  );
};

export default CountryMap;
