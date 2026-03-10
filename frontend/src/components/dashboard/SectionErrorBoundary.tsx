"use client";

import { Component, ReactNode } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface Props {
  children: ReactNode;
  section: string;
  onRetry?: () => void;
}

interface State {
  hasError: boolean;
  error: string | null;
}

export default class SectionErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error: error.message };
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    this.props.onRetry?.();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 text-red-500 flex-shrink-0" />
            <p className="text-sm text-red-700">
              Failed to load {this.props.section}.
            </p>
            {this.props.onRetry && (
              <button
                onClick={this.handleRetry}
                className="ml-auto flex items-center gap-1 text-xs text-red-600 hover:text-red-800"
              >
                <RefreshCw className="h-3 w-3" />
                Retry
              </button>
            )}
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
