import {useCallback, useState} from "react";
import {AuthTab} from "@/features/auth/types";
import {useNavigate} from "react-router-dom";
import {authService} from "@/services/authService";
import {toast} from "sonner";
import {useAuth} from "@/features/auth/context";

export function useRegisterForm() {
    const navigate = useNavigate();
    const { login: authLogin } = useAuth();

    const onLogin = useCallback(() => {
        navigate('/analysis');
    }, [navigate]);

    const [activeTab, setActiveTab] = useState<AuthTab>('login');
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const toggleActiveTab = useCallback((tab: AuthTab) => () => {
        setActiveTab(tab);
    }, []);

    const toggleShowPassword = useCallback(() => {
        setShowPassword((prev) => !prev);
    }, []);

    const changePassword = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    }, []);

    const changeEmail = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    }, []);

    const changeName = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value);
    }, []);

    const handleSubmit = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            if (activeTab === 'register') {
                await authService.register({
                    login: name,
                    email,
                    password,
                    full_name: name,
                });
                toast.success('Registration successful! Please log in.');
                setActiveTab('login');
            } else {
                const response = await authService.login({ email, password });

                // Decode JWT to get userId
                const parts = response.access_token.split('.');
                const payload = JSON.parse(atob(parts[1]));
                const userId = payload.sub;

                authLogin(response.access_token, userId);
                toast.success('Login successful!');
                onLogin();
            }
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'An error occurred';
            toast.error(activeTab === 'register' ? 'Registration failed: ' + errorMessage : 'Login failed: ' + errorMessage);
            console.error('Auth error:', error);
        } finally {
            setIsLoading(false);
        }
    }, [name, email, password, onLogin, activeTab, authLogin]);

    return {
        activeTab,
        password,
        showPassword,
        email,
        name,
        isLoading,
        toggleActiveTab,
        toggleShowPassword,
        changePassword,
        changeEmail,
        changeName,
        handleSubmit,
    }
}