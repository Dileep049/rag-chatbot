import React from 'react';
import { PlusCircle, Database, Sparkles, LogIn, LogOut, Shield } from 'lucide-react';
import { useAuth } from '../auth/AuthContext';

export default function Header({ activeTab, setActiveTab, onNewChat }) {
  const { isAdmin, user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 bg-[#0b1329]/90 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 via-indigo-600 to-emerald-500 p-0.5 shadow-md shadow-indigo-500/20 shrink-0">
              <div className="w-full h-full bg-[#0b1329] rounded-[10px] flex items-center justify-center text-lg">
                🇮🇳
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-base sm:text-lg font-bold bg-gradient-to-r from-amber-200 via-slate-100 to-emerald-300 bg-clip-text text-transparent">
                  Citizen Assistance AI
                </h1>
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  <Sparkles className="w-3 h-3 mr-1" /> RAG Powered
                </span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onNewChat}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white text-xs sm:text-sm font-medium transition-all shadow-sm"
            >
              <PlusCircle className="w-4 h-4 text-indigo-400" />
              <span>+ New Chat</span>
            </button>

            {isAdmin ? (
              <>
                <button
                  onClick={() => setActiveTab('admin')}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 text-indigo-300 text-xs sm:text-sm font-medium transition-all"
                >
                  <Database className="w-4 h-4 text-indigo-400" />
                  <span className="hidden sm:inline">Admin Hub</span>
                </button>

                <button
                  onClick={logout}
                  className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-rose-800 text-slate-400 hover:text-rose-300 transition-all"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </>
            ) : (
              <button
                onClick={() => setActiveTab('login')}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-slate-200 text-xs sm:text-sm font-medium transition-all"
              >
                <LogIn className="w-4 h-4 text-slate-400" />
                <span className="hidden sm:inline">Admin Login</span>
              </button>
            )}
          </div>

        </div>
      </div>
    </header>
  );
}
