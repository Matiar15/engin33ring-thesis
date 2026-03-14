import {AuthTab} from "@/features/auth/types";
import {Scan} from "lucide-react";

const AuthLogo = () => {
  return (
      <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-primary/10 neon-border mb-4 animate-glow-pulse">
              <Scan className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-3xl font-display font-bold neon-text text-primary tracking-wider">
              MS TRAFFIC SIGN ANALYZER
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">
              Traffic Sign Recognition System
          </p>
      </div>
  )
}

export default AuthLogo;