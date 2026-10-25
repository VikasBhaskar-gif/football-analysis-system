import React, { useRef, useState } from 'react';
import { AlertCircle, FileVideo, FolderOpen, Layers, LoaderCircle, Map, Play, Plus, SkipBack, SkipForward, SlidersHorizontal } from 'lucide-react';

export default function UploadPromptView({ onUploadFile, isUploading, uploadStatus }) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef(null);
  const dragDepth = useRef(0);
  const chooseVideo = () => inputRef.current?.click();

  return (
    <section className={`studio-welcome ${isDragging ? 'is-dragging' : ''}`} aria-label="Match review workspace"
      onDragEnter={(e) => { e.preventDefault(); dragDepth.current += 1; setIsDragging(true); }}
      onDragOver={(e) => e.preventDefault()}
      onDragLeave={(e) => { e.preventDefault(); dragDepth.current = Math.max(0, dragDepth.current - 1); if (!dragDepth.current) setIsDragging(false); }}
      onDrop={(e) => { e.preventDefault(); dragDepth.current = 0; setIsDragging(false); if (e.dataTransfer.files?.[0]) onUploadFile(e.dataTransfer.files[0]); }}>
      <div className="studio-editor-grid">
        <div className="studio-editor-main">
          <section className="studio-viewer" aria-labelledby="viewer-title">
            <div className="studio-panel-bar"><h2 id="viewer-title"><FileVideo size={14} />Viewer</h2><span>NO SOURCE</span></div>
            <div className="studio-empty-canvas">
              <span className="canvas-corner tl" /><span className="canvas-corner tr" /><span className="canvas-corner bl" /><span className="canvas-corner br" />
              <div className="studio-import-focus">
                <span className="studio-source-icon">{isUploading ? <LoaderCircle size={26} className="spin-icon" /> : <FolderOpen size={26} strokeWidth={1.2} />}</span>
                <h2>{isDragging ? 'Drop to import' : isUploading ? 'Preparing video…' : 'Open a match video'}</h2>
                <p>Drop your footage here to start a review.</p>
                <button className="studio-primary" onClick={chooseVideo}><Plus size={15} />{isUploading ? 'Importing…' : 'Import footage'}</button>
                <span className="studio-formats">MP4 · MOV · WEBM · MKV</span>
              </div>
            </div>
            <div className="studio-empty-transport"><span className="studio-timecode">00:00:00:00</span><div><button disabled aria-label="Previous frame"><SkipBack size={14} /></button><button disabled aria-label="Play"><Play size={16} /></button><button disabled aria-label="Next frame"><SkipForward size={14} /></button></div><span className="studio-transport-meta">— fps</span></div>
          </section>
          <section className="studio-timeline" aria-labelledby="timeline-title">
            <div className="studio-panel-bar"><h2 id="timeline-title"><Layers size={14} />Timeline</h2><span>SEQUENCE 01</span></div>
            <div className="studio-empty-ruler"><span>00:00</span></div>
            <div className="studio-empty-track"><span className="studio-track-label">V1</span><div><span>No clips in sequence</span><button onClick={chooseVideo}>Import video <Plus size={12} /></button></div></div>
          </section>
          {uploadStatus && <div className={`studio-upload-status ${uploadStatus.type}`} role={uploadStatus.type === 'error' ? 'alert' : 'status'}><AlertCircle size={16} /><span>{uploadStatus.message}</span></div>}
        </div>
        <aside className="studio-inspector" aria-labelledby="inspector-title">
          <div className="studio-panel-bar"><h2 id="inspector-title"><SlidersHorizontal size={14} />Inspector</h2><span>SOURCE</span></div>
          <div className="studio-inspector-body"><h3>Source details</h3><dl><div><dt>File</dt><dd>—</dd></div><div><dt>Resolution</dt><dd>—</dd></div><div><dt>Frame rate</dt><dd>—</dd></div><div><dt>Duration</dt><dd>—</dd></div></dl>
            <div className="studio-tracking-note"><Map size={18} strokeWidth={1.3} /><h3>Built around the match.</h3><p>Import a video for playback and frame review. Link tracking data to explore players, team shape and passing lanes.</p><span>No sample matches included</span></div>
          </div>
        </aside>
      </div>
      <input ref={inputRef} id="main-video-upload-input" type="file" hidden accept=".mp4,.webm,.mov,.mkv" aria-label="Choose match video" onChange={(e) => e.target.files?.[0] && onUploadFile(e.target.files[0])} />
    </section>
  );
}
