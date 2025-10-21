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
  const getColor = (score: number) => {
    if (score > 0.85) return 'text-red-600 bg-red-50 border-red-200';
    if (score > 0.70) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };
  
  const getBarColor = (score: number) => {
    if (score > 0.85) return 'bg-red-500';
    if (score > 0.70) return 'bg-yellow-500';
    return 'bg-green-500';
  };
  
  return (
    <div>
      {/* Overall Score */}
      <div className="text-center mb-10 p-8 bg-white rounded-2xl shadow-xl">
        <div className="relative inline-flex items-center justify-center mb-6">
          {/* Circular progress ring */}
          <svg className="w-48 h-48 transform -rotate-90">
            <circle
              className="text-gray-200"
              strokeWidth="12"
              stroke="currentColor"
              fill="transparent"
              r="88"
              cx="96"
              cy="96"
            />
            <circle
              className={results.overall > 0.85 ? "text-red-500" : results.overall > 0.70 ? "text-yellow-500" : "text-green-500"}
              strokeWidth="12"
              strokeDasharray={`${2 * Math.PI * 88}`}
              strokeDashoffset={`${2 * Math.PI * 88 * (1 - results.overall)}`}
              strokeLinecap="round"
              stroke="currentColor"
              fill="transparent"
              r="88"
              cx="96"
              cy="96"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-6xl font-bold">
              {Math.round(results.overall * 100)}%
            </span>
          </div>
        </div>
        
        <div className="text-3xl font-bold mb-2">OVERALL SIMILARITY</div>
        <div className={`inline-block px-8 py-3 rounded-full font-bold text-xl ${getColor(results.overall)} border-2`}>
          {results.level === 'HIGH' && '⚠️ HIGH PLAGIARISM RISK'}
          {results.level === 'MODERATE' && '⚡ MODERATE SIMILARITY'}
          {results.level === 'LOW' && '✓ LOW SIMILARITY'}
        </div>
      </div>
      
      {/* Dimension Breakdown */}
      <div className="mb-10">
        <h3 className="text-2xl font-bold mb-6">Dimension Breakdown</h3>
        <div className="space-y-5">
          {Object.entries(results.dimensions).map(([dim, score]) => (
            <div key={dim}>
              <div className="flex justify-between mb-2">
                <span className="font-semibold text-lg capitalize">{dim} Structure</span>
                <span className="font-bold text-lg">{Math.round(score * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
                <div 
                  className={`h-6 rounded-full transition-all duration-1000 ease-out ${getBarColor(score)}`}
                  style={{ width: `${score * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Matching Elements */}
      {results.matching_elements && results.matching_elements.length > 0 && (
        <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center">
            <span className="text-2xl mr-2">⚠️</span>
            Matching Semantic Elements
          </h3>
          <ul className="space-y-3">
            {results.matching_elements.map((element, i) => (
              <li key={i} className="flex items-start">
                <span className="text-yellow-600 mr-3 mt-1">•</span>
                <span className="text-gray-800">{element}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

