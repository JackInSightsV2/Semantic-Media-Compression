import React from 'react';

interface SectionProps {
  className?: string;
  children: React.ReactNode;
  id?: string;
}

export const Section = ({ className, children, id }: SectionProps) => {
  return (
    <section id={id} className={`py-16 md:py-24 px-4 md:px-8 ${className}`}>
      <div className="max-w-6xl mx-auto">
        {children}
      </div>
    </section>
  );
};

export const WavySeparator = ({ color = "fill-white", flip = false }: { color?: string; flip?: boolean }) => {
  return (
    <div className={`w-full overflow-hidden leading-none ${flip ? 'rotate-180' : ''}`}>
      <svg
        position="relative"
        display="block"
        width="calc(133% + 1.3px)"
        height="60px"
        viewBox="0 0 1200 120"
        preserveAspectRatio="none"
      >
        <path
          d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
          className={color}
        />
      </svg>
    </div>
  );
};

