import {useCallback, useState} from "react";
import {AuthTab} from "@/features/auth/types";
import {useNavigate} from "react-router-dom";

export function useRegisterForm() {
    const navigate = useNavigate();

    const onLogin = useCallback(() => {
        // W prawdziwej aplikacji tu byłaby logika autoryzacji
        // Na razie po prostu przekierowujemy do dashboardu
        navigate('/analysis');
    }, [navigate]);

    const [activeTab, setActiveTab] = useState<AuthTab>('login');
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');

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

    const handleSubmit = useCallback((e: React.FormEvent) => {
        e.preventDefault();
        // Here you would typically handle form submission, e.g., call an API to register the user
        // For this example, we'll just log the form data and switch to the login tab
        console.log('Registering user:', { name, email, password });
        onLogin();
    }, [name, email, password, onLogin]);

    return {
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
        handleSubmit,
    }
}