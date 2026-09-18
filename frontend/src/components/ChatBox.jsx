import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, AlertCircle, ShieldCheck, ArrowDown, RefreshCw } from 'lucide-react';
import Message from './Message';
import VoiceInput from './VoiceInput';

export default function ChatBox({ 
  messages, 
  onSendMessage, 
  loading, 
  error,
  onRegenerateLast
}) {
  const [input, setInput] = useState('');
  const [showScrollBottom, setShowScrollBottom] = useState(false);
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = (behavior = 'smooth') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  const handleScroll = () => {
    if (!containerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    const isUp = scrollHeight - scrollTop - clientHeight > 150;
    setShowScrollBottom(isUp);
  };

  useEffect(() => {
    if (!showScrollBottom) {
      scrollToBottom();
    }
  }, [messages, loading]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextareaChange = (e) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  };

  const handleVoiceTranscript = (text) => {
    setInput((prev) => (prev ? `${prev} ${text}` : text));
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight + 30, 160)}px`;
    }
  };

  const renderSearchForm = () => (
    <form onSubmit={handleSubmit} className="relative flex items-center bg-[#1a233a] border border-white/10 rounded-full shadow-lg shadow-black/20 focus-within:ring-1 focus-within:ring-slate-500 focus-within:border-transparent transition-all duration-200">
      <textarea
        ref={textareaRef}
        rows="1"
        value={input}
        onChange={handleTextareaChange}
        onKeyDown={handleKeyDown}
        placeholder="Ask about government services, procedures, or schemes..."
        className="w-full pl-6 pr-28 py-4 bg-transparent text-slate-100 placeholder-slate-400 text-sm sm:text-base focus:outline-none resize-none leading-normal"
        aria-label="Ask your question"
      />

      <div className="absolute right-3.5 flex items-center space-x-2">
        <VoiceInput onTranscript={handleVoiceTranscript} disabled={loading} />

        <button
          type="submit"
          disabled={!input.trim() || loading}
          aria-label="Send question"
          className={`p-2.5 rounded-full flex items-center justify-center transition-all duration-200 ${
            input.trim() && !loading
              ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 hover:bg-indigo-500 active:scale-95'
              : 'bg-slate-800/80 text-slate-500 cursor-not-allowed'
          }`}
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
        </button>
      </div>
    </form>
  );

  return (
    <div className="flex-1 flex flex-col h-full bg-[#0b1329] overflow-hidden relative">
      
      {/* Empty State: Perfectly Centered Greeting, Sub-description & Sleek Input Box */}
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center p-4 sm:p-6 text-center animate-fadeIn my-auto">
          <div className="w-full max-w-2xl space-y-6">
            
            {/* Clean Greeting */}
            <div className="space-y-3">
              <h2 className="text-2xl sm:text-4xl font-bold text-slate-100 tracking-tight">
                How can I help you today?
              </h2>

              <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-lg mx-auto font-normal">
                Ask questions about citizen services, government procedures and official information in <strong>English</strong> or <strong>తెలుగు</strong>.
              </p>
            </div>

            {/* Main Search Input Box (max-w-2xl) Centered */}
            <div className="w-full space-y-2">
              {renderSearchForm()}
              <div className="flex items-center justify-between text-[11px] text-slate-500 px-3">
                <span>Press <strong>Enter</strong> to send, <strong>Shift + Enter</strong> for line break</span>
                <span className="flex items-center space-x-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 inline" />
                  <span>Grounded RAG Knowledge Base</span>
                </span>
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* Conversation Thread State */
        <>
          {/* Scrollable Messages Area */}
          <div 
            ref={containerRef}
            onScroll={handleScroll}
            className="flex-1 overflow-y-auto px-4 py-6 sm:py-8 space-y-6"
          >
            <div className="max-w-2xl mx-auto space-y-6">
              {messages.map((msg, index) => (
                <Message 
                  key={index} 
                  message={msg} 
                  onRegenerate={!msg.sender && index === messages.length - 1 ? onRegenerateLast : undefined}
                />
              ))}

              {/* Typing / Processing State */}
              {loading && (
                <div className="flex items-center space-x-3 text-slate-400 p-4 bg-slate-900/70 border border-slate-800/80 rounded-2xl max-w-md animate-pulse">
                  <Loader2 className="w-4 h-4 animate-spin text-indigo-400 shrink-0" />
                  <div className="text-xs sm:text-sm">
                    <span className="font-semibold text-slate-200 block">Searching official information...</span>
                    <span className="text-slate-400 text-xs">● ● ●</span>
                  </div>
                </div>
              )}

              {/* Error Alert with Retry */}
              {error && (
                <div className="flex items-start justify-between p-4 bg-rose-950/40 border border-rose-800/60 text-rose-300 rounded-2xl">
                  <div className="flex items-start space-x-3 text-xs sm:text-sm">
                    <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                    <div>
                      <strong className="font-semibold text-rose-200">Something went wrong.</strong>
                      <p className="mt-0.5 text-xs">{error}</p>
                    </div>
                  </div>
                  {onRegenerateLast && (
                    <button
                      onClick={onRegenerateLast}
                      className="px-3 py-1.5 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-rose-100 text-xs font-semibold shrink-0 transition flex items-center space-x-1"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      <span>Retry</span>
                    </button>
                  )}
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Floating "New Messages" Scroll Pill */}
          {showScrollBottom && (
            <button
              onClick={() => scrollToBottom('smooth')}
              className="absolute bottom-20 left-1/2 -translate-x-1/2 px-3 py-1.5 rounded-full bg-indigo-600 text-white text-xs font-semibold shadow-lg shadow-indigo-600/40 hover:bg-indigo-500 transition flex items-center space-x-1.5 animate-bounce z-20"
            >
              <ArrowDown className="w-3.5 h-3.5" />
              <span>New messages</span>
            </button>
          )}

          {/* Bottom Chat Input Box */}
          <div className="p-4 bg-[#0b1329]/90 border-t border-slate-800/60 backdrop-blur-md">
            <div className="max-w-2xl mx-auto space-y-2">
              {renderSearchForm()}
              <div className="flex items-center justify-between text-[11px] text-slate-500 px-3">
                <span>Press <strong>Enter</strong> to send, <strong>Shift + Enter</strong> for line break</span>
                <span className="flex items-center space-x-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 inline" />
                  <span>Grounded RAG Knowledge Base</span>
                </span>
              </div>
            </div>
          </div>
        </>
      )}

    </div>
  );
}
