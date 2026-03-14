import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NotFound from "@/components/NotFound.tsx";
import { Toaster } from "@/components/sonner.tsx";
import AuthPage from "@/pages/AuthPage.tsx";
import RegistryPage from "@/pages/RegistryPage.tsx";
import AnalysisPage from "@/pages/AnalysisPage.tsx";
import { VideoAnalysisProvider } from "@/features/analysis/context";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <Toaster />
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/registry" element={<RegistryPage/>} />
        <Route path="/analysis" element={
          <VideoAnalysisProvider>
            <AnalysisPage/>
          </VideoAnalysisProvider>
        } />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
