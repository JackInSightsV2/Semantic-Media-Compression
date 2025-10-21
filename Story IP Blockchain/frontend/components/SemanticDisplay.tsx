interface SemanticData {
  content_id: string;
  semantic_fingerprint: {
    narrative: {
      genre: string;
      story_arc: string;
      themes: string[];
      dramatic_progression: string;
    };
    characters: {
      protagonist: {
        archetype: string;
        traits: string[];
        arc: string;
      };
    };
    themes: {
      primary: string;
      secondary: string[];
      emotional_tone: string;
      visual_metaphors: string[];
    };
  };
}

interface Props {
  data: SemanticData;
  compact?: boolean;
}

export default function SemanticDisplay({ data, compact = false }: Props) {
  const { semantic_fingerprint } = data;
  
  return (
    <div className="space-y-4">
      {/* Narrative Layer */}
      <div className="bg-gradient-to-r from-purple-50 to-purple-100 border-l-4 border-purple-500 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">📖</span>
          <h3 className="text-xl font-bold text-purple-700">
            Narrative Structure
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-semibold text-gray-700">Genre:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.narrative.genre}</p>
          </div>
          <div>
            <span className="font-semibold text-gray-700">Story Arc:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.narrative.story_arc}</p>
          </div>
          <div className="md:col-span-2">
            <span className="font-semibold text-gray-700">Themes:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.narrative.themes.join(', ')}</p>
          </div>
          {!compact && (
            <div className="md:col-span-2">
              <span className="font-semibold text-gray-700">Progression:</span>
              <p className="text-gray-900 mt-1">{semantic_fingerprint.narrative.dramatic_progression}</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Character Layer */}
      <div className="bg-gradient-to-r from-blue-50 to-blue-100 border-l-4 border-blue-500 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">👤</span>
          <h3 className="text-xl font-bold text-blue-700">
            Character Essence
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-semibold text-gray-700">Archetype:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.characters.protagonist.archetype}</p>
          </div>
          <div>
            <span className="font-semibold text-gray-700">Traits:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.characters.protagonist.traits.join(', ')}</p>
          </div>
          {!compact && (
            <div className="md:col-span-2">
              <span className="font-semibold text-gray-700">Arc:</span>
              <p className="text-gray-900 mt-1">{semantic_fingerprint.characters.protagonist.arc}</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Thematic Layer */}
      <div className="bg-gradient-to-r from-pink-50 to-pink-100 border-l-4 border-pink-500 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">💭</span>
          <h3 className="text-xl font-bold text-pink-700">
            Thematic Content
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-semibold text-gray-700">Primary:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.themes.primary}</p>
          </div>
          <div>
            <span className="font-semibold text-gray-700">Secondary:</span>
            <p className="text-gray-900 mt-1">{semantic_fingerprint.themes.secondary.join(', ')}</p>
          </div>
          {!compact && (
            <>
              <div>
                <span className="font-semibold text-gray-700">Tone:</span>
                <p className="text-gray-900 mt-1">{semantic_fingerprint.themes.emotional_tone}</p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Visual Metaphors:</span>
                <p className="text-gray-900 mt-1">{semantic_fingerprint.themes.visual_metaphors.join(', ')}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

