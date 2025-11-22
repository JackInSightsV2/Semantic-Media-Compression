import Link from 'next/link';
import { FaArrowRight, FaPlay } from 'react-icons/fa';

export const Hero = () => {
  return (
    <section className="relative bg-brand-yellow pt-20 pb-32 overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-brand-pink rounded-full filter blur-3xl opacity-20 -translate-y-1/2 translate-x-1/2"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-brand-cyan rounded-full filter blur-3xl opacity-20 translate-y-1/2 -translate-x-1/2"></div>

      <div className="max-w-6xl mx-auto px-4 md:px-8 relative z-10">
        <div className="flex flex-col md:flex-row items-center gap-12">
          <div className="w-full md:w-1/2 text-center md:text-left space-y-6">
            <h1 className="text-4xl md:text-6xl font-black text-brand-dark leading-tight">
              Turn Your <span className="text-brand-pink">Creative Work</span> Into Its Essence
            </h1>
            <p className="text-xl text-brand-dark/80 font-medium">
              Semantic compression captures the meaning, story, and soul of your content—not just the pixels or words.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start pt-4">
              <Link 
                href="/produce" 
                className="inline-flex items-center justify-center gap-2 bg-brand-pink text-white px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:bg-brand-pink/90 transition-transform hover:scale-105"
              >
                Get Started <FaArrowRight />
              </Link>
              <Link 
                href="#how-it-works" 
                className="inline-flex items-center justify-center gap-2 bg-white text-brand-dark px-8 py-4 rounded-full font-bold text-lg shadow-md hover:bg-gray-50 transition-transform hover:scale-105"
              >
                <FaPlay className="text-brand-cyan" size={14} /> See How It Works
              </Link>
            </div>
          </div>
          
          <div className="w-full md:w-1/2 relative">
            <div className="relative z-10 bg-white rounded-3xl shadow-2xl p-4 md:p-8 transform rotate-2 hover:rotate-0 transition-transform duration-500">
               {/* Placeholder for Hero Illustration */}
               <div className="aspect-video bg-brand-cream rounded-xl flex items-center justify-center border-2 border-dashed border-brand-yellow">
                  <div className="text-center p-4">
                    <div className="flex items-center justify-center gap-4 mb-4">
                       <div className="w-12 h-16 bg-gray-200 rounded shadow flex items-center justify-center">📄</div>
                       <FaArrowRight className="text-brand-cyan" />
                       <div className="w-16 h-16 bg-brand-purple text-white rounded-lg shadow flex items-center justify-center font-mono text-xs">JSON</div>
                       <FaArrowRight className="text-brand-cyan" />
                       <div className="flex gap-2">
                          <div className="w-10 h-10 bg-green-100 rounded shadow flex items-center justify-center">🎬</div>
                          <div className="w-10 h-10 bg-blue-100 rounded shadow flex items-center justify-center">🎮</div>
                       </div>
                    </div>
                    <p className="font-bold text-brand-dark">Content → Blueprint → Anything</p>
                  </div>
               </div>
            </div>
            
            {/* Decorative elements behind image */}
            <div className="absolute -bottom-6 -right-6 w-full h-full bg-brand-cyan rounded-3xl -z-10 opacity-50 transform -rotate-2"></div>
          </div>
        </div>
      </div>
      
      {/* Wavy bottom divider */}
      <div className="absolute bottom-0 left-0 w-full leading-none text-white">
         <svg className="block w-full h-12 md:h-24" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path fill="currentColor" fillOpacity="1" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,261.3C960,256,1056,224,1152,197.3C1248,171,1344,149,1392,138.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
         </svg>
      </div>
    </section>
  );
};

