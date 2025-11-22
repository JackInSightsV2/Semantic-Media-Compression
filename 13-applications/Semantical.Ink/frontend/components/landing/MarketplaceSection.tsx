import { FaUsers, FaNetworkWired, FaExchangeAlt } from 'react-icons/fa';

export const MarketplaceSection = () => {
  return (
    <section className="py-24 bg-white relative overflow-hidden">
      <div className="max-w-6xl mx-auto px-4 md:px-8">
        <div className="flex flex-col md:flex-row items-center gap-12 mb-16">
           <div className="w-full md:w-1/2">
              <span className="text-brand-pink font-bold tracking-wider uppercase mb-2 block">Community</span>
              <h2 className="text-3xl md:text-5xl font-black text-brand-dark mb-6">The Marketplace of Ideas</h2>
              <p className="text-xl text-gray-600 leading-relaxed mb-8">
                 Share your semantic blueprints, build on each other's creativity, and track how your stories evolve through the community.
              </p>
              <div className="space-y-4">
                 <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-brand-yellow/20 text-brand-dark rounded-full flex items-center justify-center">
                       <FaUsers />
                    </div>
                    <p className="font-medium text-brand-dark">Collaborate with other creators</p>
                 </div>
                 <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-brand-cyan/20 text-brand-cyan rounded-full flex items-center justify-center">
                       <FaNetworkWired />
                    </div>
                    <p className="font-medium text-brand-dark">Track derivative chains</p>
                 </div>
              </div>
           </div>
           
           <div className="w-full md:w-1/2 relative">
              {/* Mock Gallery Grid */}
              <div className="grid grid-cols-2 gap-4 transform rotate-3 hover:rotate-0 transition-transform duration-500">
                 {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="bg-white p-3 rounded-2xl shadow-lg border border-gray-100">
                       <div className={`aspect-square rounded-xl mb-3 ${i % 2 === 0 ? 'bg-brand-pink/20' : 'bg-brand-cyan/20'}`}></div>
                       <div className="h-2 w-2/3 bg-gray-200 rounded mb-2"></div>
                       <div className="h-2 w-1/3 bg-gray-100 rounded"></div>
                    </div>
                 ))}
              </div>
              {/* Floating badge */}
              <div className="absolute -bottom-6 -left-6 bg-brand-dark text-white p-4 rounded-xl shadow-xl rotate-[-6deg]">
                 <div className="flex items-center gap-2 font-bold">
                    <FaExchangeAlt className="text-brand-yellow" />
                    <span>Remix & Share</span>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
};

