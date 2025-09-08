import { useEffect } from 'react';
import { useDescope } from '@/contexts/DescopeContext';
import Sidebar from '@/components/Sidebar';
import ChatWindow from '@/components/ChatWindow';
import { useLocalChatStore } from '@/hooks/useLocalChatStore';
import { setMockMode } from '@/api/backend';

const Index = () => {
  const sdk = useDescope();
  const {
    conversations,
    currentConversationId,
    selectConversation,
    createNewConversation,
  } = useLocalChatStore();

  // Enable mock mode for development when backend is not available
  useEffect(() => {
    setMockMode(true); // Set to false when backend is ready
  }, []);

  // Check for session on mount and after redirects
  useEffect(() => {
    const checkSession = async () => {
      try {
        // Session check is handled by the Descope provider automatically
        console.log('Descope session check');
      } catch (error) {
        console.log('No active session');
      }
    };
    checkSession();
  }, [sdk]);

  const handleNewChat = () => {
    createNewConversation();
  };

  const handleSelectConversation = (id: string) => {
    selectConversation(id);
  };

  return (
    <div className="h-screen flex bg-background">
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
      />
      <div className="flex-1">
        <ChatWindow />
      </div>
    </div>
  );
};

export default Index;
