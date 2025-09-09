import { createRoot } from "react-dom/client";
import { AuthProvider } from "@descope/react-sdk";
import App from "./App.jsx";
import "./styles/index.css";

// Get Descope project ID from environment
const projectId = import.meta.env.VITE_DESCOPE_PROJECT_ID;

function EnvironmentCheck({ children }) {
  if (!projectId) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-8">
        <div className="max-w-md text-center space-y-4">
          <div className="w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center mx-auto">
            <span className="text-2xl">⚠️</span>
          </div>
          <h1 className="text-2xl font-bold text-foreground">
            Configuration Required
          </h1>
          <div className="text-left bg-card border border-border rounded-lg p-4 space-y-3">
            <p className="text-sm text-muted-foreground">
              Missing environment variables:
            </p>
            <div className="bg-muted rounded p-2">
              <code className="text-xs">VITE_DESCOPE_PROJECT_ID</code>
            </div>
            <div className="text-xs text-muted-foreground space-y-2">
              <p>
                1. Copy <code>.env.local.example</code> to{" "}
                <code>.env.local</code>
              </p>
              <p>2. Add your Descope project ID from your Descope console</p>
              <p>3. Refresh the page</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return children;
}

createRoot(document.getElementById("root")).render(
  <EnvironmentCheck>
    <AuthProvider projectId={projectId} sessionTokenViaCookie>
      <App />
    </AuthProvider>
  </EnvironmentCheck>
);
