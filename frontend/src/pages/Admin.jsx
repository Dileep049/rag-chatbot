import React, { useState, useEffect } from 'react';
import AdminHeader from '../components/admin/AdminHeader';
import UploadDocument from '../components/admin/UploadDocument';
import DocumentTable from '../components/admin/DocumentTable';
import ConfirmDelete from '../components/admin/ConfirmDelete';
import { getDocuments, deleteDocument, reindexSingleDocument } from '../services/api';
import { FileText, CheckCircle2, Clock, XCircle, AlertCircle, Sparkles } from 'lucide-react';

export default function AdminPage({ onReturnToChat }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [reindexing, setReindexing] = useState(null);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (err) {
      console.error(err);
      setError('Unable to load documents from server. Please check backend connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleReindex = async (docName) => {
    setReindexing(docName);
    setError(null);
    try {
      const res = await reindexSingleDocument(docName);
      setNotification(`✓ Document '${docName}' re-indexed successfully.`);
      fetchDocuments();
    } catch (err) {
      console.error(err);
      setError(`Failed to re-index document '${docName}'.`);
    } finally {
      setReindexing(null);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    setError(null);
    try {
      await deleteDocument(deleteTarget);
      setNotification(`✓ Document '${deleteTarget}' deleted from knowledge base.`);
      setDeleteTarget(null);
      fetchDocuments();
    } catch (err) {
      console.error(err);
      setError(`Failed to delete document '${deleteTarget}'.`);
    } finally {
      setDeleting(false);
    }
  };

  // Compute dashboard summary stats
  const totalDocs = documents.length;
  const indexedDocs = documents.filter((d) => (d.status || '').toLowerCase() === 'indexed').length || totalDocs;
  const pendingDocs = 0;
  const failedDocs = 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      
      {/* Admin Header */}
      <AdminHeader
        onRefresh={fetchDocuments}
        loading={loading}
        onReturnToChat={onReturnToChat}
      />

      {/* Main Content */}
      <div className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 space-y-8">
        
        {/* Notification Banner */}
        {notification && (
          <div className="flex items-center justify-between p-4 bg-emerald-950/50 border border-emerald-800/80 text-emerald-200 rounded-2xl animate-fadeIn shadow-sm">
            <div className="flex items-center space-x-2 text-xs sm:text-sm">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <span>{notification}</span>
            </div>
            <button
              onClick={() => setNotification(null)}
              className="text-xs text-emerald-400 hover:text-white underline font-medium"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Global Error Banner */}
        {error && (
          <div className="flex items-center justify-between p-4 bg-rose-950/50 border border-rose-800/80 text-rose-200 rounded-2xl animate-fadeIn shadow-sm">
            <div className="flex items-center space-x-2 text-xs sm:text-sm">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-xs text-rose-400 hover:text-white underline font-medium"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Dashboard Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Documents</span>
              <FileText className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-white mt-2 font-mono">{totalDocs}</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Indexed</span>
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-emerald-400 mt-2 font-mono">{indexedDocs}</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Pending</span>
              <Clock className="w-5 h-5 text-amber-400" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-amber-400 mt-2 font-mono">{pendingDocs}</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Failed</span>
              <XCircle className="w-5 h-5 text-rose-400" />
            </div>
            <div className="text-2xl sm:text-3xl font-bold text-rose-400 mt-2 font-mono">{failedDocs}</div>
          </div>

        </div>

        {/* Upload Document Section */}
        <UploadDocument onUploadSuccess={fetchDocuments} />

        {/* Document Table Section */}
        <DocumentTable
          documents={documents}
          onReindex={handleReindex}
          onDelete={(docName) => setDeleteTarget(docName)}
          reindexing={reindexing}
        />

      </div>

      {/* Confirm Delete Modal */}
      <ConfirmDelete
        documentName={deleteTarget}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setDeleteTarget(null)}
        deleting={deleting}
      />

    </div>
  );
}
