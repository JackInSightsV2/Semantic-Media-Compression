import Link from 'next/link';
import { FaRocket, FaArrowRight } from 'react-icons/fa';

export const ProductHero = () => {
  return (
    <section className="relative bg-brand-dark pt-32 pb-48 overflow-hidden min-h-[90vh] flex items-center">
      {/* Abstract Background */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
         <div className="absolute top-[-10%] right-[-5%] w-[50vw] h-[50vw] bg-brand-purple rounded-full filter blur-[100px] opacity-30 animate-pulse"></div>
         <div className="absolute bottom-[-10%] left-[-10%] w-[40vw] h-[40vw] bg-brand-cyan rounded-full filter blur-[100px] opacity-20"></div>
         {/* Grid pattern overlay */}
         <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
         <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0)', backgroundSize: '40px 40px' }}></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 md:px-8 relative z-10 w-full">
        <div className="flex flex-col lg:flex-row items-center gap-16">
          
          {/* Text Content */}
          <div className="w-full lg:w-1/2 space-y-8">
            <div className="inline-flex items-center gap-2 bg-brand-cyan/10 border border-brand-cyan/30 rounded-full px-4 py-1.5">
               <span className="w-2 h-2 rounded-full bg-brand-cyan animate-pulse"></span>
               <span className="text-brand-cyan text-sm font-bold tracking-wide uppercase">Operating System for IP</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-black text-white leading-tight">
              Manage, Protect, <br />
              and <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-pink to-brand-yellow">Remix</span> Your <br />
              Creative DNA
            </h1>
            
            <p className="text-xl text-gray-400 max-w-xl leading-relaxed">
              The first platform that treats your story as data. Upload your work, generate a Semantic Blueprint, and unlock a universe of derivatives.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <button className="inline-flex items-center justify-center gap-3 bg-brand-cyan text-brand-dark px-8 py-4 rounded-full font-bold text-lg hover:bg-brand-cyan/90 transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(6,182,212,0.4)]">
                <FaRocket /> Launch Studio
              </button>
              <button className="inline-flex items-center justify-center gap-3 bg-white/5 text-white border border-white/10 px-8 py-4 rounded-full font-bold text-lg hover:bg-white/10 transition-all backdrop-blur-sm">
                Request Demo
              </button>
            </div>
          </div>

          {/* UI Mockup Visual */}
          <div className="w-full lg:w-1/2 relative">
             <div className="relative rounded-xl bg-gray-900/80 border border-white/10 backdrop-blur-xl shadow-2xl overflow-hidden transform rotate-y-[-12deg] hover:rotate-0 transition-all duration-700 p-2">
                {/* Window Controls */}
                <div className="h-8 bg-black/50 flex items-center px-4 gap-2 border-b border-white/5">
                   <div className="w-3 h-3 rounded-full bg-red-500"></div>
                   <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                   <div className="w-3 h-3 rounded-full bg-green-500"></div>
                   <div className="ml-4 text-xs text-gray-500 font-mono">semantical.ink — studio</div>
                </div>
                {/* Mock Interface */}
                <div className="p-6 grid grid-cols-12 gap-6 min-h-[400px]">
                   {/* Sidebar */}
                   <div className="col-span-3 space-y-3 border-r border-white/5 pr-4">
                      <div className="h-8 w-full bg-brand-pink/20 rounded animate-pulse"></div>
                      <div className="h-4 w-2/3 bg-white/10 rounded"></div>
                      <div className="h-4 w-3/4 bg-white/10 rounded"></div>
                      <div className="h-4 w-1/2 bg-white/10 rounded"></div>
                      <div className="mt-8 h-32 w-full bg-white/5 rounded border border-white/5 border-dashed flex items-center justify-center text-xs text-gray-600">
                         Assets
                      </div>
                   </div>
                   {/* Main Canvas - Node Graph */}
                   <div className="col-span-9 relative">
                      <div className="absolute inset-0 flex items-center justify-center">
                         <div className="relative w-full h-full">
                            {/* Central Node */}
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-brand-yellow rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(253,224,71,0.3)] z-10">
                               <span className="text-3xl">📖</span>
                            </div>
                            {/* Connected Nodes */}
                            <div className="absolute top-1/4 left-1/4 w-16 h-16 bg-brand-pink rounded-2xl flex items-center justify-center text-xl z-10 animate-bounce" style={{ animationDuration: '3s' }}>🎬</div>
                            <div className="absolute bottom-1/3 right-1/4 w-16 h-16 bg-brand-cyan rounded-2xl flex items-center justify-center text-xl z-10 animate-bounce" style={{ animationDuration: '4s' }}>🎮</div>
                            <div className="absolute top-1/3 right-1/3 w-12 h-12 bg-brand-purple rounded-full flex items-center justify-center text-lg z-10">🎵</div>
                            
                            {/* Connecting Lines (SVG) */}
                            <svg className="absolute inset-0 w-full h-full pointer-events-none stroke-white/20 stroke-2">
                               <line x1="50%" y1="50%" x2="25%" y2="25%" />
                               <line x1="50%" y1="50%" x2="75%" y2="66%" />
                               <line x1="50%" y1="50%" x2="66%" y2="33%" />
                            </svg>
                         </div>
                      </div>
                   </div>
                </div>
             </div>
             
             {/* Floating Badge */}
             <div className="absolute -bottom-8 -left-8 bg-brand-dark border border-brand-pink/30 p-4 rounded-xl shadow-xl backdrop-blur-md">
                <div className="flex items-center gap-3">
                   <div className="w-10 h-10 rounded-full bg-brand-pink flex items-center justify-center text-white font-bold">
                      AI
                   </div>
                   <div>
                      <div className="text-xs text-gray-400 uppercase tracking-wider">Analysis</div>
                      <div className="text-white font-bold">Processing...</div>
                   </div>
                </div>
             </div>
          </div>
        </div>
      </div>
      
      {/* Bottom Wavy Divider */}
      <div className="absolute bottom-0 left-0 w-full leading-none text-brand-dark bg-brand-dark z-20">
         <svg className="block w-full h-16 md:h-24 text-gray-900" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path fill="currentColor" fillOpacity="1" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,261.3C960,256,1056,224,1152,197.3C1248,171,1344,149,1392,138.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
         </svg>
      </div>
    </section>
  );
};

