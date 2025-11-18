import React, { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { DistillPanel } from './components/DistillPanel';
import { InflatePanel } from './components/InflatePanel';
import { DistillAndInflatePanel } from './components/DistillAndInflatePanel';
import { ComparePanel } from './components/ComparePanel';
import { RunsList } from './components/RunsList';
import { RunDetails } from './components/RunDetails';
import { CleanupPanel } from './components/CleanupPanel';
import './styles/App.css';

type Tab = 'upload' | 'distill' | 'inflate' | 'distill-inflate' | 'compare' | 'runs' | 'details' | 'cleanup';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('upload');

  const tabs: { id: Tab; label: string }[] = [
    { id: 'upload', label: 'Upload File' },
    { id: 'distill', label: 'Distill' },
    { id: 'inflate', label: 'Inflate' },
    { id: 'distill-inflate', label: 'Distill & Inflate' },
    { id: 'compare', label: 'Compare' },
    { id: 'runs', label: 'Runs List' },
    { id: 'details', label: 'Run Details' },
    { id: 'cleanup', label: 'Cleanup' }
  ];

  return (
    <div className="app">
      <header>
        <h1>Semantic Media Compression - Testing Frontend</h1>
      </header>
      <nav>
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>
      <main>
        {activeTab === 'upload' && <FileUpload />}
        {activeTab === 'distill' && <DistillPanel />}
        {activeTab === 'inflate' && <InflatePanel />}
        {activeTab === 'distill-inflate' && <DistillAndInflatePanel />}
        {activeTab === 'compare' && <ComparePanel />}
        {activeTab === 'runs' && <RunsList />}
        {activeTab === 'details' && <RunDetails />}
        {activeTab === 'cleanup' && <CleanupPanel />}
      </main>
    </div>
  );
}

export default App;

