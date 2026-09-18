import React from 'react';
import { ChevronRight } from 'lucide-react';

export default function CategoryCard({ category, onClick }) {
  return (
    <button
      onClick={onClick}
      className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 text-left transition-all duration-200 flex items-center justify-between group shadow-sm hover:shadow-indigo-500/10"
    >
      <div className="flex items-center space-x-3">
        <span className="text-2xl p-2 rounded-lg bg-slate-950 border border-slate-800 shrink-0">
          {category.icon}
        </span>
        <div>
          <h3 className="text-sm font-semibold text-slate-100 group-hover:text-indigo-300 transition">
            {category.name}
          </h3>
          <p className="text-xs text-slate-400">
            {category.description || 'View procedures & official guidelines'}
          </p>
        </div>
      </div>
      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all shrink-0" />
    </button>
  );
}
