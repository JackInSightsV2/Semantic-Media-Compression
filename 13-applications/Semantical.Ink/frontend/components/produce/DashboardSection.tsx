import { FaTree, FaStore, FaList } from 'react-icons/fa';

export const DashboardSection = () => {
  return (
    <section className="py-32 bg-white text-brand-dark relative">
      {/* Top Wavy Separator (Transition from Dark to Light) */}
      <div className="absolute top-0 left-0 w-full overflow-hidden leading-none bg-gray-900 z-10">
         <svg className="block w-full h-12 md:h-24 text-white" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path fill="currentColor" fillOpacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
         </svg>
      </div>

      <div className="max-w-7xl mx-auto px-4 md:px-8">
         <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-black text-brand-dark mb-6">Complete Control Over Your IP</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
               Manage your entire IP portfolio in one place. Track versions, view derivative chains, and manage access rights.
            </p>
         </div>
         
         <div className="bg-gray-100 rounded-3xl p-4 md:p-8 shadow-inner">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
               {/* Mock Dashboard Header */}
               <div className="border-b border-gray-100 p-4 flex justify-between items-center bg-gray-50/50">
                  <div className="font-bold text-brand-dark">My Projects</div>
                  <div className="flex gap-2">
                     <div className="h-8 w-24 bg-brand-dark text-white rounded-lg text-xs flex items-center justify-center font-bold cursor-pointer hover:bg-brand-dark/90">New Project</div>
                  </div>
               </div>
               
               {/* Mock Dashboard Body */}
               <div className="p-6 md:p-8">
                  <div className="flex flex-col md:flex-row gap-8">
                     {/* Sidebar */}
                     <div className="w-full md:w-64 space-y-2 shrink-0">
                        <div className="bg-brand-cyan/10 text-brand-cyan font-bold p-3 rounded-lg flex items-center gap-3 cursor-pointer"><FaList /> All Assets</div>
                        <div className="text-gray-500 p-3 rounded-lg flex items-center gap-3 hover:bg-gray-50 cursor-pointer"><FaTree /> Genealogy</div>
                        <div className="text-gray-500 p-3 rounded-lg flex items-center gap-3 hover:bg-gray-50 cursor-pointer"><FaStore /> Marketplace</div>
                     </div>
                     
                     {/* Content Area - Tree View */}
                     <div className="flex-1 bg-gray-50 rounded-xl p-8 min-h-[300px] flex items-center justify-center relative overflow-hidden border border-dashed border-gray-300">
                         <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:16px_16px] opacity-50"></div>
                         
                         {/* Simple Tree Visualization */}
                         <div className="relative z-10 flex flex-col items-center gap-8">
                            <div className="flex flex-col items-center">
                               <div className="w-16 h-16 bg-brand-dark text-white rounded-xl flex items-center justify-center text-2xl shadow-lg mb-2 border-2 border-brand-dark">📖</div>
                               <span className="font-bold text-xs bg-white px-2 py-1 rounded shadow-sm">Original Novel</span>
                            </div>
                            
                            <div className="h-8 w-0.5 bg-gray-300"></div>
                            <div className="w-full h-0.5 bg-gray-300 w-32"></div>
                            
                            <div className="flex gap-16 mt-[-1px]">
                               <div className="flex flex-col items-center pt-8 relative">
                                  <div className="absolute top-0 left-1/2 -translate-x-1/2 h-8 w-0.5 bg-gray-300"></div>
                                  <div className="w-12 h-12 bg-white border-2 border-brand-pink text-brand-pink rounded-xl flex items-center justify-center text-xl shadow-md mb-2">💬</div>
                                  <span className="font-bold text-xs text-gray-500">Comic</span>
                               </div>
                               
                               <div className="flex flex-col items-center pt-8 relative">
                                  <div className="absolute top-0 left-1/2 -translate-x-1/2 h-8 w-0.5 bg-gray-300"></div>
                                  <div className="w-12 h-12 bg-white border-2 border-brand-yellow text-brand-yellow rounded-xl flex items-center justify-center text-xl shadow-md mb-2">🇪🇸</div>
                                  <span className="font-bold text-xs text-gray-500">Spanish Translation</span>
                               </div>
                            </div>
                         </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>
         
         {/* CTA */}
         <div className="mt-24 text-center">
             <h3 className="text-2xl font-bold text-brand-dark mb-6">Ready to structure your creativity?</h3>
             <button className="bg-brand-pink text-white px-10 py-4 rounded-full font-bold text-lg shadow-xl hover:bg-brand-pink/90 transition-transform hover:scale-105">
                Create Your First Blueprint
             </button>
         </div>
      </div>
    </section>
  );
};

