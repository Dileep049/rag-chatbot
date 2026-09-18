import React from 'react';
import { CheckCircle2, Clock, XCircle } from 'lucide-react';

export default function DocumentStatus({ status }) {
  const normalized = (status || 'indexed').toLowerCase();

  if (normalized === 'processing') {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
        <Clock className="w-3 h-3 mr-1 animate-spin" /> Processing...
      </span>
    );
  }

  if (normalized === 'failed') {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">
        <XCircle className="w-3 h-3 mr-1" /> ✕ Failed
      </span>
    );
  }

  return (
    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
      <CheckCircle2 className="w-3 h-3 mr-1" /> ✓ Indexed
    </span>
  );
}
