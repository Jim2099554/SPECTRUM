

// Usa el logo circular de sentinela y una animación de giro
export default function LogoSpinner({ size = 80 }: { size?: number }) {
  return (
    <div className="flex items-center justify-center w-full h-full">
      <img
        src="/images/logo/logo-sentinela-circular.png"
        alt="Cargando Sentinela"
        style={{ width: size, height: size }}
        className="animate-spin-slow"
      />
    </div>
  );
}

// Animación personalizada (Tailwind):
// .animate-spin-slow { animation: spin 1.2s linear infinite; }
// Si no existe, agrégala en tailwind.config.js o usa animate-spin normal.
