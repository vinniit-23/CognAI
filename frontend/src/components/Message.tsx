import { ReactNode } from 'react';
import { ChatMessage } from '@/hooks/useLocalChatStore';
import { User, Bot } from 'lucide-react';

interface MessageProps {
  message: ChatMessage;
}

// Simple markdown renderer for basic formatting
const renderMarkdown = (content: string): ReactNode => {
  // Basic markdown support: **bold**, *italic*, `code`, and line breaks
  const parts = content.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`|\n)/g);
  
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('*') && part.endsWith('*') && !part.startsWith('**')) {
      return <em key={index}>{part.slice(1, -1)}</em>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={index} className="bg-muted px-1 py-0.5 rounded text-sm font-mono">{part.slice(1, -1)}</code>;
    }
    if (part === '\n') {
      return <br key={index} />;
    }
    return part;
  });
};

export default function Message({ message }: MessageProps) {
  const isUser = message.role === 'user';
  const time = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  return (
    <div className={`flex gap-3 p-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser 
          ? 'bg-primary text-primary-foreground' 
          : 'bg-muted text-muted-foreground'
      }`}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Message content */}
      <div className={`flex flex-col gap-1 max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`${isUser ? 'chat-message-user' : 'chat-message-ai'} whitespace-pre-wrap`}>
          {isUser ? message.content : renderMarkdown(message.content)}
        </div>
        <span className="text-xs text-muted-foreground px-1">
          {time}
        </span>
      </div>
    </div>
  );
}