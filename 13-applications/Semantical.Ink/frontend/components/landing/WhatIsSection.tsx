import { FaFileImage, FaBrain, FaCompressAlt, FaArrowRight } from 'react-icons/fa';

export const WhatIsSection = () => {
  return (
    <section className="py-20 bg-white overflow-hidden">
      <div className="max-w-6xl mx-auto px-4 md:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-black text-brand-dark mb-4">What is Semantic Compression?</h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
             Traditional compression shrinks files but loses quality. Semantic compression captures what your content <em className="font-bold text-brand-pink">means</em>.
          </p>
        </div>

        {/* Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
           {/* Traditional */}
           <div className="bg-gray-50 p-8 rounded-3xl border-2 border-dashed border-gray-300 flex flex-col items-center text-center">
              <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center mb-6 text-gray-400">
                <FaCompressAlt size={40} />
              </div>
              <h3 className="text-2xl font-bold text-gray-700 mb-2">Traditional</h3>
              <p className="text-gray-500 mb-4">File size reduction (100MB → 10MB)</p>
              <div className="w-full h-32 bg-gray-200 rounded-xl flex items-center justify-center overflow-hidden">
                 <span className="filter blur-[2px] opacity-50">Pixelated Content</span>
              </div>
              <p className="mt-4 text-sm font-medium text-red-500">Loses fidelity & meaning</p>
           </div>

           {/* Semantic */}
           <div className="bg-brand-cream p-8 rounded-3xl border-2 border-brand-yellow flex flex-col items-center text-center shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-brand-yellow text-brand-dark text-xs font-bold px-3 py-1 rounded-bl-xl">
                THE FUTURE
              </div>
              <div className="w-24 h-24 bg-brand-pink text-white rounded-full flex items-center justify-center mb-6 shadow-lg transform hover:scale-110 transition-transform">
                <FaBrain size={40} />
              </div>
              <h3 className="text-2xl font-bold text-brand-dark mb-2">Semantic</h3>
              <p className="text-gray-600 mb-4">Captures the "Soul" & "Story"</p>
              <div className="w-full h-32 bg-white rounded-xl flex items-center justify-center border border-brand-yellow/30">
                 <div className="flex gap-2">
                    <span className="text-2xl">🎨</span>
                    <span className="text-2xl">📝</span>
                    <span className="text-2xl">🎵</span>
                 </div>
              </div>
              <p className="mt-4 text-sm font-bold text-brand-pink">Preserves essence forever</p>
           </div>
        </div>

        {/* Core Concept */}
        <div className="bg-brand-dark text-white rounded-[3rem] p-8 md:p-16 relative overflow-hidden">
           {/* Decorative circles */}
           <div className="absolute top-0 left-0 w-64 h-64 bg-brand-purple rounded-full filter blur-3xl opacity-50 -translate-x-1/2 -translate-y-1/2"></div>
           <div className="absolute bottom-0 right-0 w-64 h-64 bg-brand-pink rounded-full filter blur-3xl opacity-20 translate-x-1/2 translate-y-1/2"></div>

           <div className="relative z-10 flex flex-col md:flex-row items-center gap-12">
              <div className="w-full md:w-1/2">
                 <h3 className="text-3xl md:text-4xl font-black mb-6 text-brand-yellow">Your Story, Not Your File</h3>
                 <p className="text-lg text-gray-300 mb-6 leading-relaxed">
                   Imagine you wrote a 300-page novel. Traditional compression shrinks the file size, but you still have 300 pages of text.
                 </p>
                 <p className="text-lg text-white font-medium leading-relaxed">
                   Semantic compression asks: <span className="text-brand-cyan">What's the story? Who are the characters?</span> It captures the blueprint that can recreate your novel, turn it into a comic, or adapt it for different cultures.
                 </p>
              </div>
              <div className="w-full md:w-1/2">
                 {/* Diagram Visualization */}
                 <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                    <div className="flex items-center justify-between text-center">
                       <div className="flex flex-col items-center">
                          <div className="w-16 h-16 bg-white text-brand-dark rounded-xl flex items-center justify-center text-2xl shadow-lg">📖</div>
                          <span className="mt-2 text-sm font-bold">Novel</span>
                       </div>
                       <div className="flex-1 px-4 flex items-center justify-center">
                          <div className="h-1 w-full bg-brand-yellow/50 relative">
                             <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-brand-dark border border-brand-yellow px-2 py-1 rounded-full text-xs text-brand-yellow">
                                Extract
                             </div>
                          </div>
                          <FaArrowRight className="text-brand-yellow mx-2" />
                       </div>
                       <div className="flex flex-col items-center">
                          <div className="w-16 h-16 bg-brand-cyan text-white rounded-xl flex items-center justify-center text-2xl shadow-lg border-2 border-white">🧬</div>
                          <span className="mt-2 text-sm font-bold text-brand-cyan">Blueprint</span>
                       </div>
                       <div className="flex-1 px-4 flex items-center justify-center">
                          <div className="h-1 w-full bg-brand-yellow/50 relative">
                             <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-brand-dark border border-brand-yellow px-2 py-1 rounded-full text-xs text-brand-yellow">
                                Generate
                             </div>
                          </div>
                          <FaArrowRight className="text-brand-yellow mx-2" />
                       </div>
                       <div className="flex flex-col gap-2">
                          <div className="w-10 h-10 bg-white text-brand-dark rounded-lg flex items-center justify-center text-lg shadow">🎬</div>
                          <div className="w-10 h-10 bg-white text-brand-dark rounded-lg flex items-center justify-center text-lg shadow">🎮</div>
                          <div className="w-10 h-10 bg-white text-brand-dark rounded-lg flex items-center justify-center text-lg shadow">📱</div>
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
};

