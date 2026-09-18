import React from 'react';
import { FileText, RefreshCw, Trash2, Calendar, Layers } from 'lucide-react';
import DocumentStatus from './DocumentStatus';

export default function DocumentCard({ doc, onReindex, onDelete, reindexing }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3 shadow-sm md:hidden">
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-2 font-semibold text-white text-sm truncate pr-2">
          <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
          <span className="truncate">{doc.name}</span>
        </div>
        <DocumentStatus status={doc.status} />
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
        <div>
          <span className="text-slate-500 font-medium block">Category</span>
          <span className="text-indigo-300 capitalize">{doc.category || 'General'}</span>
        </div>
        <div>
          <span className="text-slate-500 font-medium block">File Type</span>
          <span className="uppercase text-slate-300">{doc.type || 'PDF'}</span>
        </div>
        <div>
          <span className="text-slate-500 font-medium block">Pages</span>
          <span className="text-slate-300">{doc.pages || 1}</span>
        </div>
        <div>
          <span className="text-slate-500 font-medium block">Chunks</span>
          <span className="text-slate-300">{doc.chunks || 0}</span>
        </div>
      </div>

      <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
        <span className="flex items-center gap-1">
          <Calendar className="w-3 h-3" /> {doc.uploaded_at || 'Indexed'}
        </span>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onReindex(doc.name)}
            disabled={reindexing === doc.name}
            className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 text-xs border border-slate-700 transition flex items-center space-x-1"
          >
            <RefreshCw className={`w-3 h-3 ${reindexing === doc.name ? 'animate-spin' : ''}`} />
            <span>Re-index</span>
          </button>

          <button
            onClick={() => onDelete(doc.name)}
            className="px-2.5 py-1 rounded-lg bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 text-xs border border-rose-800/50 transition flex items-center space-x-1"
          >
            <Trash2 className="w-3 h-3" />
            <span>Delete</span>
          </button>
        </div>
      </div>
    </div>
  );
}
