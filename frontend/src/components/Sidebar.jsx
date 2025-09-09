import { useState } from "react";
import { useDescope } from "@descope/react-sdk";
import SignInFlow from "./SignInFlow";
import ConnectGmailButton from "./ConnectGmailButton";
import { getEmails } from "../api/backend";

function Sidebar({ session, onSignInSuccess, messages, sessionToken }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emails, setEmails] = useState([]);
  const [emailsLoading, setEmailsLoading] = useState(false);
  const sdk = useDescope();

  const user = session?.user || session?.data?.user || null;

  const filteredMessages = messages.filter((msg) =>
    msg.text.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleFetchEmails = async () => {
    if (!user) return;
    setEmailsLoading(true);
    try {
      const data = await getEmails(user.userId, 10);
      setEmails(data.messages || []);
      setShowEmailModal(true);
    } catch (error) {
      console.error("Fetch emails error:", error);
      alert(`Failed to fetch emails: ${error.message}`);
    } finally {
      setEmailsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await sdk.logout();
      console.log("✅ Logged out successfully");
    } catch (error) {
      console.error("❌ Logout error:", error);
    }
  };

  return (
    <div className="h-full flex flex-col p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-sidebar-foreground">
          <span className="bg-gradient-to-r from-primary to-primary-glow bg-clip-text text-transparent">
            CognAI
          </span>
        </h1>
        <p className="text-sm text-muted-foreground mt-1">AI Email Assistant</p>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full bg-card border border-border rounded-lg px-3 py-2 text-sm placeholder-muted-foreground focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>

      <div className="mb-6">
        {user ? (
          <div className="space-y-4">
            <div className="p-3 bg-card rounded-lg border border-border">
              <p className="text-sm font-medium text-foreground">
                {user.name || user.givenName || "User"}
              </p>
              <p className="text-xs text-muted-foreground">
                {user.email || user.loginIds?.[0] || "No email"}
              </p>
            </div>

            <div className="space-y-2">
              <ConnectGmailButton user={user} sessionToken={sessionToken} />

              <button
                onClick={handleFetchEmails}
                disabled={emailsLoading}
                className="w-full btn-ghost text-left p-2 rounded hover:bg-card"
              >
                {emailsLoading ? "Loading..." : "📧 Fetch Emails"}
              </button>

              <button
                onClick={handleLogout}
                className="w-full btn-ghost text-left p-2 rounded hover:bg-destructive/10 text-destructive"
              >
                🚪 Sign Out
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-sidebar-foreground">
              Sign In
            </h3>
            <SignInFlow onSuccess={onSignInSuccess} />
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto">
        <h3 className="text-sm font-medium text-sidebar-foreground mb-3">
          Recent Chats
        </h3>
        <div className="space-y-2">
          {filteredMessages.length === 0 ? (
            <p className="text-xs text-muted-foreground">
              No conversations yet
            </p>
          ) : (
            filteredMessages.slice(0, 10).map((message, index) => (
              <div
                key={index}
                className="p-2 bg-card rounded border border-border"
              >
                <p className="text-xs text-muted-foreground truncate">
                  {message.text.substring(0, 50)}...
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {new Date(message.timestamp).toLocaleDateString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {showEmailModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-card p-6 rounded-lg max-w-md w-full mx-4 max-h-96 overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Recent Emails</h3>
              <button
                onClick={() => setShowEmailModal(false)}
                className="text-muted-foreground hover:text-foreground"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3">
              {emails.length === 0 ? (
                <p className="text-muted-foreground">No emails found</p>
              ) : (
                emails.map((email, index) => (
                  <div key={index} className="p-3 border border-border rounded">
                    <p className="font-medium text-sm">
                      {email.subject || "No Subject"}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {email.from}
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(email.date).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Sidebar;
