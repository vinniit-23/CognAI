import { useState, useEffect } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatConversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  lastUpdated: string;
}

export function useLocalChatStore() {
  const [conversations, setConversations] = useState<ChatConversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Load conversations from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('cognai-conversations');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setConversations(parsed);
      } catch (error) {
        console.error('Failed to parse stored conversations:', error);
      }
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('cognai-conversations', JSON.stringify(conversations));
  }, [conversations]);

  const getCurrentConversation = () => {
    return conversations.find(conv => conv.id === currentConversationId) || null;
  };

  const createNewConversation = (firstMessage?: ChatMessage) => {
    const newConv: ChatConversation = {
      id: Date.now().toString(),
      title: firstMessage?.content.slice(0, 50) + '...' || 'New Chat',
      messages: firstMessage ? [firstMessage] : [],
      lastUpdated: new Date().toISOString(),
    };
    
    setConversations(prev => [newConv, ...prev]);
    setCurrentConversationId(newConv.id);
    return newConv.id;
  };

  const addMessage = (message: ChatMessage, conversationId?: string) => {
    const targetId = conversationId || currentConversationId;
    if (!targetId) {
      // Create new conversation if none exists
      const newId = createNewConversation(message);
      return newId;
    }

    setConversations(prev => prev.map(conv => {
      if (conv.id === targetId) {
        const updatedMessages = [...conv.messages, message];
        return {
          ...conv,
          messages: updatedMessages,
          lastUpdated: new Date().toISOString(),
          title: conv.messages.length === 0 ? message.content.slice(0, 50) + '...' : conv.title,
        };
      }
      return conv;
    }));

    return targetId;
  };

  const selectConversation = (id: string) => {
    setCurrentConversationId(id);
  };

  const deleteConversation = (id: string) => {
    setConversations(prev => prev.filter(conv => conv.id !== id));
    if (currentConversationId === id) {
      setCurrentConversationId(null);
    }
  };

  return {
    conversations,
    currentConversation: getCurrentConversation(),
    currentConversationId,
    isLoading,
    setIsLoading,
    createNewConversation,
    addMessage,
    selectConversation,
    deleteConversation,
  };
}