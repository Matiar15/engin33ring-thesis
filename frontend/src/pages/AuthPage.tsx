import { Eye, EyeOff, Mail, Lock, User, Scan, ShieldCheck } from 'lucide-react';
import { AuthTab } from '@/features/auth/types'
import {useRegisterForm} from "@/features/auth/hooks/useRegisterForm.ts";
import AuthLogo from "@/features/auth/components/AuthLogo.tsx";


const AuthPage = () => {
  const {
    activeTab,
    password,
    showPassword,
    email,
    name,
    toggleActiveTab,
    toggleShowPassword,
    changePassword,
    changeEmail,
    changeName,
    handleSubmit
  } = useRegisterForm()

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 gradient-radial opacity-50" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />

      <div className="w-full max-w-md animate-fade-in">
        <AuthLogo />

        {/* Auth Card */}
        <div className="glass-panel rounded-2xl p-8 neon-border">
          {/* Tabs */}
          <div className="flex gap-2 mb-8 p-1 bg-muted/50 rounded-xl">
            {(['login', 'register'] as AuthTab[]).map((tab) => (
              <button
                key={tab}
                onClick={toggleActiveTab(tab)}
                className={`flex-1 py-3 px-4 rounded-lg font-display text-sm uppercase tracking-wider transition-all duration-300 ${
                  activeTab === tab
                    ? 'bg-primary text-primary-foreground shadow-lg'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div
              className={`space-y-2 overflow-hidden transition-[opacity,max-height] duration-300 ${
                activeTab === 'register'
                  ? 'opacity-100 max-h-40'
                  : 'opacity-0 max-h-0 pointer-events-none'
              }`}
            >
              <label className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="text"
                  value={name}
                  onChange={changeName}
                  placeholder="Enter your name"
                  className="w-full pl-12 pr-4 py-3.5 bg-input border border-border rounded-xl text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 focus-visible:ring-offset-0 focus-visible:border-primary transition-colors"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="email"
                  value={email}
                  onChange={changeEmail}
                  placeholder="Enter your email"
                  className="w-full pl-12 pr-4 py-3.5 bg-input border border-border rounded-xl text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 focus-visible:ring-offset-0 focus-visible:border-primary transition-colors"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={changePassword}
                  placeholder="Enter your password"
                  className="w-full pl-12 pr-12 py-3.5 bg-input border border-border rounded-xl text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 focus-visible:ring-offset-0 focus-visible:border-primary transition-colors"
                />
                <button
                  type="button"
                  onClick={toggleShowPassword}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-4 bg-primary text-primary-foreground font-display font-bold text-lg uppercase tracking-widest rounded-xl hover:bg-primary/90 transition-all duration-300 shadow-lg hover:shadow-primary/25 flex items-center justify-center gap-3"
            >
              <ShieldCheck className="w-5 h-5" />
              {activeTab === 'login' ? 'Access System' : 'Create Account'}
            </button>
          </form>

          {activeTab === 'login' && (
            <p className="text-center text-muted-foreground text-sm mt-6 transition-[opacity,max-height] duration-300 opacity-100 max-h-40">
              Demo mode: Any credentials will work
            </p>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-muted-foreground/60 text-sm mt-6">
          Powered by YOLOv8, React and FastAPI, built by Mateusz Sidor
        </p>
      </div>
    </div>
  );
};

export default AuthPage;
