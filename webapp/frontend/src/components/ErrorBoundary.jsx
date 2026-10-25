import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('[TacticalPredictor ErrorBoundary Caught]:', error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            padding: '24px',
            backgroundColor: '#0f172a',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            borderRadius: '8px',
            color: '#f8fafc',
            margin: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <AlertTriangle size={22} color="#ef4444" />
            <h3 style={{ margin: 0, fontSize: '15px', color: '#f87171' }}>
              Tactical Interface Recovery Notice
            </h3>
          </div>
          <p style={{ margin: 0, fontSize: '12px', color: '#94a3b8', lineHeight: 1.5 }}>
            A component encounter an issue during overlay or state rendering. The application has safely prevented a black screen.
          </p>
          {this.state.error && (
            <pre
              style={{
                backgroundColor: 'rgba(0, 0, 0, 0.4)',
                padding: '8px 12px',
                borderRadius: '4px',
                fontSize: '11px',
                color: '#fca5a5',
                overflowX: 'auto',
                margin: 0,
              }}
            >
              {this.state.error.toString()}
            </pre>
          )}
          <div style={{ display: 'flex', gap: '10px', marginTop: '6px' }}>
            <button
              onClick={this.handleReset}
              className="btn btn-primary"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '12px', padding: '6px 14px' }}
            >
              <RefreshCw size={13} />
              <span>Recover Component</span>
            </button>
            <button
              onClick={() => window.location.reload()}
              className="btn"
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.08)',
                color: '#e2e8f0',
                fontSize: '12px',
                padding: '6px 14px',
              }}
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
