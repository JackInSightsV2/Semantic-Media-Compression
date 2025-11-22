import { FaCloudUploadAlt, FaRobot, FaProjectDiagram } from 'react-icons/fa';

export const HowItWorksSection = () => {
  const steps = [
    {
      id: 1,
      title: "Upload Your Content",
      desc: "Upload your novel, comic, artwork, or any creative content. We support PDFs, images, text files, and more.",
      icon: <FaCloudUploadAlt size={32} />,
      color: "bg-brand-pink",
      delay: "0"
    },
    {
      id: 2,
      title: "AI Extracts the Essence",
      desc: "Our AI identifies the narrative, characters, themes, and visual style, reading your content like a human would.",
      icon: <FaRobot size={32} />,
      color: "bg-brand-cyan",
      delay: "100"
    },
    {
      id: 3,
      title: "Get Your Blueprint",
      desc: "Receive a structured semantic blueprint—a recipe that preserves everything that matters and allows for infinite regeneration.",
      icon: <FaProjectDiagram size={32} />,
      color: "bg-brand-yellow",
      delay: "200"
    }
  ];

  return (
    <section id="how-it-works" className="py-24 bg-brand-cream relative">
       {/* Wavy top divider */}
       <div className="absolute top-0 left-0 w-full overflow-hidden leading-none rotate-180 -mt-1">
          <svg className="block w-full h-12 md:h-24 text-white" viewBox="0 0 1440 320" preserveAspectRatio="none">
             <path fill="currentColor" fillOpacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
          </svg>
       </div>

       <div className="max-w-6xl mx-auto px-4 md:px-8 relative z-10">
         <div className="text-center mb-16">
           <span className="text-brand-pink font-bold tracking-wider uppercase mb-2 block">The Process</span>
           <h2 className="text-3xl md:text-5xl font-black text-brand-dark">Start your engine in 3 simple steps</h2>
         </div>

         <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step) => (
              <div key={step.id} className="bg-white rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-2 relative overflow-hidden group">
                 {/* Step Number */}
                 <div className="absolute -right-4 -top-4 w-24 h-24 bg-gray-50 rounded-full flex items-end justify-start p-4 text-6xl font-black text-gray-100 group-hover:text-brand-yellow/20 transition-colors">
                    {step.id}
                 </div>
                 
                 <div className={`${step.color} w-16 h-16 rounded-2xl flex items-center justify-center text-white mb-6 shadow-lg relative z-10`}>
                    {step.icon}
                 </div>
                 
                 <h3 className="text-2xl font-bold text-brand-dark mb-4 relative z-10">{step.title}</h3>
                 <p className="text-gray-600 leading-relaxed relative z-10">
                    {step.desc}
                 </p>
              </div>
            ))}
         </div>
       </div>
    </section>
  );
};

