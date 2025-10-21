interface SimilarityResults {
  overall: number;
  dimensions: {
    narrative: number;
    character: number;
    thematic: number;
  };
  level: string;
  matching_elements: string[];
}

interface Props {
  results: SimilarityResults;
}

export default function SimilarityScore({ results }: Props) {
  const getBadgeColor = (score: number) => {
    if (score > 0.85) return 'from-red-600 to-red-500';
    if (score > 0.70) return 'from-yellow-600 to-yellow-500';
    return 'from-green-600 to-green-500';
  };
  
  const getBarColor = (score: number) => {
    if (score > 0.85) return 'from-red-500 to-red-600';
    if (score > 0.70) return 'from-yellow-500 to-yellow-600';
    return 'from-green-500 to-green-600';
  };
  
  const circumference = 2 * Math.PI * 120;
  const strokeDashoffset = circumference - (results.overall * circumference);
  
  return (
    <div>
      {/* Overall Score */}
      <div className="text-center mb-12">
        <div className="relative inline-flex items-center justify-center mb-8">
          {/* Background glow */}
          <div className={`absolute inset-0 bg-gradient-to-r ${getBadgeColor(results.overall)} blur-3xl opacity-30`} />
          
          {/* SVG Circle */}
          <svg className="w-64 h-64 transform -rotate-90 relative">
            <circle
              className="text-white/5"
              strokeWidth="16"
              stroke="currentColor"
              fill="transparent"
              r="120"
              cx="128"
              cy="128"
            />
            <circle
              className={`transition-all duration-1000 ease-out`}
              strokeWidth="16"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              stroke="url(#gradient)"
              fill="transparent"
              r="120"
              cx="128"
              cy="128"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" className={results.overall > 0.85 ? "text-red-500" : results.overall > 0.70 ? "text-yellow-500" : "text-green-500"} stopColor="currentColor" />
                <stop offset="100%" className={results.overall > 0.85 ? "text-red-600" : results.overall > 0.70 ? "text-yellow-600" : "text-green-600"} stopColor="currentColor" />
              </linearGradient>
            </defs>
          </svg>
          
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-7xl font-bold text-white mb-2">
              {Math.round(results.overall * 100)}%
            </span>
            <span className="text-sm text-gray-400 uppercase tracking-wider">Similarity</span>
          </div>
        </div>
        
        <div className={`inline-block px-8 py-4 rounded-2xl font-bold text-lg glass-card border-2 ${
          results.level === 'HIGH' ? 'border-red-500/50 text-red-400' :
          results.level === 'MODERATE' ? 'border-yellow-500/50 text-yellow-400' :
          'border-green-500/50 text-green-400'
        }`}>
          {results.level === 'HIGH' && '⚠️ HIGH PLAGIARISM RISK'}
          {results.level === 'MODERATE' && '⚡ MODERATE SIMILARITY'}
          {results.level === 'LOW' && '✓ LOW SIMILARITY'}
        </div>
      </div>
      
      {/* Dimension Breakdown */}
      <div className="mb-12">
        <h3 className="text-2xl font-bold mb-8 text-white">Dimensional Analysis</h3>
        <div className="space-y-6">
          {Object.entries(results.dimensions).map(([dim, score]) => (
            <div key={dim} className="glass-card p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="font-semibold text-lg capitalize text-white">{dim} Structure</span>
                <span className="font-bold text-2xl text-white">{Math.round(score * 100)}%</span>
              </div>
              <div className="relative h-3 bg-white/5 rounded-full overflow-hidden">
                <div 
                  className={`absolute h-full rounded-full bg-gradient-to-r ${getBarColor(score)} transition-all duration-1000 ease-out`}
                  style={{ width: `${score * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Matching Elements */}
      {results.matching_elements && results.matching_elements.length > 0 && (
        <div className="glass-card border-2 border-yellow-500/30 p-8">
          <h3 className="text-2xl font-bold mb-6 flex items-center text-white">
            <span className="text-3xl mr-3">⚠️</span>
            Matching Semantic Elements
          </h3>
          <ul className="space-y-4">
            {results.matching_elements.map((element, i) => (
              <li key={i} className="flex items-start text-gray-300">
                <span className="text-yellow-500 mr-4 mt-1 text-xl">•</span>
                <span className="flex-1 leading-relaxed">{element}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
