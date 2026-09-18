import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

const SUGGESTED_ITEMS = [
  "My Aadhaar card is lost. What should I do?",
  "నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?",
  "What documents are required for pension?",
  "Police seized my bike. What should I do?",
  "How can I apply for a driving licence?"
];

export default function SuggestedQuestions({ onSelectQuestion }) {
  return (
    <div className="w-full max-w-2xl mx-auto space-y-3 pt-2">
      <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 text-left px-1 flex items-center space-x-1.5">
        <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
        <span>Try Asking / ఉదాహరణ ప్రశ్నలు</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {SUGGESTED_ITEMS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(q)}
            className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-indigo-500/40 text-left text-xs sm:text-sm text-slate-300 hover:text-slate-100 transition-all duration-200 flex items-center justify-between group shadow-sm hover:shadow-indigo-500/10"
          >
            <span className="leading-snug pr-2">{q}</span>
            <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all shrink-0" />
          </button>
        ))}
      </div>
    </div>
  );
}
