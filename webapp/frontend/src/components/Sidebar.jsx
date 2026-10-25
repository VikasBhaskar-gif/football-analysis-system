import React from 'react';
import { 
  PlaySquare, 
  BarChart3, 
  Layers, 
  Calendar, 
  Settings, 
  Activity,
  HardDrive
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, activeMatch }) {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'video_analysis', label: 'Video Analysis', icon: PlaySquare },
    { id: 'tactical_states', label: 'Tactical States (K=8)', icon: Layers },
    { id: 'possession_events', label: 'Possession & Events', icon: Activity },
    { id: 'settings_storage', label: 'Upload & Storage', icon: HardDrive },
  ];

  return (
    <aside className="sidebar">
      <div>
        <div className="sidebar-header">
          <div className="brand-row">
            <div className="brand-icon">FP</div>
            <div className="brand-text">
              <h1>Tactical Predictor</h1>
              <span>AI FOOTBALL SUITE</span>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                className={`nav-item ${isActive ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-footer">
        <div>ACTIVE CLIP</div>
        <div style={{ color: '#f8fafc', fontWeight: 600, marginTop: 2, fontSize: 12 }}>
          {activeMatch ? activeMatch.title.split('(')[0] : 'No clip loaded'}
        </div>
        <div className="sidebar-status-badge">
          <div className="status-dot"></div>
          <span>PIPELINE READY</span>
        </div>
      </div>
    </aside>
  );
}
