import React, { useState } from 'react';
import { UploadCloud, FileVideo, Shield, Target, Calendar, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';

export default function UploadPromptView({ onUploadFile, isUploading, uploadStatus }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onUploadFile(e.dataTransfer.files[0]);
    }
  };

  const handleSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onUploadFile(e.target.files[0]);
    }
  };

  return (
    <div className="upload-empty-state">
      <div
        className={`upload-box-hero ${isDragging ? 'drag-over' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById('main-video-upload-input').click()}
      >
        <input
          id="main-video-upload-input"
          type="file"
          accept="video/mp4,video/webm,video/quicktime,video/x-matroska"
          style={{ display: 'none' }}
          onChange={handleSelect}
        />

        <div style={{
          width: 72,
          height: 72,
          borderRadius: '50%',
          background: 'rgba(0, 229, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 20px',
          border: '1px solid rgba(0, 229, 255, 0.35)',
          boxShadow: '0 0 24px rgba(0, 229, 255, 0.2)',
        }}>
          <UploadCloud size={36} color="#00e5ff" />
        </div>

        <h2 style={{ fontSize: 22, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 8, letterSpacing: '-0.3px' }}>
          {isUploading ? 'Loading and Probing Video...' : 'Upload Football Match Video'}
        </h2>
        
        <p style={{ color: 'var(--text-secondary)', fontSize: 13, maxWidth: 480, margin: '0 auto 24px', lineHeight: 1.6 }}>
          Drag and drop your local match video file here, or click to browse.
          Supports MP4, WebM, and MOV formats.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button 
            type="button" 
            className="btn btn-primary" 
            style={{ padding: '10px 24px', fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              document.getElementById('main-video-upload-input').click();
            }}
          >
            <FileVideo size={16} />
            <span>Select Local Video File</span>
          </button>
        </div>

        {uploadStatus && (
          <div style={{
            marginTop: 20,
            padding: '10px 16px',
            borderRadius: 'var(--radius-md)',
            fontSize: 12,
            backgroundColor: uploadStatus.type === 'error' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(0, 229, 255, 0.1)',
            border: `1px solid ${uploadStatus.type === 'error' ? 'var(--accent-red)' : 'var(--accent-cyan)'}`,
            color: uploadStatus.type === 'error' ? 'var(--accent-red)' : 'var(--accent-cyan)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8
          }}>
            {uploadStatus.type === 'error' ? <AlertTriangle size={15} /> : <CheckCircle2 size={15} />}
            <span>{uploadStatus.message}</span>
          </div>
        )}
      </div>

      {/* Feature capabilities grid below upload box */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
        gap: 16,
        maxWidth: 720,
        width: '100%',
        marginTop: 32,
      }}>
        <div className="card" style={{ padding: '14px 16px', textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--accent-cyan)', fontSize: 13, fontWeight: 700, marginBottom: 4 }}>
            <FileVideo size={15} />
            <span>Local Playback</span>
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
            Direct browser playback with draggable timeline scrubber and frame stepping.
          </div>
        </div>

        <div className="card" style={{ padding: '14px 16px', textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--accent-green)', fontSize: 13, fontWeight: 700, marginBottom: 4 }}>
            <Shield size={15} />
            <span>Possession Dynamics</span>
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
            Identifies controlled carries, pressure tiers, and defensive tackles.
          </div>
        </div>

        <div className="card" style={{ padding: '14px 16px', textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--accent-amber)', fontSize: 13, fontWeight: 700, marginBottom: 4 }}>
            <Target size={15} />
            <span>Tactical Options</span>
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
            Evaluates forward progression, overlaps, wing switches, and direct shots on goal.
          </div>
        </div>

        <div className="card" style={{ padding: '14px 16px', textAlign: 'left' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--accent-purple)', fontSize: 13, fontWeight: 700, marginBottom: 4 }}>
            <Calendar size={15} />
            <span>Chronological Events</span>
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
            Synthesizes passes, turnovers, and carries into an interactive timeline.
          </div>
        </div>
      </div>
    </div>
  );
}
