import { useState } from 'react';
import { Search, MessageSquare, Plus, Settings, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import SignInButton from './SignInButton';
import ConnectButton from './ConnectButton';
import EmailsModal from './EmailsModal';
import { ChatConversation } from '@/hooks/useLocalChatStore';

interface SidebarProps {
  conversations: ChatConversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
}

export default function Sidebar({ 
  conversations, 
  currentConversationId, 
  onSelectConversation,
  onNewChat 
}: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredConversations = conversations.filter(conv =>
    conv.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    conv.messages.some(msg => 
      msg.content.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString([], { weekday: 'short' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  return (
    <div className="sidebar-bg h-full flex flex-col w-80 max-w-80">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 brand-gradient rounded-lg flex items-center justify-center">
            <Brain size={20} className="text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold">CognAI</h1>
            <p className="text-xs text-muted-foreground">AI Assistant</p>
          </div>
        </div>

        <Button 
          onClick={onNewChat}
          className="w-full mb-3"
          variant="outline"
        >
          <Plus size={16} className="mr-2" />
          New Chat
        </Button>

        {/* Search */}
        <div className="relative">
          <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-hidden">
        <div className="p-3 text-xs font-medium text-muted-foreground">
          Recent Chats
        </div>
        
        <ScrollArea className="h-full px-2">
          <div className="space-y-1 pb-4">
            {filteredConversations.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <MessageSquare size={32} className="mx-auto mb-2 opacity-50" />
                <p className="text-sm">
                  {searchQuery ? 'No matching chats' : 'No chats yet'}
                </p>
                {!searchQuery && (
                  <p className="text-xs mt-1">Start a conversation to get going!</p>
                )}
              </div>
            ) : (
              filteredConversations.map((conversation) => (
                <button
                  key={conversation.id}
                  onClick={() => onSelectConversation(conversation.id)}
                  className={`w-full text-left p-3 rounded-lg hover-bg transition-colors group ${
                    currentConversationId === conversation.id 
                      ? 'bg-accent/20 border border-accent/30' 
                      : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {conversation.title}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {conversation.messages[conversation.messages.length - 1]?.content || 'No messages'}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-1 ml-2">
                      <span className="text-xs text-muted-foreground">
                        {formatDate(conversation.lastUpdated)}
                      </span>
                      {conversation.messages.length > 0 && (
                        <Badge variant="secondary" className="text-xs">
                          {conversation.messages.length}
                        </Badge>
                      )}
                    </div>
                  </div>
                </button>
              ))
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Bottom Actions */}
      <div className="p-4 border-t border-border space-y-3">
        <SignInButton />
        <ConnectButton />
        <EmailsModal />
        
        <Separator />
        
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <Settings size={12} />
          <span>Mock mode enabled for development</span>
        </div>
      </div>
    </div>
  );
}