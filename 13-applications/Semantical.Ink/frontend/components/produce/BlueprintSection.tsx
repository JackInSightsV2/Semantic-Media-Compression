import { FaCode, FaProjectDiagram, FaLayerGroup } from 'react-icons/fa';

export const BlueprintSection = () => {
  return (
    <section className="py-24 bg-gray-900 text-white relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 md:px-8">
        <div className="flex flex-col md:flex-row items-center gap-16">
           <div className="w-full md:w-1/2 order-2 md:order-1">
              {/* JSON Visualization Code Block */}
              <div className="bg-[#1E1E1E] rounded-2xl p-6 shadow-2xl border border-gray-700 font-mono text-sm relative overflow-hidden group">
                 {/* Header */}
                 <div className="flex gap-2 mb-4 opacity-50">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                 </div>
                 
                 {/* Code Content */}
                 <div className="space-y-1 text-gray-300">
                    <div className="text-purple-400">{"{"}</div>
                    <div className="pl-4"><span className="text-blue-400">"title"</span>: <span className="text-green-400">"The Last Starship"</span>,</div>
                    <div className="pl-4"><span className="text-blue-400">"version"</span>: <span className="text-orange-400">1.0</span>,</div>
                    <div className="pl-4"><span className="text-blue-400">"semantic_hash"</span>: <span className="text-green-400">"0x8f2...a9"</span>,</div>
                    <div className="pl-4"><span className="text-blue-400">"dimensions"</span>: {"{"}</div>
                    
                    {/* Highlighted Block - Narrative */}
                    <div className="pl-8 py-1 bg-brand-yellow/10 border-l-2 border-brand-yellow -ml-2 pr-2 rounded-r transition-colors hover:bg-brand-yellow/20 cursor-pointer">
                       <span className="text-blue-400">"narrative"</span>: {"{"} <span className="text-gray-500">// Extracted plot arcs</span>
                       <div className="pl-4"><span className="text-blue-400">"theme"</span>: <span className="text-green-400">"Hope vs Despair"</span>,</div>
                       <div className="pl-4"><span className="text-blue-400">"pacing"</span>: <span className="text-green-400">"Accelerating"</span></div>
                       <span className="text-blue-400">{"}"}</span>,
                    </div>

                    {/* Highlighted Block - Characters */}
                    <div className="pl-8 py-1 bg-brand-pink/10 border-l-2 border-brand-pink -ml-2 pr-2 rounded-r transition-colors hover:bg-brand-pink/20 cursor-pointer mt-1">
                       <span className="text-blue-400">"characters"</span>: [ <span className="text-gray-500">// Character profiles</span>
                       <div className="pl-4">{"{"} <span className="text-blue-400">"id"</span>: <span className="text-green-400">"hero_01"</span>, <span className="text-blue-400">"archetype"</span>: <span className="text-green-400">"Rebel"</span> {"}"}</div>
                       <span className="text-blue-400">]</span>
                    </div>

                    <div className="pl-4 text-blue-400">{"}"}</div>
                    <div className="text-purple-400">{"}"}</div>
                 </div>

                 {/* Floating Label */}
                 <div className="absolute top-4 right-4 bg-brand-cyan/20 text-brand-cyan px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border border-brand-cyan/50">
                    blueprint.json
                 </div>
              </div>
           </div>

           <div className="w-full md:w-1/2 order-1 md:order-2">
              <h2 className="text-4xl md:text-5xl font-black mb-6 text-white">Your Story, <span className="text-brand-cyan">Structured</span>.</h2>
              <p className="text-gray-400 text-lg mb-8 leading-relaxed">
                 Our AI distills your content into a <strong>Semantic JSON Blueprint</strong>. This isn't just metadata; it's the source code of your narrative. It captures character arcs, emotional beats, and world-building rules in a format that machines can understand and creators can build upon.
              </p>
              
              <div className="space-y-6">
                 <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-brand-yellow rounded-xl flex items-center justify-center text-brand-dark shrink-0">
                       <FaProjectDiagram size={24} />
                    </div>
                    <div>
                       <h3 className="text-xl font-bold text-white mb-1">Narrative Extraction</h3>
                       <p className="text-gray-500 text-sm">Identifies plot points, pacing, and conflict structures automatically.</p>
                    </div>
                 </div>
                 
                 <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-brand-pink rounded-xl flex items-center justify-center text-white shrink-0">
                       <FaLayerGroup size={24} />
                    </div>
                    <div>
                       <h3 className="text-xl font-bold text-white mb-1">Thematic Analysis</h3>
                       <p className="text-gray-500 text-sm">Maps tone, mood, and core messages to preserve emotional resonance.</p>
                    </div>
                 </div>
                 
                 <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-brand-purple rounded-xl flex items-center justify-center text-white shrink-0">
                       <FaCode size={24} />
                    </div>
                    <div>
                       <h3 className="text-xl font-bold text-white mb-1">Machine Readable</h3>
                       <p className="text-gray-500 text-sm">Ready for generative AI inputs, game engines, and licensing protocols.</p>
                    </div>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
};

