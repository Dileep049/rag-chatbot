import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, Clock, Trash2, MoreVertical } from 'lucide-react';

const INITIAL_HISTORY = [
  { id: '1', text: "My Aadhaar card is lost..." },
  { id: '2', text: "Vehicle seized by police..." },
  { id: '3', text: "How can I download E-Aadhaar..." },
  { id: '4', text: "What documents required for pension..." },
  { id: '5', text: "How to apply for driving licence..." },
  { id: '6', text: "PAN card correction procedure..." }
];

export default function Sidebar({ onSelectHistoryItem, onClearChat }) {
  const [historyList, setHistoryList] = useState(INITIAL_HISTORY);
  const [activeMenuId, setActiveMenuId] = useState(null);
  const menuRef = useRef(null);

  // Close dropdown menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setActiveMenuId(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleDelete = (id, e) => {
    e.stopPropagation();
    setHistoryList((prev) => prev.filter((item) => item.id !== id));
    setActiveMenuId(null);
  };

  const handleClearAll = () => {
    setHistoryList([]);
    if (onClearChat) onClearChat();
  };

  return (
    <aside className="w-64 bg-[#0b1329] border-r border-slate-800 hidden md:flex flex-col h-full shrink-0 select-none">
      
      {/* Sidebar Header / History Title */}
      <div className="p-4 border-b border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center space-x-2 text-slate-300 font-semibold text-sm">
          <Clock className="w-4 h-4 text-indigo-400" />
          <span>Chat History</span>
        </div>
        <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-medium">
          {historyList.length}
        </span>
      </div>

      {/* History Items List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1.5" ref={menuRef}>
        {historyList.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            No chat history
          </div>
        ) : (
          historyList.map((item) => (
            <div key={item.id} className="relative group">
              <button
                onClick={() => onSelectHistoryItem && onSelectHistoryItem(item.text.replace('...', ''))}
                className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left text-xs sm:text-sm text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent hover:border-slate-700/50 transition-all duration-150 pr-8"
              >
                <div className="flex items-center space-x-2.5 min-w-0 flex-1">
                  <MessageSquare className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 shrink-0 transition" />
                  <span className="truncate">{item.text}</span>
                </div>
              </button>

              {/* Three-Dot Menu Trigger Button */}
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setActiveMenuId((prev) => (prev === item.id ? null : item.id));
                }}
                aria-label="More options"
                className={`absolute right-1.5 top-1/2 -translate-y-1/2 p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 transition-all ${
                  activeMenuId === item.id ? 'opacity-100 bg-slate-700/50 text-white' : 'opacity-0 group-hover:opacity-100'
                }`}
              >
                <MoreVertical className="w-3.5 h-3.5" />
              </button>

              {/* Popup Dropdown Menu */}
              {activeMenuId === item.id && (
                <div className="absolute right-1 top-9 z-50 w-32 bg-[#1a233a] border border-white/10 rounded-xl shadow-2xl p-1 animate-fadeIn">
                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    className="w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-lg text-xs font-medium text-rose-400 hover:text-rose-200 hover:bg-rose-950/60 transition"
                  >
                    <Trash2 className="w-3.5 h-3.5 text-rose-400" />
                    <span>Delete</span>
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Sidebar Footer */}
      <div className="p-3 border-t border-slate-800/80">
        <button
          onClick={handleClearAll}
          className="w-full flex items-center justify-center space-x-2 px-3 py-2 rounded-xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-800 text-slate-400 hover:text-rose-300 text-xs font-medium transition"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Clear All</span>
        </button>
      </div>

    </aside>
  );
}
