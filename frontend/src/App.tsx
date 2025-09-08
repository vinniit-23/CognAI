import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { DescopeProvider } from "./contexts/DescopeContext";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();
const DESCOPE_PROJECT_ID = import.meta.env.VITE_DESCOPE_PROJECT_ID || 'your-project-id';

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <DescopeProvider projectId={DESCOPE_PROJECT_ID}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Index />} />
              {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </DescopeProvider>
    </QueryClientProvider>
  );
};

export default App;
