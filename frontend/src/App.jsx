import { useEffect, useState } from "react";
import {
  getSessionToken,
  useSession,
  useDescope,
  useUser,
} from "@descope/react-sdk";
import Sidebar from "./components/Sidebar.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import SignInFlow from "./components/SignInFlow.jsx";
import { notifyConnection } from "./api/backend.js";

function App() {
  const {
    isAuthenticated,
    session,
    isLoading: isSessionLoading,
  } = useSession();
  const { user, isLoading: isUserLoading } = useUser();
  const [messages, setMessages] = useState([]);
  const sdk = useDescope();

  const isLoading = isSessionLoading || isUserLoading;

  // Debug session token and auth state
  useEffect(() => {
    console.log("isAuthenticated:", isAuthenticated);
    console.log("session:", session);
    console.log("user:", user);
    const token = getSessionToken();
    console.log("sessionToken:", token);
  }, [isAuthenticated, session, user]);

  useEffect(() => {
    const handleOAuthReturn = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const currentUser = user || session?.user;

        if (urlParams.get("code") && currentUser?.userId) {
          await notifyConnection(currentUser.userId);
          alert("✅ Gmail connected successfully!");
          window.history.replaceState({}, "", window.location.pathname);
        }
      } catch (err) {
        console.error("❌ Failed to notify backend:", err);
      }
    };

    if (isAuthenticated && !isLoading) {
      handleOAuthReturn();
    }
  }, [isAuthenticated, user, session, isLoading]);

  const handleSignInSuccess = async (e) => {
    if (sdk) {
      try {
        await sdk.refresh();
      } catch (error) {
        console.error("Failed to refresh session:", error);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="max-w-md w-full p-6">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-foreground mb-2">
              <span className="bg-gradient-to-r from-primary to-primary-glow bg-clip-text text-transparent">
                CognAI
              </span>
            </h1>
            <p className="text-muted-foreground">
              Sign in to access your AI Email Assistant
            </p>
          </div>
          <SignInFlow onSuccess={handleSignInSuccess} />
        </div>
      </div>
    );
  }

  // Get session token from Descope SDK
  const sessionToken = getSessionToken();

  return (
    <div className="flex h-screen bg-background">
      <div className="w-80 sidebar">
        <Sidebar
          session={session || { user }}
          messages={messages}
          onSignInSuccess={handleSignInSuccess}
          sessionToken={sessionToken} // Pass the session token here
        />
      </div>
      <div className="flex-1 flex flex-col">
        <ChatWindow
          session={session || { user }}
          messages={messages}
          setMessages={setMessages}
        />
      </div>
    </div>
  );
}

export default App;
