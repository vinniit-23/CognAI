import { useState } from 'react';
import { useSession, useUser } from '@/contexts/DescopeContext';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Mail, Calendar, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { getEmails, EmailMessage } from '@/api/backend';

export default function EmailsModal() {
  const { isAuthenticated } = useSession();
  const { user } = useUser();
  const [emails, setEmails] = useState<EmailMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const { toast } = useToast();

  const handleFetchEmails = async () => {
    if (!isAuthenticated || !user) {
      toast({
        title: "Sign in required",
        description: "Please sign in and connect Gmail first",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await getEmails(user.userId, 10);
      setEmails(response.messages);
      setIsOpen(true);
      
      toast({
        title: "Emails fetched",
        description: `Retrieved ${response.messages.length} emails`,
      });
    } catch (error) {
      console.error('Fetch emails error:', error);
      toast({
        title: "Failed to fetch emails",
        description: "Make sure Gmail is connected and try again",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString([], {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button 
          onClick={handleFetchEmails}
          disabled={isLoading || !isAuthenticated}
          variant="outline"
          className="w-full"
        >
          {isLoading ? (
            <Loader2 size={16} className="mr-2 animate-spin" />
          ) : (
            <Mail size={16} className="mr-2" />
          )}
          {isLoading ? 'Fetching...' : 'Fetch Emails'}
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Mail size={20} />
            Recent Emails ({emails.length})
          </DialogTitle>
        </DialogHeader>
        
        <div className="overflow-y-auto space-y-3 pr-2">
          {emails.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <Mail size={48} className="mx-auto mb-4 opacity-50" />
              <p>No emails to display</p>
              <p className="text-sm">Make sure Gmail is connected</p>
            </div>
          ) : (
            emails.map((email) => (
              <Card key={email.id} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-sm font-medium line-clamp-1">
                      {email.subject}
                    </CardTitle>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Calendar size={12} />
                      {formatDate(email.date)}
                    </div>
                  </div>
                  <CardDescription className="flex items-center gap-1 text-xs">
                    <User size={12} />
                    {email.from}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {email.snippet}
                  </p>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}