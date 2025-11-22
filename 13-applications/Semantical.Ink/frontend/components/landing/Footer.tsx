import Link from 'next/link';
import { FaTwitter, FaGithub, FaDiscord, FaHeart } from 'react-icons/fa';

export const Footer = () => {
  return (
    <footer className="bg-brand-dark text-white pt-24 pb-12 relative overflow-hidden">
      {/* Top Wavy Divider - Inverted */}
       <div className="absolute top-0 left-0 w-full overflow-hidden leading-none rotate-180">
          <svg className="block w-full h-12 md:h-24 text-brand-yellow/10" viewBox="0 0 1440 320" preserveAspectRatio="none">
             <path fill="currentColor" fillOpacity="1" d="M0,64L48,80C96,96,192,128,288,128C384,128,480,96,576,80C672,64,768,64,864,80C960,96,1056,128,1152,128C1248,128,1344,96,1392,80L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
          </svg>
       </div>

      <div className="max-w-6xl mx-auto px-4 md:px-8 relative z-10">
        {/* CTA Section */}
        <div className="bg-brand-pink rounded-[3rem] p-8 md:p-16 text-center mb-20 shadow-2xl transform -translate-y-10 border-4 border-white/10">
           <h2 className="text-3xl md:text-5xl font-black mb-6">Start Creating Your Semantic Blueprints</h2>
           <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
             Join creators who are transforming how content is made, protected, and shared.
           </p>
           <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/produce" className="bg-white text-brand-pink px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:bg-gray-100 transition-transform hover:scale-105">
                 Get Started Now
              </Link>
              <Link href="#" className="bg-brand-dark/30 text-white border-2 border-white/30 px-8 py-4 rounded-full font-bold text-lg hover:bg-brand-dark/50 transition-transform hover:scale-105">
                 Read the Docs
              </Link>
           </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 border-b border-white/10 pb-12">
           <div className="col-span-1 md:col-span-2">
              <h3 className="text-2xl font-black text-brand-yellow mb-4">Semantical.Ink</h3>
              <p className="text-gray-400 leading-relaxed max-w-sm">
                 The semantic compression platform for creators. Turn your stories into blueprints and unlock infinite possibilities.
              </p>
           </div>
           
           <div>
              <h4 className="font-bold text-lg mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                 <li><Link href="/produce" className="hover:text-brand-cyan">Produce</Link></li>
                 <li><Link href="/marketplace" className="hover:text-brand-cyan">Marketplace</Link></li>
                 <li><Link href="/library" className="hover:text-brand-cyan">Library</Link></li>
              </ul>
           </div>
           
           <div>
              <h4 className="font-bold text-lg mb-4">Connect</h4>
              <div className="flex gap-4">
                 <a href="#" className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-brand-cyan transition-colors"><FaTwitter /></a>
                 <a href="#" className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-brand-cyan transition-colors"><FaGithub /></a>
                 <a href="#" className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-brand-cyan transition-colors"><FaDiscord /></a>
              </div>
           </div>
        </div>
        
        <div className="pt-8 text-center text-gray-500 text-sm flex items-center justify-center gap-2">
           <span>© {new Date().getFullYear()} Semantical.Ink. Made with</span> <FaHeart className="text-brand-pink" /> <span>for creators.</span>
        </div>
      </div>
    </footer>
  );
};

