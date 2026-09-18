import React, { useState } from 'react';
import { User, Bot, FileText, Copy, Check, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import SourceCard from './SourceCard';

export default function Message({ message, onRegenerate }) {
  const isUser = message.sender === 'user';
  const [copied, setCopied] = useState(false);
  const [sourcesExpanded, setSourcesExpanded] = useState(false);

  const handleCopy = () => {
    if (message.text) {
      navigator.clipboard.writeText(message.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const formatMarkdown = (text) => {
    if (!text) return '';
    // Format headings, bold text, and numbered lists
    let formatted = text
      .replace(/#### (.*?)\n/g, '<h4 class="text-sm font-semibold text-indigo-300 mt-2.5 mb-1">$1</h4>')
      .replace(/### (.*?)\n/g, '<h3 class="text-base font-bold text-white mt-3 mb-1">$1</h3>')
      .replace(/## (.*?)\n/g, '<h2 class="text-lg font-bold text-white mt-3 mb-1.5">$1</h2>')
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-slate-100">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic text-slate-300">$1</em>');

    return formatted;
  };

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
      <div className={`flex space-x-3 max-w-2xl ${isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
        
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-md ${
          isUser 
            ? 'bg-slate-700 text-slate-200' 
            : 'bg-indigo-600 text-white shadow-indigo-600/30'
        }`}>
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>

        {/* Message Content Container */}
        <div className="space-y-2 flex-1">
          
          {/* Header Label */}
          <div className={`flex items-center space-x-2 text-xs font-semibold ${isUser ? 'justify-end text-slate-400' : 'text-indigo-400'}`}>
            <span>{isUser ? 'You' : 'Citizen Assistance AI'}</span>
            {message.timestamp && (
              <span className="text-[10px] text-slate-500 font-normal">{message.timestamp}</span>
            )}
          </div>

          {/* Message Text Bubble */}
          <div className={`p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
            isUser 
              ? 'bg-indigo-600 text-white rounded-tr-none shadow-md shadow-indigo-600/20' 
              : 'bg-slate-900 border border-slate-800 text-slate-100 rounded-tl-none shadow-sm'
          }`}>
            <div dangerouslySetInnerHTML={{ __html: formatMarkdown(message.text) }} />
          </div>

          {/* Action Bar for AI Messages: Copy & Regenerate */}
          {!isUser && (
            <div className="flex items-center justify-between pt-1 text-xs text-slate-400">
              
              {/* Collapsible Sources Toggle Button */}
              {message.sources && message.sources.length > 0 ? (
                <button
                  onClick={() => setSourcesExpanded(!sourcesExpanded)}
                  className="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-indigo-300 font-medium transition"
                >
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Sources ({message.sources.length})</span>
                  {sourcesExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              ) : <div />}

              {/* Copy & Regenerate Controls */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleCopy}
                  className="flex items-center space-x-1 px-2 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 transition"
                  title="Copy visible answer"
                  aria-label="Copy visible answer"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>

                {onRegenerate && (
                  <button
                    onClick={onRegenerate}
                    className="flex items-center space-x-1 px-2 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 transition"
                    title="Regenerate response"
                    aria-label="Regenerate response"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Regenerate</span>
                  </button>
                )}
              </div>

            </div>
          )}

          {/* Expanded Source Cards */}
          {!isUser && sourcesExpanded && message.sources && message.sources.length > 0 && (
            <div className="pt-2 space-y-2 animate-fadeIn">
              <div className="grid grid-cols-1 gap-2">
                {message.sources.map((src, idx) => (
                  <SourceCard key={idx} source={src} />
                ))}
              </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
