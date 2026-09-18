import React from 'react';
import { useAuth } from './AuthContext';
import { Loader2, ShieldAlert } from 'lucide-react';

export default function ProtectedRoute({ children, onGoToLogin, onGoToChat }) {
  const { token, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-300 space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
        <div className="text-sm font-medium">Checking authentication...</div>
      </div>
    );
  }

  if (!token || !isAdmin) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4 text-slate-100 font-sans">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-md w-full shadow-2xl text-center space-y-6 animate-fadeIn">
          
          <div className="w-14 h-14 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 mx-auto flex items-center justify-center">
            <ShieldAlert className="w-8 h-8" />
          </div>

          <div className="space-y-2">
            <h2 className="text-xl font-bold text-white">Access Denied</h2>
            <p className="text-sm text-slate-400 leading-relaxed">
              You do not have permission to access the Admin Panel. Authentication and Admin role are required.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <button
              onClick={onGoToLogin}
              className="flex-1 py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-md shadow-indigo-600/30 transition"
            >
              Log In as Admin
            </button>

            <button
              onClick={onGoToChat}
              className="flex-1 py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-sm border border-slate-700 transition"
            >
              Back to Chat
            </button>
          </div>

        </div>
      </div>
    );
  }

  return children;
}
