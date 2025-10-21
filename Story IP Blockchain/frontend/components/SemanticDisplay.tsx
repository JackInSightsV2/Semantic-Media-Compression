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
      <div className="semantic-card border-l-2 border-purple-500/50 relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        <div className="relative">
          <div className="flex items-center mb-5">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600/20 to-purple-600/5 rounded-xl flex items-center justify-center text-2xl mr-4">
              📖
            </div>
            <h3 className="text-xl font-bold text-white">
              Narrative Structure
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-1">Genre</div>
              <div className="text-white/90">{semantic_fingerprint.narrative.genre}</div>
            </div>
            <div>
              <div className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-1">Story Arc</div>
              <div className="text-white/90">{semantic_fingerprint.narrative.story_arc}</div>
            </div>
            <div className="md:col-span-2">
              <div className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-1">Themes</div>
              <div className="flex flex-wrap gap-2 mt-2">
                {semantic_fingerprint.narrative.themes.map((theme, i) => (
                  <span key={i} className="px-3 py-1 glass-card text-sm text-purple-300">
                    {theme}
                  </span>
                ))}
              </div>
            </div>
            {!compact && (
              <div className="md:col-span-2">
                <div className="text-xs font-semibold text-purple-400 uppercase tracking-wider mb-1">Progression</div>
                <div className="text-white/90">{semantic_fingerprint.narrative.dramatic_progression}</div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Character Layer */}
      <div className="semantic-card border-l-2 border-blue-500/50 relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        <div className="relative">
          <div className="flex items-center mb-5">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600/20 to-blue-600/5 rounded-xl flex items-center justify-center text-2xl mr-4">
              👤
            </div>
            <h3 className="text-xl font-bold text-white">
              Character Essence
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">Archetype</div>
              <div className="text-white/90">{semantic_fingerprint.characters.protagonist.archetype}</div>
            </div>
            <div>
              <div className="text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">Traits</div>
              <div className="flex flex-wrap gap-2 mt-2">
                {semantic_fingerprint.characters.protagonist.traits.map((trait, i) => (
                  <span key={i} className="px-3 py-1 glass-card text-sm text-blue-300">
                    {trait}
                  </span>
                ))}
              </div>
            </div>
            {!compact && (
              <div className="md:col-span-2">
                <div className="text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">Character Arc</div>
                <div className="text-white/90">{semantic_fingerprint.characters.protagonist.arc}</div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Thematic Layer */}
      <div className="semantic-card border-l-2 border-cyan-500/50 relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        <div className="relative">
          <div className="flex items-center mb-5">
            <div className="w-12 h-12 bg-gradient-to-br from-cyan-600/20 to-cyan-600/5 rounded-xl flex items-center justify-center text-2xl mr-4">
              💭
            </div>
            <h3 className="text-xl font-bold text-white">
              Thematic Content
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-1">Primary Theme</div>
              <div className="text-white/90">{semantic_fingerprint.themes.primary}</div>
            </div>
            <div>
              <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-1">Secondary Themes</div>
              <div className="flex flex-wrap gap-2 mt-2">
                {semantic_fingerprint.themes.secondary.slice(0, compact ? 2 : undefined).map((theme, i) => (
                  <span key={i} className="px-3 py-1 glass-card text-sm text-cyan-300">
                    {theme}
                  </span>
                ))}
              </div>
            </div>
            {!compact && (
              <>
                <div>
                  <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-1">Emotional Tone</div>
                  <div className="text-white/90">{semantic_fingerprint.themes.emotional_tone}</div>
                </div>
                <div>
                  <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-1">Visual Metaphors</div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {semantic_fingerprint.themes.visual_metaphors.map((metaphor, i) => (
                      <span key={i} className="px-3 py-1 glass-card text-sm text-cyan-300">
                        {metaphor}
                      </span>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
