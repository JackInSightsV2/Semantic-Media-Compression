import { FaMagic, FaGlobeAmericas, FaPalette, FaShieldAlt } from 'react-icons/fa';

export const UseCasesSection = () => {
  const useCases = [
    {
      title: "Format Transformation",
      desc: "Turn your novel into a comic, or your comic into an animation script.",
      icon: <FaMagic size={24} />,
      color: "bg-purple-100 text-purple-600"
    },
    {
      title: "Style Adaptation",
      desc: "Keep your story, change the style. Realistic → Stylized. Modern → Vintage.",
      icon: <FaPalette size={24} />,
      color: "bg-pink-100 text-pink-600"
    },
    {
      title: "Cultural Adaptation",
      desc: "Adapt your content for different cultures while preserving the core narrative.",
      icon: <FaGlobeAmericas size={24} />,
      color: "bg-green-100 text-green-600"
    },
    {
      title: "Protection & Ownership",
      desc: "Immutable proof of ownership on the blockchain via Story Protocol.",
      icon: <FaShieldAlt size={24} />,
      color: "bg-blue-100 text-blue-600"
    }
  ];

  return (
    <section className="py-24 bg-brand-yellow/10">
      <div className="max-w-6xl mx-auto px-4 md:px-8">
        <div className="flex flex-col md:flex-row items-end justify-between mb-12">
           <div className="max-w-2xl">
             <span className="text-brand-cyan font-bold tracking-wider uppercase mb-2 block">Possibilities</span>
             <h2 className="text-3xl md:text-5xl font-black text-brand-dark">What can you do with it?</h2>
           </div>
           <p className="text-xl text-gray-600 max-w-md mt-4 md:mt-0">
              One blueprint, infinite possibilities. Unlock the full potential of your IP.
           </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {useCases.map((item, idx) => (
            <div key={idx} className="bg-white rounded-3xl p-6 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-brand-yellow group">
               <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 ${item.color} group-hover:scale-110 transition-transform`}>
                  {item.icon}
               </div>
               <h3 className="text-xl font-bold text-brand-dark mb-3">{item.title}</h3>
               <p className="text-gray-600 text-sm leading-relaxed">
                  {item.desc}
               </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

