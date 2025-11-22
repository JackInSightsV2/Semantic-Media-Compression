import Link from 'next/link';
import { FaCheckCircle, FaArrowRight } from 'react-icons/fa';

export const WhyMattersSection = () => {
  const benefits = [
    "Create once, use everywhere",
    "Protect your ideas, not just your files",
    "Monetize your creativity in new ways",
    "Future-proof your content for AI"
  ];

  return (
    <section className="py-24 bg-brand-dark text-white relative overflow-hidden">
      {/* Background noise/pattern could go here */}
      
      <div className="max-w-6xl mx-auto px-4 md:px-8 relative z-10">
        <div className="flex flex-col md:flex-row-reverse items-center gap-16">
           <div className="w-full md:w-1/2">
              <h2 className="text-3xl md:text-5xl font-black text-white mb-8">Why It Matters</h2>
              <div className="space-y-6 mb-8">
                 {benefits.map((benefit, idx) => (
                    <div key={idx} className="flex items-center gap-4">
                       <div className="w-8 h-8 rounded-full bg-brand-yellow flex items-center justify-center text-brand-dark flex-shrink-0">
                          <FaCheckCircle />
                       </div>
                       <p className="text-xl font-medium">{benefit}</p>
                    </div>
                 ))}
              </div>
              
              <Link href="/produce" className="inline-flex items-center gap-2 text-brand-cyan hover:text-brand-pink font-bold text-lg group transition-colors">
                 Explore the Platform <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
              </Link>
           </div>
           
           <div className="w-full md:w-1/2">
              <div className="bg-white/5 backdrop-blur-md rounded-3xl p-8 border border-white/10">
                 {/* Abstract illustration of One Source -> Many Outputs */}
                 <div className="flex flex-col items-center gap-4">
                    <div className="w-20 h-20 bg-brand-pink rounded-2xl flex items-center justify-center text-3xl shadow-lg shadow-brand-pink/20">
                       🧠
                    </div>
                    <div className="h-12 w-0.5 bg-white/20"></div>
                    <div className="grid grid-cols-3 gap-4 w-full">
                       {[1,2,3].map((i) => (
                          <div key={i} className="bg-white/10 rounded-xl p-4 flex flex-col items-center gap-2">
                             <div className="w-10 h-10 bg-brand-cyan/20 rounded-full"></div>
                             <div className="h-2 w-12 bg-white/20 rounded"></div>
                          </div>
                       ))}
                    </div>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </section>
  );
};
