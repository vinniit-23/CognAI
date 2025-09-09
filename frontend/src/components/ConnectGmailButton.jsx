// src/components/ConnectGmailButton.jsx
import React, { useState, useEffect } from "react";
import { getSessionToken, useUser, useSession } from "@descope/react-sdk";
import { apiPost } from "../api/backend"; // named export from api/backend.js

const ConnectGmailButton = ({
  user: propUser = null,
  sessionToken: propSessionToken = null,
}) => {
  // prefer passed props (Sidebar passes these), fallback to SDK hooks
  const { user: hookUser } = useUser();
  const { isAuthenticated } = useSession();
  const user = propUser ?? hookUser ?? null;

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // debug info
    console.log("ConnectGmailButton - isAuthenticated:", isAuthenticated);
    console.log("ConnectGmailButton - user (prop/hook):", user);
    const tok = propSessionToken ?? getSessionToken();
    console.log(
      "ConnectGmailButton - sessionToken (preview):",
      tok ? "available" : "null"
    );
  }, [isAuthenticated, user, propSessionToken]);

  const handleConnectGmail = async () => {
    if (!user?.userId) {
      alert("Please sign in first before connecting Gmail.");
      return;
    }

    const sessionToken = propSessionToken ?? getSessionToken();
    if (!sessionToken) {
      alert("No session token available. Please sign in again.");
      return;
    }

    try {
      setLoading(true);

      // Use apiPost helper which will attach the Authorization header automatically
      const data = await apiPost(
        "/auth/connect",
        {
          user_id: user.userId,
          redirect_url: window.location.origin,
        },
        { sessionToken }
      );

      const redirect_url = data?.redirect_url;
      if (!redirect_url) {
        throw new Error("No redirect URL returned from server");
      }

      // redirect browser to consent URL
      window.location.href = redirect_url;
    } catch (err) {
      console.error("Gmail connection error:", err);
      alert(`Failed to connect Gmail: ${err?.message || err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleConnectGmail}
      disabled={loading}
      className="px-4 py-2 bg-blue-500 text-white rounded"
    >
      {loading ? "Connecting..." : "Connect Gmail"}
    </button>
  );
};

export default ConnectGmailButton;
