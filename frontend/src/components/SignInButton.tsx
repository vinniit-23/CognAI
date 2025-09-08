import { useDescope, useSession, useUser } from '@/contexts/DescopeContext';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { LogIn, LogOut, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const FLOW_ID = import.meta.env.VITE_DESCOPE_FLOW_ID || 'sign-in-or-up';

export default function SignInButton() {
  const sdk = useDescope();
  const { isAuthenticated } = useSession();
  const { user } = useUser();
  const { toast } = useToast();

  const handleSignIn = async () => {
    try {
      const result = await sdk.flow.start(FLOW_ID);
      if (result.ok) {
        toast({
          title: "Welcome!",
          description: "Successfully signed in to CognAI",
        });
      } else {
        toast({
          title: "Sign-in failed",
          description: "Please try again",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Sign-in error:', error);
      toast({
        title: "Sign-in error",
        description: "An unexpected error occurred",
        variant: "destructive",
      });
    }
  };

  const handleSignOut = async () => {
    try {
      await sdk.logout();
      toast({
        title: "Signed out",
        description: "You have been successfully signed out",
      });
    } catch (error) {
      console.error('Sign-out error:', error);
    }
  };

  if (isAuthenticated && user) {
    return (
      <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
        <Avatar className="w-8 h-8">
          <AvatarImage src={user.picture} alt={user.name || 'User'} />
          <AvatarFallback>
            <User size={16} />
          </AvatarFallback>
        </Avatar>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">
            {user.name || user.email || 'User'}
          </p>
          <p className="text-xs text-muted-foreground truncate">
            {user.email}
          </p>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleSignOut}
          className="px-2"
        >
          <LogOut size={16} />
        </Button>
      </div>
    );
  }

  return (
    <Button 
      onClick={handleSignIn}
      className="w-full"
      variant="default"
    >
      <LogIn size={16} className="mr-2" />
      Sign In
    </Button>
  );
}