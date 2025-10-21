import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-purple-600">
            Semantic Copyright Guardian
          </h1>
        </div>
      </nav>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold mb-6 text-gray-900">
            Protect Your Creative Work with <br />
            <span className="text-purple-600">Semantic Fingerprints</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Mathematical proof of semantic plagiarism on Story Protocol blockchain.
            Detect copycats who steal your <em>meaning</em>, not just your pixels.
          </p>
        </div>
        
        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <Link href="/register" className="card group">
            <div className="text-5xl mb-4">📝</div>
            <h3 className="text-2xl font-semibold mb-3 group-hover:text-purple-600 transition-colors">
              Register IP
            </h3>
            <p className="text-gray-600">
              Register your semantic fingerprint on Story Protocol blockchain for immutable proof of ownership
            </p>
          </Link>
          
          <Link href="/compare" className="card group">
            <div className="text-5xl mb-4">🔍</div>
            <h3 className="text-2xl font-semibold mb-3 group-hover:text-purple-600 transition-colors">
              Detect Plagiarism
            </h3>
            <p className="text-gray-600">
              Compare semantic fingerprints across multiple dimensions to find sophisticated copycats
            </p>
          </Link>
          
          <Link href="/dispute" className="card group">
            <div className="text-5xl mb-4">⚖️</div>
            <h3 className="text-2xl font-semibold mb-3 group-hover:text-purple-600 transition-colors">
              File Dispute
            </h3>
            <p className="text-gray-600">
              Submit plagiarism evidence to Story Protocol with mathematical proof of semantic theft
            </p>
          </Link>
        </div>
        
        {/* How It Works */}
        <div className="bg-white rounded-2xl shadow-xl p-10">
          <h3 className="text-3xl font-bold mb-8 text-center text-gray-900">
            How It Works
          </h3>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-2xl font-bold text-purple-600 mx-auto mb-4">
                1
              </div>
              <h4 className="font-semibold mb-2">Extract Semantics</h4>
              <p className="text-sm text-gray-600">
                Multi-layer analysis captures narrative, characters, and themes
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-2xl font-bold text-purple-600 mx-auto mb-4">
                2
              </div>
              <h4 className="font-semibold mb-2">Register on Blockchain</h4>
              <p className="text-sm text-gray-600">
                Store immutable fingerprint on Story Protocol
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-2xl font-bold text-purple-600 mx-auto mb-4">
                3
              </div>
              <h4 className="font-semibold mb-2">Compare & Detect</h4>
              <p className="text-sm text-gray-600">
                Mathematical similarity analysis across dimensions
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-2xl font-bold text-purple-600 mx-auto mb-4">
                4
              </div>
              <h4 className="font-semibold mb-2">File Dispute</h4>
              <p className="text-sm text-gray-600">
                Submit cryptographic proof to blockchain for resolution
              </p>
            </div>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
          <p>Powered by Story Protocol • Built for Encode Hackathon</p>
          <p className="mt-2 text-sm">
            Based on extensive semantic compression research
          </p>
        </div>
      </footer>
    </div>
  );
}
