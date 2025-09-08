import { useState, useRef, useEffect } from 'react';
import { useSession, useUser } from '@/contexts/DescopeContext';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, Loader2, MessageSquare } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import Message from './Message';
import { ChatMessage, useLocalChatStore } from '@/hooks/useLocalChatStore';
import { postChat } from '@/api/backend';

export default function ChatWindow() {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  
  const { isAuthenticated } = useSession();
  const { user } = useUser();
  const { toast } = useToast();
  
  const {
    currentConversation,
    currentConversationId,
    addMessage,
    createNewConversation,
    isLoading: storeLoading,
  } = useLocalChatStore();

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [currentConversation?.messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };

    const userInput = input.trim();
    setInput('');
    setIsLoading(true);

    try {
      // Add user message to conversation
      const conversationId = addMessage(userMessage, currentConversationId);

      // Get AI response
      const response = await postChat(userInput, user?.userId);
      
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.ai_response,
        timestamp: new Date().toISOString(),
      };

      // Add AI response to conversation
      addMessage(aiMessage, conversationId);

    } catch (error) {
      console.error('Chat error:', error);
      toast({
        title: "Message failed",
        description: error instanceof Error ? error.message : "Failed to send message",
        variant: "destructive",
      });

      // Add error message to show user what happened
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I'm having trouble responding right now. Please try again.",
        timestamp: new Date().toISOString(),
      };
      addMessage(errorMessage, currentConversationId);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const messages = currentConversation?.messages || [];

  return (
    <div className="chat-bg h-full flex flex-col">
      {/* Chat Messages */}
      <div className="flex-1 overflow-hidden">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md">
              <div className="w-16 h-16 brand-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageSquare size={32} className="text-white" />
              </div>
              <h2 className="text-xl font-semibold mb-2">Welcome to CognAI</h2>
              <p className="text-muted-foreground mb-4">
                Your intelligent assistant for Gmail and more. Start a conversation below!
              </p>
              {!isAuthenticated && (
                <p className="text-sm text-muted-foreground">
                  Sign in to connect your Gmail and unlock more features.
                </p>
              )}
            </div>
          </div>
        ) : (
          <ScrollArea ref={scrollAreaRef} className="h-full">
            <div className="max-w-4xl mx-auto py-4">
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex gap-3 p-4">
                  <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                    <Loader2 size={16} className="animate-spin" />
                  </div>
                  <div className="chat-message-ai">
                    <div className="flex items-center gap-2">
                      <Loader2 size={14} className="animate-spin" />
                      <span className="text-sm text-muted-foreground">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-border p-4">
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything... (Press Enter to send, Shift+Enter for new line)"
              className="chat-input pr-12 min-h-[44px] max-h-[120px] resize-none"
              disabled={isLoading}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              size="sm"
              className="absolute right-2 bottom-2 h-8 w-8 p-0"
            >
              {isLoading ? (
                <Loader2 size={16} className="animate-spin" />
              ) : (
                <Send size={16} />
              )}
            </Button>
          </div>
          
          <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
            <span>
              {isAuthenticated ? `Signed in${user?.email ? ` as ${user.email}` : ''}` : 'Not signed in'}
            </span>
            <span>{input.length}/2000</span>
          </div>
        </div>
      </div>
    </div>
  );
}