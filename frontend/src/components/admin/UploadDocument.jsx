import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2, RefreshCw } from 'lucide-react';
import { uploadDocument } from '../../services/api';

const CATEGORY_OPTIONS = [
  { id: 'aadhaar', name: 'Aadhaar' },
  { id: 'pension', name: 'Pension' },
  { id: 'police', name: 'Police' },
  { id: 'vehicle', name: 'Vehicle' },
  { id: 'pan', name: 'PAN' },
  { id: 'driving_license', name: 'Driving Licence' },
  { id: 'schemes', name: 'Government Schemes' },
  { id: 'other', name: 'Other Citizen Services' }
];

export default function UploadDocument({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('aadhaar');
  const [uploading, setUploading] = useState(false);
  const [uploadStep, setUploadStep] = useState(''); // Uploading..., Chunking..., Embedding...
  const [error, setError] = useState(null);
  const [duplicateConflict, setDuplicateConflict] = useState(null); // File object if duplicate 409
  const [successMsg, setSuccessMsg] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    validateAndSetFile(selected);
  };

  const validateAndSetFile = (selectedFile) => {
    setError(null);
    setSuccessMsg(null);
    setDuplicateConflict(null);

    if (!selectedFile) return;

    const ext = selectedFile.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt'].includes(ext)) {
      setError('Unsupported file type. Please upload PDF, DOCX or TXT files.');
      setFile(null);
      return;
    }

    if (selectedFile.size === 0) {
      setError('File is empty. Please select a valid document.');
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUpload = async (overwrite = false) => {
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccessMsg(null);
    setDuplicateConflict(null);
    setUploadStep('Uploading & indexing document into ChromaDB...');

    try {
      const res = await uploadDocument(file, category, overwrite);
      setSuccessMsg(res.message || `✓ Document '${file.name}' indexed successfully.`);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      if (err.response?.status === 409) {
        setDuplicateConflict(file);
      } else {
        const detail = err.response?.data?.detail || 'Unable to process this document. Please check the file and try again.';
        setError(detail);
      }
    } finally {
      setUploading(false);
      setUploadStep('');
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-6">
      
      <div className="flex items-center space-x-2 pb-2 border-b border-slate-800">
        <Upload className="w-5 h-5 text-indigo-400" />
        <h2 className="text-base sm:text-lg font-bold text-white">Upload Official Document</h2>
      </div>

      {/* Drag & Drop Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
          file 
            ? 'border-indigo-500 bg-indigo-500/10' 
            : 'border-slate-700 hover:border-slate-600 bg-slate-950/50 hover:bg-slate-950'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          className="hidden"
        />

        {file ? (
          <div className="space-y-2">
            <FileText className="w-10 h-10 text-indigo-400 mx-auto" />
            <div className="font-semibold text-slate-100">{file.name}</div>
            <div className="text-xs text-slate-400">
              {(file.size / (1024 * 1024)).toFixed(2)} MB • Click or drag to replace
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <Upload className="w-10 h-10 text-slate-500 mx-auto" />
            <div className="text-sm font-medium text-slate-200">
              Drag & Drop File Here <span className="text-slate-500">OR</span>
            </div>
            <button
              type="button"
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-indigo-400 text-xs font-semibold border border-slate-700 transition"
            >
              Choose File (.PDF, .DOCX, .TXT)
            </button>
          </div>
        )}
      </div>

      {/* Category Dropdown & Submit Button */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-end">
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1.5">
            Document Category
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            disabled={uploading}
            className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
          >
            {CATEGORY_OPTIONS.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={() => handleUpload(false)}
          disabled={!file || uploading}
          className={`w-full py-2.5 px-4 rounded-xl font-semibold text-sm flex items-center justify-center space-x-2 transition ${
            file && !uploading
              ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/30'
              : 'bg-slate-800 text-slate-500 cursor-not-allowed'
          }`}
        >
          {uploading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Indexing...</span>
            </>
          ) : (
            <>
              <Upload className="w-4 h-4" />
              <span>Upload & Index Document</span>
            </>
          )}
        </button>
      </div>

      {/* Progress Status Message */}
      {uploadStep && (
        <div className="flex items-center space-x-2 text-xs text-indigo-400 p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
          <Loader2 className="w-4 h-4 animate-spin shrink-0" />
          <span>{uploadStep}</span>
        </div>
      )}

      {/* Success Message */}
      {successMsg && (
        <div className="flex items-center space-x-2 text-xs text-emerald-300 p-3 bg-emerald-950/40 border border-emerald-800/60 rounded-xl">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="flex items-center space-x-2 text-xs text-rose-300 p-3 bg-rose-950/40 border border-rose-800/60 rounded-xl">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Duplicate File Conflict Dialog */}
      {duplicateConflict && (
        <div className="p-4 bg-amber-950/40 border border-amber-800/60 rounded-2xl space-y-3">
          <div className="flex items-start space-x-2 text-xs text-amber-200">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold text-amber-100">This document already exists in the knowledge base.</strong>
              <p className="mt-0.5">Would you like to replace the existing vectors and re-index this file?</p>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-1">
            <button
              onClick={() => setDuplicateConflict(null)}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700"
            >
              Cancel
            </button>
            <button
              onClick={() => handleUpload(true)}
              className="px-3.5 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold shadow-sm"
            >
              Replace & Re-index
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
