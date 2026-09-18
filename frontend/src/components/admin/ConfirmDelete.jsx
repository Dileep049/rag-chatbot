import React from 'react';
import { AlertTriangle, Trash2 } from 'lucide-react';

export default function ConfirmDelete({ documentName, onConfirm, onCancel, deleting }) {
  if (!documentName) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-md w-full shadow-2xl space-y-5">
        
        <div className="flex items-center space-x-3 text-rose-400">
          <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center shrink-0">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Delete Document</h3>
            <p className="text-xs text-slate-400">Confirm knowledge base removal</p>
          </div>
        </div>

        <div className="text-sm text-slate-300 space-y-2">
          <p>
            Are you sure you want to delete <strong className="text-white font-semibold">{documentName}</strong>?
          </p>
          <p className="text-xs text-slate-400 leading-relaxed">
            This will remove the document file and all associated vector chunks from the RAG knowledge base. The chatbot will no longer use this document.
          </p>
        </div>

        <div className="flex items-center justify-end space-x-3 pt-2 border-t border-slate-800">
          <button
            onClick={onCancel}
            disabled={deleting}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
          >
            Cancel
          </button>
          
          <button
            onClick={onConfirm}
            disabled={deleting}
            className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow-md shadow-rose-600/30 transition flex items-center space-x-1.5"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>{deleting ? 'Deleting...' : 'Delete'}</span>
          </button>
        </div>

      </div>
    </div>
  );
}
