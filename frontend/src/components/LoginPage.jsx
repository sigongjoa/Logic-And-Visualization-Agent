import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';

const LoginPage = () => {
    const [emailOrUsername, setEmailOrUsername] = useState('');
    const [password, setPassword] = useState('');
    const [userType, setUserType] = useState('student'); // Default to student
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await login(emailOrUsername, password, userType);
            // Assuming successful login returns a token and we store it
            localStorage.setItem('access_token', response.access_token);
            localStorage.setItem('user_type', userType); // Store user type for redirection

            if (userType === 'student') {
                navigate('/student/dashboard');
            } else if (userType === 'coach') {
                navigate('/coach');
            }
        } catch (err) {
            setError(err.message || 'Login failed. Please check your credentials.');
            console.error('Login error:', err);
        }
    };

    return (
        <main className="flex-grow">
            <div className="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
                <div className="relative hidden lg:flex flex-col items-center justify-center bg-primary p-12">
                    <div className="flex flex-col gap-6 text-white text-center max-w-md">
                        <div className="flex flex-col gap-2">
                            <h1 className="text-5xl font-black leading-tight tracking-[-0.033em]">Logic-And-Visualization-Agent</h1>
                            <h2 className="text-base font-normal leading-normal opacity-80">Navigate Your Learning Journey</h2>
                        </div>
                        <div className="w-full bg-center bg-no-repeat aspect-square bg-contain" data-alt="Abstract globe with interconnected nodes, representing a network of knowledge" style={{ backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuA3NQoBhDPfBE8okV4EXeaiBOp-bfAcVJrrxBLI9YXMsUPZypqUAgIz-W8KFssHwvUTgF69ZJldMso1fQD0-dwBr7igBEjZ5QDM_7sD0TtwtcXncOqZ9F6PCsZCWSIEeICmOGlgCZcMNvdk1hcR-sfsVKfbMSqcmW6IAPnDwxD3OByEe9uhp-jVQzfR9JlmraWCpwhTSUAgIz-W8KFssHwvUTgF69ZJldMso1fQD0-dwBr7igBEjZ5QDM_7sD0TtwtcXncOqZ9F6PCsZCWSIEeICmOGlgCZcMNvdk1hcR-sfsVKfbMSqcmW6IAPnDwxD3OByEe9uhp-jVQzfR9JlmraWCpwhTSZI-Hh2xmgnriNHyDBMAcuXsoLGaMAE0wM7c1ABJ9PXGWrOqCZQrfO9PBboGDveH37w1A")', backgroundPosition: 'center', borderRadius: '9999px', filter: 'grayscale(100%) contrast(1.2)', opacity: '0.2' }}></div>
                    </div>
                </div>
                <div className="flex flex-col items-center justify-center p-6 sm:p-12 bg-white dark:bg-background-dark">
                    <div className="w-full max-w-md flex flex-col gap-8">
                        <div className="flex flex-col gap-3 text-center lg:text-left">
                            <p className="text-[#111318] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Welcome Back</p>
                            <p className="text-[#616f89] dark:text-gray-400 text-base font-normal leading-normal">Please enter your details to log in.</p>
                        </div>
                        <div className="flex">
                            <div className="flex h-12 flex-1 items-center justify-center rounded-lg bg-background-light dark:bg-gray-800 p-1">
                                <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-gray-700 has-[:checked]:shadow-[0_0_4px_rgba(0,0,0,0.1)] has-[:checked]:text-[#111318] dark:has-[:checked]:text-white text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal transition-colors">
                                    <span className="truncate">Student</span>
                                    <input
                                        type="radio"
                                        name="user_type"
                                        value="student"
                                        checked={userType === 'student'}
                                        onChange={(e) => setUserType(e.target.value)}
                                        className="invisible w-0"
                                    />
                                </label>
                                <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-gray-700 has-[:checked]:shadow-[0_0_4px_rgba(0,0,0,0.1)] has-[:checked]:text-[#111318] dark:has-[:checked]:text-white text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal transition-colors">
                                    <span className="truncate">Coach</span>
                                    <input
                                        type="radio"
                                        name="user_type"
                                        value="coach"
                                        checked={userType === 'coach'}
                                        onChange={(e) => setUserType(e.target.value)}
                                        className="invisible w-0"
                                    />
                                </label>
                            </div>
                        </div>
                        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
                            <label className="flex flex-col flex-1">
                                <p className="text-[#111318] dark:text-white text-base font-medium leading-normal pb-2">Email Address</p>
                                <input
                                    type="email"
                                    placeholder="Enter your email"
                                    value={emailOrUsername}
                                    onChange={(e) => setEmailOrUsername(e.target.value)}
                                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111318] dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary dark:focus:border-primary h-14 placeholder:text-[#616f89] p-[15px] text-base font-normal leading-normal"
                                    required
                                />
                            </label>
                            <label className="flex flex-col flex-1">
                                <p className="text-[#111318] dark:text-white text-base font-medium leading-normal pb-2">Password</p>
                                <div className="flex w-full flex-1 items-stretch rounded-lg">
                                    <input
                                        type="password"
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-l-lg text-[#111318] dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-primary dark:focus:border-primary h-14 placeholder:text-[#616f89] p-[15px] border-r-0 text-base font-normal leading-normal"
                                        required
                                    />
                                    <button type="button" className="text-[#616f89] dark:text-gray-400 flex border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 items-center justify-center px-[15px] rounded-r-lg border-l-0 focus:outline-0 focus:ring-2 focus:ring-primary/50 focus:border-primary dark:focus:border-primary" data-alt="Toggle password visibility">
                                        <span className="material-symbols-outlined text-2xl">visibility</span>
                                    </button>
                                </div>
                                <div className="flex justify-end pt-2">
                                    <a className="text-sm font-medium text-primary hover:underline" href="#">Forgot Password?</a>
                                </div>
                            </label>
                            {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                            <button type="submit" className="flex items-center justify-center gap-2 px-6 py-4 rounded-lg bg-primary text-white text-base font-bold leading-normal shadow-[0_4px_14px_rgba(19,91,236,0.3)] hover:bg-opacity-90 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 dark:focus:ring-offset-background-dark">
                                <span>Log In</span>
                            </button>
                            <p className="text-center text-sm text-[#616f89] dark:text-gray-400">
                                Don't have an account? <a className="font-medium text-primary hover:underline" href="#">Sign Up</a>
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default LoginPage;
