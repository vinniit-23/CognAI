import { Descope } from "@descope/react-sdk";

function SignInFlow({ onSuccess }) {
  const flowId = import.meta.env.VITE_DESCOPE_FLOW_ID;

  if (!flowId) {
    return (
      <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
        <div className="text-center">
          <span className="text-2xl mb-2 block">⚠️</span>
          <p className="text-sm font-medium">Configuration Error</p>
          <p className="text-xs text-muted-foreground mt-1">
            Missing VITE_DESCOPE_FLOW_ID in environment variables
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <Descope
        flowId={flowId}
        theme="light"
        debug={true} // ✅ Enable debug for troubleshooting
        onSuccess={(e) => {
          console.log("✅ Sign in successful:", e.detail);
          // ✅ Call the success callback with a slight delay to ensure state updates
          setTimeout(() => {
            if (onSuccess) {
              onSuccess(e);
            }
          }, 100);
        }}
        onError={(e) => {
          console.error("❌ Sign in error:", e.detail || e);
        }}
        onReady={() => {
          console.log("🔄 Flow is ready");
        }}
      />
    </div>
  );
}

export default SignInFlow;
