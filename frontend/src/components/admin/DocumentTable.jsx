import React, { useState } from 'react';
import { Search, Filter, RefreshCw, Trash2, FileText, Database } from 'lucide-react';
import DocumentStatus from './DocumentStatus';
import DocumentCard from './DocumentCard';

const FILTER_CATEGORIES = [
  { id: 'all', label: 'All' },
  { id: 'aadhaar', label: 'Aadhaar' },
  { id: 'pension', label: 'Pension' },
  { id: 'police', label: 'Police' },
  { id: 'vehicle', label: 'Vehicle' },
  { id: 'pan', label: 'PAN' },
  { id: 'driving_license', label: 'Driving Licence' },
  { id: 'schemes', label: 'Government Schemes' },
  { id: 'other', label: 'Other' }
];

export default function DocumentTable({ 
  documents, 
  onReindex, 
  onDelete, 
  reindexing 
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');

  const filteredDocs = documents.filter((doc) => {
    const matchesSearch = doc.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = selectedFilter === 'all' 
      || (doc.category && doc.category.toLowerCase() === selectedFilter.toLowerCase());
    return matchesSearch && matchesCat;
  });

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-5">
      
      {/* Table Header & Search Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-400" />
            Knowledge Base Documents ({filteredDocs.length})
          </h2>
          <p className="text-xs text-slate-400">
            Manage official documents indexed in ChromaDB vector storage
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative max-w-xs w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search documents..."
            className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 text-xs focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-500 font-medium pr-1 flex items-center gap-1 shrink-0">
          <Filter className="w-3.5 h-3.5" /> Filter:
        </span>
        {FILTER_CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedFilter(cat.id)}
            className={`px-3 py-1.5 rounded-xl font-medium shrink-0 transition ${
              selectedFilter === cat.id
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Mobile Card List View */}
      <div className="space-y-3 md:hidden">
        {filteredDocs.length === 0 ? (
          <div className="text-center py-8 text-slate-500 text-xs">
            No matching documents found.
          </div>
        ) : (
          filteredDocs.map((doc, idx) => (
            <DocumentCard
              key={idx}
              doc={doc}
              onReindex={onReindex}
              onDelete={onDelete}
              reindexing={reindexing}
            />
          ))
        )}
      </div>

      {/* Desktop Responsive Table View */}
      <div className="hidden md:block overflow-x-auto border border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950 text-slate-400 uppercase font-semibold border-b border-slate-800">
            <tr>
              <th className="py-3.5 px-4">Document Name</th>
              <th className="py-3.5 px-4">Category</th>
              <th className="py-3.5 px-4">Type</th>
              <th className="py-3.5 px-4">Pages</th>
              <th className="py-3.5 px-4">Chunks</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4">Uploaded Date</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-800/60 bg-slate-900/50">
            {filteredDocs.length === 0 ? (
              <tr>
                <td colSpan="8" className="py-8 text-center text-slate-500">
                  No matching documents found in the knowledge base.
                </td>
              </tr>
            ) : (
              filteredDocs.map((doc, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition">
                  
                  {/* Name */}
                  <td className="py-3 px-4 font-semibold text-white">
                    <div className="flex items-center space-x-2">
                      <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
                      <span className="truncate max-w-xs">{doc.name}</span>
                    </div>
                  </td>

                  {/* Category */}
                  <td className="py-3 px-4 capitalize text-indigo-300 font-medium">
                    {doc.category || 'General'}
                  </td>

                  {/* Type */}
                  <td className="py-3 px-4 uppercase text-slate-400 font-mono">
                    {doc.type || 'pdf'}
                  </td>

                  {/* Pages */}
                  <td className="py-3 px-4">{doc.pages || 1}</td>

                  {/* Chunks */}
                  <td className="py-3 px-4 font-mono">{doc.chunks || 0}</td>

                  {/* Status */}
                  <td className="py-3 px-4">
                    <DocumentStatus status={doc.status} />
                  </td>

                  {/* Date */}
                  <td className="py-3 px-4 text-slate-400">{doc.uploaded_at || 'Indexed'}</td>

                  {/* Actions */}
                  <td className="py-3 px-4 text-right space-x-2">
                    <button
                      onClick={() => onReindex(doc.name)}
                      disabled={reindexing === doc.name}
                      className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 text-xs border border-slate-700 transition inline-flex items-center space-x-1"
                    >
                      <RefreshCw className={`w-3 h-3 ${reindexing === doc.name ? 'animate-spin' : ''}`} />
                      <span>Re-index</span>
                    </button>

                    <button
                      onClick={() => onDelete(doc.name)}
                      className="px-2.5 py-1 rounded-lg bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 text-xs border border-rose-800/50 transition inline-flex items-center space-x-1"
                    >
                      <Trash2 className="w-3 h-3" />
                      <span>Delete</span>
                    </button>
                  </td>

                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}
