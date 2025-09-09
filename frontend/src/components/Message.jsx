function Message({ message }) {
  const { text, sender, timestamp, isError } = message;
  
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  if (sender === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-xs lg:max-w-md">
          <div className="message-user">
            <p className="text-sm whitespace-pre-wrap">{text}</p>
          </div>
          <p className="text-xs text-muted-foreground mt-1 text-right">
            {formatTime(timestamp)}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-xs lg:max-w-md">
        <div className="flex items-start gap-2">
          <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
            <span className="text-sm">🤖</span>
          </div>
          <div className="flex-1">
            <div className={`message-ai ${isError ? 'bg-destructive/10 text-destructive border border-destructive/20' : ''}`}>
              <p className="text-sm whitespace-pre-wrap">{text}</p>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {formatTime(timestamp)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Message;