import { useState } from 'react';
import { useDescope, useSession, useUser } from '@/contexts/DescopeContext';
import { Button } from '@/components/ui/button';
import { Mail, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { notifyConnection } from '@/api/backend';

export default function ConnectButton() {
  const sdk = useDescope();
  const { isAuthenticated } = useSession();
  const { user } = useUser();
  const [isConnecting, setIsConnecting] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const { toast } = useToast();

  const handleConnect = async () => {
    if (!isAuthenticated || !user) {
      toast({
        title: "Sign in required",
        description: "Please sign in first to connect Gmail",
        variant: "destructive",
      });
      return;
    }

    setIsConnecting(true);
    
    try {
      // Connect Gmail via Descope Outbound App
      await sdk.outbound.connect('gmail', {
        redirectUrl: window.location.origin,
      });

      // After successful connection, notify the backend
      await notifyConnection(user.userId);
      
      setIsConnected(true);
      toast({
        title: "Gmail connected!",
        description: "Successfully connected your Gmail account",
      });
    } catch (error) {
      console.error('Gmail connection error:', error);
      toast({
        title: "Connection failed",
        description: "Failed to connect Gmail. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsConnecting(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <Button 
        variant="outline" 
        disabled 
        className="w-full"
      >
        <Mail size={16} className="mr-2" />
        Connect Gmail
        <span className="text-xs text-muted-foreground ml-2">(Sign in first)</span>
      </Button>
    );
  }

  if (isConnected) {
    return (
      <Button 
        variant="outline" 
        disabled 
        className="w-full border-green-200 bg-green-50 text-green-700 dark:border-green-800 dark:bg-green-950 dark:text-green-300"
      >
        <CheckCircle size={16} className="mr-2" />
        Gmail Connected
      </Button>
    );
  }

  return (
    <Button 
      onClick={handleConnect}
      disabled={isConnecting}
      variant="outline"
      className="w-full"
    >
      {isConnecting ? (
        <Loader2 size={16} className="mr-2 animate-spin" />
      ) : (
        <Mail size={16} className="mr-2" />
      )}
      {isConnecting ? 'Connecting...' : 'Connect Gmail'}
    </Button>
  );
}