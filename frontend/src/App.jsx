import React, { useState } from 'react';
import { AuthProvider } from './auth/AuthContext';
import ProtectedRoute from './auth/ProtectedRoute';
import ChatPage from './pages/Chat';
import AdminPage from './pages/Admin';
import LoginPage from './pages/Login';

function AppContent() {
  const [currentView, setCurrentView] = useState('chat'); // 'chat', 'admin', 'login'

  if (currentView === 'login') {
    return (
      <LoginPage
        onLoginSuccess={() => setCurrentView('admin')}
        onBackToChat={() => setCurrentView('chat')}
      />
    );
  }

  if (currentView === 'admin') {
    return (
      <ProtectedRoute
        onGoToLogin={() => setCurrentView('login')}
        onGoToChat={() => setCurrentView('chat')}
      >
        <AdminPage onReturnToChat={() => setCurrentView('chat')} />
      </ProtectedRoute>
    );
  }

  return (
    <ChatPage
      onNavigateToAdmin={() => setCurrentView('admin')}
      onNavigateToLogin={() => setCurrentView('login')}
      currentView={currentView}
      setCurrentView={setCurrentView}
    />
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
