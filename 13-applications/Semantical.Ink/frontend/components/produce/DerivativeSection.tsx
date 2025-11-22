import { FaMagic, FaArrowRight } from 'react-icons/fa';

export const DerivativeSection = () => {
  return (
    <section className="py-24 bg-gray-900 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 md:px-8">
        <div className="text-center mb-20">
          <h2 className="text-3xl md:text-5xl font-black text-white mb-4">One Source. <span className="text-brand-pink">Infinite Adaptations</span>.</h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
             Use your Semantic Blueprint to generate high-fidelity derivatives instantly. Adaptations stay true to the source material because the AI understands the meaning.
          </p>
        </div>

        <div className="relative">
           {/* Central Workflow Line */}
           <div className="absolute top-1/2 left-0 w-full h-1 bg-gradient-to-r from-brand-cyan via-brand-purple to-brand-pink opacity-30 hidden md:block transform -translate-y-1/2"></div>
           
           <div className="grid grid-cols-1 md:grid-cols-5 gap-8 items-center relative z-10">
              {/* Step 1: Input */}
              <div className="col-span-2 bg-[#111] border border-gray-800 p-8 rounded-3xl relative group hover:border-brand-cyan transition-colors">
                 <div className="absolute -top-4 left-8 bg-brand-cyan text-brand-dark font-bold px-3 py-1 rounded text-xs uppercase">Input</div>
                 <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-gray-800 rounded-xl flex items-center justify-center text-3xl">📘</div>
                    <div>
                       <h3 className="text-xl font-bold text-white">Original Novel</h3>
                       <p className="text-gray-500 text-sm">"The Space Between"</p>
                    </div>
                 </div>
              </div>

              {/* Arrow / Engine */}
              <div className="col-span-1 flex justify-center">
                 <div className="w-20 h-20 bg-brand-dark rounded-full border-4 border-brand-purple flex items-center justify-center shadow-[0_0_30px_rgba(76,29,149,0.5)] z-10 relative">
                    <FaMagic className="text-brand-purple text-2xl animate-pulse" />
                 </div>
              </div>

              {/* Step 2: Outputs */}
              <div className="col-span-2 space-y-4">
                 <div className="bg-[#111] border border-gray-800 p-4 rounded-2xl flex items-center justify-between group hover:border-brand-pink transition-colors cursor-pointer">
                    <div className="flex items-center gap-3">
                       <div className="w-10 h-10 bg-brand-pink/20 text-brand-pink rounded-lg flex items-center justify-center">💬</div>
                       <span className="text-white font-medium">Graphic Novel Script</span>
                    </div>
                    <FaArrowRight className="text-gray-600 group-hover:text-brand-pink" />
                 </div>
                 
                 <div className="bg-[#111] border border-gray-800 p-4 rounded-2xl flex items-center justify-between group hover:border-brand-yellow transition-colors cursor-pointer">
                    <div className="flex items-center gap-3">
                       <div className="w-10 h-10 bg-brand-yellow/20 text-brand-yellow rounded-lg flex items-center justify-center">🎮</div>
                       <span className="text-white font-medium">Interactive RPG Quest</span>
                    </div>
                    <FaArrowRight className="text-gray-600 group-hover:text-brand-yellow" />
                 </div>
                 
                 <div className="bg-[#111] border border-gray-800 p-4 rounded-2xl flex items-center justify-between group hover:border-brand-cyan transition-colors cursor-pointer">
                    <div className="flex items-center gap-3">
                       <div className="w-10 h-10 bg-brand-cyan/20 text-brand-cyan rounded-lg flex items-center justify-center">🎌</div>
                       <span className="text-white font-medium">Anime Character Sheet</span>
                    </div>
                    <FaArrowRight className="text-gray-600 group-hover:text-brand-cyan" />
                 </div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
};

