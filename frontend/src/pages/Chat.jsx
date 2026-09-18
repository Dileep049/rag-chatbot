import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import ChatBox from '../components/ChatBox';
import { askChat } from '../services/api';

const LOCAL_STORAGE_KEY = 'citizen_chat_history';

export default function ChatPage({ onNavigateToAdmin, onNavigateToLogin }) {
  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      console.error('Failed to load chat history from localStorage', e);
      return [];
    }
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Save conversation history to localStorage on update
  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(messages));
    } catch (e) {
      console.error('Failed to save chat history to localStorage', e);
    }
  }, [messages]);

  const handleSendMessage = async (questionText) => {
    if (!questionText.trim()) return;

    const userMsg = {
      sender: 'user',
      text: questionText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    const currentHistory = [...messages];
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      // Send question and conversation history to backend RAG API
      const response = await askChat(questionText, null, currentHistory);
      
      const aiMsg = {
        sender: 'ai',
        text: response.answer,
        sources: response.sources || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.detail 
        || "Sorry, I couldn't connect to the Citizen Assistance service. Please try again.";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerateLast = () => {
    const userMsgs = messages.filter((m) => m.sender === 'user');
    if (userMsgs.length > 0) {
      const lastUserQuestion = userMsgs[userMsgs.length - 1].text;
      const trimmedMessages = messages.slice(0, messages.findLastIndex((m) => m.sender === 'user'));
      setMessages(trimmedMessages);
      handleSendMessage(lastUserQuestion);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setError(null);
    try {
      localStorage.removeItem(LOCAL_STORAGE_KEY);
    } catch (e) {
      console.error('Failed to clear localStorage chat history', e);
    }
  };

  const handleTabChange = (tab) => {
    if (tab === 'admin') {
      if (onNavigateToAdmin) onNavigateToAdmin();
    } else if (tab === 'login') {
      if (onNavigateToLogin) onNavigateToLogin();
    }
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-[#0b1329] text-slate-100 font-sans">
      
      {/* Header */}
      <Header
        activeTab="chat"
        setActiveTab={handleTabChange}
        onNewChat={handleNewChat}
      />

      {/* Main Area: Sidebar + Chat Content */}
      <div className="flex-1 flex overflow-hidden bg-[#0b1329]">
        <Sidebar
          onSelectHistoryItem={(itemText) => handleSendMessage(itemText)}
          onClearChat={handleNewChat}
        />
        <ChatBox
          messages={messages}
          onSendMessage={handleSendMessage}
          loading={loading}
          error={error}
          onClearChat={handleNewChat}
          onRegenerateLast={handleRegenerateLast}
        />
      </div>

      {/* Footer */}
      <footer className="py-2.5 text-center text-[11px] text-slate-500 bg-[#0b1329] border-t border-slate-800/80 shrink-0">
        <span>Citizen Assistance AI • Information is based strictly on available official documents.</span>
      </footer>

    </div>
  );
}
