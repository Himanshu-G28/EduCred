import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught error in EduCred application:", error, errorInfo);
    this.setState({ errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
          <div className="max-w-2xl mx-auto bg-slate-800/80 border border-rose-500/40 rounded-2xl p-6 shadow-2xl space-y-4">
            <h1 className="text-xl font-bold text-rose-400">Application Error Encountered</h1>
            <p className="text-sm text-slate-300">
              An unexpected error occurred while rendering the page:
            </p>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-700 font-mono text-xs text-rose-300 overflow-auto">
              {this.state.error?.toString()}
            </div>
            <pre className="bg-slate-950 p-4 rounded-xl border border-slate-700 font-mono text-[11px] text-slate-400 overflow-auto max-h-64">
              {this.state.errorInfo?.componentStack || this.state.error?.stack}
            </pre>
            <button
              onClick={() => window.location.reload()}
              className="bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold px-4 py-2 rounded-xl"
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

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
);
