import { createContext, useContext, useState, ReactNode } from 'react';

interface MockUser {
  userId: string;
  email: string;
  name?: string;
  picture?: string;
}

interface DescopeContextType {
  sdk: {
    flow: {
      start: (flowId: string) => Promise<{ ok: boolean }>;
    };
    outbound: {
      connect: (provider: string, options: { redirectUrl: string }) => Promise<void>;
    };
    logout: () => Promise<void>;
  };
  user: MockUser | null;
  isAuthenticated: boolean;
}

const DescopeContext = createContext<DescopeContextType | null>(null);

export const useDescope = () => {
  const context = useContext(DescopeContext);
  if (!context) {
    throw new Error('useDescope must be used within DescopeProvider');
  }
  return context.sdk;
};

export const useSession = () => {
  const context = useContext(DescopeContext);
  if (!context) {
    throw new Error('useSession must be used within DescopeProvider');
  }
  return { isAuthenticated: context.isAuthenticated };
};

export const useUser = () => {
  const context = useContext(DescopeContext);
  if (!context) {
    throw new Error('useUser must be used within DescopeProvider');
  }
  return { user: context.user };
};

interface DescopeProviderProps {
  children: ReactNode;
  projectId: string;
}

export const DescopeProvider = ({ children, projectId }: DescopeProviderProps) => {
  const [user, setUser] = useState<MockUser | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Mock SDK for development - replace with real Descope implementation
  const sdk = {
    flow: {
      start: async (flowId: string) => {
        // Mock sign-in flow
        console.log(`Mock: Starting flow ${flowId} for project ${projectId}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockUser: MockUser = {
          userId: 'mock-user-123',
          email: 'user@example.com',
          name: 'Demo User',
          picture: undefined,
        };
        
        setUser(mockUser);
        setIsAuthenticated(true);
        return { ok: true };
      },
    },
    outbound: {
      connect: async (provider: string, options: { redirectUrl: string }) => {
        console.log(`Mock: Connecting ${provider} with redirect to ${options.redirectUrl}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        // Mock successful connection
      },
    },
    logout: async () => {
      setUser(null);
      setIsAuthenticated(false);
    },
  };

  const contextValue = {
    sdk,
    user,
    isAuthenticated,
  };

  return (
    <DescopeContext.Provider value={contextValue}>
      {children}
    </DescopeContext.Provider>
  );
};