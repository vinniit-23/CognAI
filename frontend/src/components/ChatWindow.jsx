import { useState, useRef, useEffect } from "react";
import Message from "./Message";
import { postChat } from "../api/backend";

function ChatWindow({ session, messages, setMessages }) {
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // ✅ Better user extraction
  const user = session?.user || session?.data?.user || null;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !user?.userId) {
      console.warn("Missing input or user ID");
      return;
    }

    const userMessage = {
      text: inputValue,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await postChat(inputValue, user.userId);
      const aiMessage = {
        text: response.ai_response || "⚠️ Could not process request.",
        sender: "ai",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          text: `Error: ${err.message}`,
          sender: "ai",
          timestamp: new Date().toISOString(),
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="border-b p-4 bg-card">
        <h2 className="text-lg font-semibold">
          {user ? "Chat with CognAI" : "Please sign in to start chatting"}
        </h2>
        {user && (
          <div className="flex items-center gap-2 mt-1">
            <p className="text-sm text-muted-foreground">
              AI assistant powered by Gmail
            </p>
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-xs text-green-600">Connected</span>
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && user ? (
          <div className="text-center text-muted-foreground py-8">
            <div className="text-4xl mb-4">🤖</div>
            <p className="text-lg font-medium mb-2">Welcome to CognAI!</p>
            <p className="text-sm">
              Ask me anything about your emails or Gmail account.
            </p>
          </div>
        ) : (
          messages.map((m, i) => <Message key={i} message={m} />)
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 p-3 bg-muted rounded-lg">
              <div className="animate-spin w-4 h-4 border-2 border-primary border-t-transparent rounded-full"></div>
              <p className="text-sm">AI is thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t p-4 bg-card">
        {!user ? (
          <div className="text-center text-muted-foreground">
            <p>Please sign in to start chatting with CognAI</p>
          </div>
        ) : (
          <div className="flex gap-2 items-end">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your emails..."
              className="flex-1 border rounded-lg p-3 min-h-[44px] max-h-32 resize-none focus:ring-2 focus:ring-primary focus:border-transparent"
              disabled={isLoading}
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="btn-primary px-4 py-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "..." : "Send"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatWindow;
