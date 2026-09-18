import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Globe, AlertCircle } from 'lucide-react';

export default function VoiceInput({ onTranscript, disabled }) {
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState('te-IN'); // Default Telugu (te-IN) or English (en-IN)
  const [recognition, setRecognition] = useState(null);
  const [isSupported, setIsSupported] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = language;

      rec.onstart = () => {
        setIsListening(true);
        setErrorMessage(null);
      };

      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript && onTranscript) {
          onTranscript(transcript);
        }
        setIsListening(false);
      };

      rec.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        if (event.error !== 'no-speech') {
          setErrorMessage(`Voice error: ${event.error}`);
        }
        setIsListening(false);
      };

      rec.onend = () => {
        setIsListening(false);
      };

      setRecognition(rec);
    } else {
      setIsSupported(false);
    }
  }, [language, onTranscript]);

  const toggleListening = () => {
    if (!isSupported) {
      setErrorMessage('Voice input is unavailable in this browser. Please type your question.');
      return;
    }

    if (isListening) {
      recognition?.stop();
      setIsListening(false);
    } else {
      setErrorMessage(null);
      try {
        recognition.lang = language;
        recognition?.start();
      } catch (e) {
        console.error(e);
        setIsListening(false);
      }
    }
  };

  return (
    <div className="flex items-center space-x-1.5">
      
      {/* Speech Language Selector Pill */}
      <button
        type="button"
        onClick={() => setLanguage(language === 'te-IN' ? 'en-IN' : 'te-IN')}
        className="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-[11px] font-semibold text-slate-300 border border-slate-700 transition flex items-center space-x-1"
        title="Toggle voice language between Telugu & English"
        aria-label="Toggle voice language"
      >
        <Globe className="w-3 h-3 text-indigo-400" />
        <span>{language === 'te-IN' ? 'తెలుగు' : 'English'}</span>
      </button>

      {/* Microphone Button */}
      <button
        type="button"
        onClick={toggleListening}
        disabled={disabled}
        aria-label={isListening ? "Stop voice input" : "Start voice input"}
        className={`p-2 rounded-xl transition-all duration-200 flex items-center justify-center ${
          isListening
            ? 'bg-rose-600 text-white animate-pulse shadow-md shadow-rose-600/40'
            : 'bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700'
        }`}
        title={isListening ? "Stop listening" : "Click to speak your question"}
      >
        {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4 text-indigo-400" />}
      </button>

      {/* Listening Status Badge */}
      {isListening && (
        <span className="hidden sm:inline-flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse">
          <span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span>
          <span>Listening ({language === 'te-IN' ? 'తెలుగు' : 'English'})...</span>
        </span>
      )}

      {/* Unsupported / Error Alert */}
      {errorMessage && (
        <div className="absolute bottom-full mb-2 left-0 right-0 p-2 bg-amber-950/90 border border-amber-800 text-amber-200 text-xs rounded-xl shadow-lg flex items-center justify-between z-50">
          <div className="flex items-center space-x-1.5">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>{errorMessage}</span>
          </div>
          <button onClick={() => setErrorMessage(null)} className="text-amber-400 hover:text-white text-xs font-bold pl-2">✕</button>
        </div>
      )}

    </div>
  );
}
