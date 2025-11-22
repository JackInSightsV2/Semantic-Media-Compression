import { FaShieldAlt, FaLink, FaFingerprint } from 'react-icons/fa';

export const ProtectionSection = () => {
  return (
    <section className="py-24 bg-brand-dark relative border-t border-white/5">
       <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-brand-purple/20 via-transparent to-transparent opacity-40"></div>
       
       <div className="max-w-4xl mx-auto px-4 md:px-8 text-center relative z-10">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 rounded-full mb-8 border border-white/20 backdrop-blur-sm">
             <FaShieldAlt size={32} className="text-white" />
          </div>
          
          <h2 className="text-3xl md:text-5xl font-black text-white mb-6">Protection by Default</h2>
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
             Every Semantic Blueprint you create is automatically registered as an <strong>IP Asset</strong> on the blockchain via <span className="text-white font-bold border-b-2 border-brand-pink">Story Protocol</span>.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
             <div className="bg-white/5 border border-white/10 p-6 rounded-2xl hover:bg-white/10 transition-colors">
                <FaFingerprint className="text-brand-cyan text-2xl mb-4" />
                <h3 className="text-lg font-bold text-white mb-2">Immutable Record</h3>
                <p className="text-gray-500 text-sm">Time-stamped proof of creation that lives forever on-chain.</p>
             </div>
             
             <div className="bg-white/5 border border-white/10 p-6 rounded-2xl hover:bg-white/10 transition-colors">
                <FaLink className="text-brand-pink text-2xl mb-4" />
                <h3 className="text-lg font-bold text-white mb-2">On-Chain Licensing</h3>
                <p className="text-gray-500 text-sm">Set programmable rules for who can use your blueprint and how.</p>
             </div>
             
             <div className="bg-white/5 border border-white/10 p-6 rounded-2xl hover:bg-white/10 transition-colors">
                <div className="flex items-center gap-2 mb-4">
                   <span className="text-brand-yellow text-2xl font-bold">$</span>
                   <span className="text-xs bg-brand-yellow/20 text-brand-yellow px-2 py-0.5 rounded uppercase">Coming Soon</span>
                </div>
                <h3 className="text-lg font-bold text-white mb-2">Royalty Tracking</h3>
                <p className="text-gray-500 text-sm">Get paid automatically when AI or other creators use your work.</p>
             </div>
          </div>
       </div>
    </section>
  );
};

