import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  FileText, 
  Trash2, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle, 
  FolderPlus,
  Database,
  Loader2,
  FileCheck
} from 'lucide-react';
import { getDocuments, uploadDocument, deleteDocument, reindexDocuments } from '../services/api';

export default function DocumentManagement({ categories }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [reindexing, setReindexing] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('aadhaar');
  const [fileToUpload, setFileToUpload] = useState(null);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch indexed documents from ChromaDB backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFileToUpload(e.target.files[0]);
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!fileToUpload) return;

    setUploading(true);
    setMessage(null);
    setError(null);

    try {
      const res = await uploadDocument(fileToUpload, selectedCategory);
      setMessage(res.message || 'Document uploaded and indexed successfully!');
      setFileToUpload(null);
      // Reset file input element
      e.target.reset();
      fetchDocuments();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to upload document.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docName) => {
    if (!window.confirm(`Are you sure you want to delete document '${docName}' from the RAG database?`)) {
      return;
    }

    setMessage(null);
    setError(null);

    try {
      await deleteDocument(docName);
      setMessage(`Document '${docName}' deleted successfully.`);
      fetchDocuments();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to delete document.');
    }
  };

  const handleReindex = async () => {
    setReindexing(true);
    setMessage(null);
    setError(null);

    try {
      const res = await reindexDocuments();
      setMessage(res.message || 'Re-indexed knowledge base successfully!');
      fetchDocuments();
    } catch (err) {
      console.error(err);
      setError('Failed to re-index documents.');
    } finally {
      setReindexing(false);
    }
  };

  return (
    <div className="flex-1 bg-slate-950 p-4 sm:p-8 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl">
          <div>
            <div className="flex items-center space-x-2">
              <Database className="w-6 h-6 text-indigo-400" />
              <h2 className="text-xl sm:text-2xl font-bold text-slate-100">
                Document Management Hub
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Upload official government & police procedures, manage indexed files, and refresh ChromaDB vectors.
            </p>
          </div>

          <button
            onClick={handleReindex}
            disabled={reindexing}
            className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 text-xs sm:text-sm font-semibold transition-all shadow-md shrink-0"
          >
            <RefreshCw className={`w-4 h-4 ${reindexing ? 'animate-spin' : ''}`} />
            <span>{reindexing ? 'Re-indexing Vectorstore...' : 'Re-index Knowledge Base'}</span>
          </button>
        </div>

        {/* Banners */}
        {message && (
          <div className="flex items-center space-x-3 p-4 bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 rounded-2xl">
            <CheckCircle2 className="w-5 h-5 shrink-0" />
            <span className="text-sm font-medium">{message}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center space-x-3 p-4 bg-rose-950/40 border border-rose-800/60 text-rose-300 rounded-2xl">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <span className="text-sm font-medium">{error}</span>
          </div>
        )}

        {/* Upload Form Section */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl">
          <div className="flex items-center space-x-2 text-base font-semibold text-slate-200 mb-4">
            <FolderPlus className="w-5 h-5 text-indigo-400" />
            <span>Upload New Official Document</span>
          </div>

          <form onSubmit={handleUploadSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              
              {/* Category Select */}
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">
                  Select Category
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-sm focus:outline-none focus:border-indigo-500"
                >
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* File Input */}
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">
                  Select File (.pdf, .docx, .txt)
                </label>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={handleFileChange}
                  required
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-300 text-xs file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500"
                />
              </div>

            </div>

            <button
              type="submit"
              disabled={!fileToUpload || uploading}
              className={`flex items-center justify-center space-x-2 w-full sm:w-auto px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200 ${
                fileToUpload && !uploading
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-indigo-600/30 hover:opacity-90'
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed'
              }`}
            >
              {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
              <span>{uploading ? 'Processing & Indexing Document...' : 'Upload & Index Document'}</span>
            </button>
          </form>
        </div>

        {/* Document Table Section */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2 text-base font-semibold text-slate-200">
              <FileCheck className="w-5 h-5 text-emerald-400" />
              <span>Indexed Documents ({documents.length})</span>
            </div>
            <button
              onClick={fetchDocuments}
              className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Refresh List</span>
            </button>
          </div>

          {loading ? (
            <div className="flex justify-center p-8 text-slate-400">
              <Loader2 className="w-6 h-6 animate-spin text-indigo-400" />
            </div>
          ) : documents.length === 0 ? (
            <div className="text-center p-8 text-slate-500 text-sm">
              No documents indexed yet. Upload a document or click "Re-index Knowledge Base".
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs sm:text-sm text-slate-300">
                <thead className="bg-slate-950 text-slate-400 font-semibold uppercase tracking-wider text-[11px] border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Document Name</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Vector Chunks</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {documents.map((doc, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-3.5 px-4 font-medium text-slate-100 flex items-center space-x-2">
                        <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
                        <span className="truncate max-w-xs">{doc.document}</span>
                      </td>
                      <td className="py-3.5 px-4 capitalize">
                        <span className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-300">
                          {doc.category}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-slate-400">
                        {doc.chunk_count} chunks
                      </td>
                      <td className="py-3.5 px-4">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          ● Indexed
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={() => handleDelete(doc.document)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
                          title="Delete Document"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
