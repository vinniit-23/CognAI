import axios from "axios";
import { getSessionToken, useUser } from "@descope/react-sdk";

export default function ConnectGmailButton() {
  const { user } = useUser();

  const handleConnectGmail = async () => {
    if (!user?.userId) {
      alert("User ID missing. Please sign in first.");
      return;
    }

    try {
      // First try Descope connect
      const sessionToken = getSessionToken();
      const res = await axios.post("http://localhost:8000/auth/connect", {
        user_id: user.userId,
        session_token: sessionToken,
        redirect_url: "http://localhost:8080",
      });

      if (res.data?.url) {
        window.location.href = res.data.url;
      }
    } catch (err) {
      console.error("Descope connect failed, falling back to Google:", err);

      // Fallback to Google
      try {
        const res = await axios.get(
          `http://localhost:8000/google/connect?user_id=${user.userId}`
        );
        if (res.data?.url) {
          window.location.href = res.data.url;
        }
      } catch (e) {
        console.error("Google connect also failed:", e);
        alert("Failed to connect Gmail. Check console for details.");
      }
    }
  };

  return (
    <button
      onClick={handleConnectGmail}
      className="bg-blue-500 text-white px-4 py-2 rounded"
    >
      Connect Gmail
    </button>
  );
}
