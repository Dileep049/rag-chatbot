import React, { useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { Lock, Mail, Loader2, AlertCircle, ArrowLeft, ShieldCheck } from 'lucide-react';

export default function LoginPage({ onLoginSuccess, onBackToChat }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError('Please enter both email and password.');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const user = await login(email.trim(), password);
      if (user.role === 'admin') {
        if (onLoginSuccess) onLoginSuccess();
      } else {
        setError('Access denied. You do not have permission to access the Admin Panel.');
      }
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail || 'Invalid email or password.';
      setError(detail);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4 text-slate-100 font-sans">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-md w-full shadow-2xl space-y-6 animate-fadeIn">
        
        {/* Header Emblem & Title */}
        <div className="text-center space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 via-indigo-600 to-emerald-500 p-0.5 shadow-lg shadow-indigo-500/20 mx-auto flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-xl">
              🇮🇳
            </div>
          </div>

          <h1 className="text-xl font-bold bg-gradient-to-r from-amber-200 via-slate-100 to-emerald-300 bg-clip-text text-transparent">
            Citizen Assistance AI
          </h1>

          <p className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">
            Admin Login
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@citizen.gov.in"
                disabled={submitting}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                disabled={submitting}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="flex items-center space-x-2 text-xs text-rose-300 p-3 bg-rose-950/40 border border-rose-800/60 rounded-xl">
              <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-md shadow-indigo-600/30 flex items-center justify-center space-x-2 transition"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Signing in...</span>
              </>
            ) : (
              <>
                <ShieldCheck className="w-4 h-4" />
                <span>Login</span>
              </>
            )}
          </button>
        </form>

        {/* Back to Citizen Assistant Link */}
        <div className="pt-2 border-t border-slate-800 text-center">
          <button
            onClick={onBackToChat}
            className="inline-flex items-center space-x-1.5 text-xs text-slate-400 hover:text-indigo-300 font-medium transition"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Citizen Assistant</span>
          </button>
        </div>

      </div>
    </div>
  );
}
