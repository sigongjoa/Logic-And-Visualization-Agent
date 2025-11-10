
import React, { useState } from 'react';
import { UserType } from '../types';

interface LoginPageProps {
    onLogin: (userType: UserType) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
    const [userType, setUserType] = useState<UserType>('student');
  
    return (
        <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden">
            <main className="flex-grow">
                <div className="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
                    <div className="relative hidden lg:flex flex-col items-center justify-center bg-[#135bec] p-12">
                        <div className="flex flex-col gap-6 text-white text-center max-w-md">
                            <div className="flex flex-col gap-2">
                                <h1 className="text-5xl font-black leading-tight tracking-[-0.033em]">Logic-And-Visualization-Agent</h1>
                                <h2 className="text-base font-normal leading-normal opacity-80">Navigate Your Learning Journey</h2>
                            </div>
                            <div className="w-full bg-center bg-no-repeat aspect-square bg-contain" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuA3NQoBhDPfBE8okV4EXeaiBOp-bfAcVJrrxBLI9YXMsUPZypqUAgIz-W8KFssHwvUTgF69ZJldMso1fQD0-dwBr7igBEjZ5QDM_7sD0TtwtcXncOqZ9F6PCsZCWSIEeICmOGlgCZcMNvdk1hcR-sfsVKfbMSqcmW6IAPnDwxD3OByEe9uhp-jVQzfR9JlmraWCpwhTSqZI-Hh2xmgnriNHyDBMAcuXsoLGaMAE0wM7c1ABJ9PXGWrOqCZQrfO9PBboGDveH37w1A")', backgroundPosition: 'center', borderRadius: '9999px', filter: 'grayscale(100%) contrast(1.2)', opacity: '0.2'}}></div>
                        </div>
                    </div>
                    <div className="flex flex-col items-center justify-center p-6 sm:p-12 bg-white dark:bg-[#101622]">
                        <div className="w-full max-w-md flex flex-col gap-8">
                            <div className="flex flex-col gap-3 text-center lg:text-left">
                                <p className="text-[#111318] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Welcome Back</p>
                                <p className="text-[#616f89] dark:text-gray-400 text-base font-normal leading-normal">Please enter your details to log in.</p>
                            </div>
                            <div className="flex">
                                <div className="flex h-12 flex-1 items-center justify-center rounded-lg bg-[#f6f6f8] dark:bg-gray-800 p-1">
                                    <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-gray-700 has-[:checked]:shadow-[0_0_4px_rgba(0,0,0,0.1)] has-[:checked]:text-[#111318] dark:has-[:checked]:text-white text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal transition-colors">
                                        <span className="truncate">Student</span>
                                        <input onChange={() => setUserType('student')} checked={userType === 'student'} className="invisible w-0" name="user_type" type="radio" value="Student"/>
                                    </label>
                                    <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-gray-700 has-[:checked]:shadow-[0_0_4px_rgba(0,0,0,0.1)] has-[:checked]:text-[#111318] dark:has-[:checked]:text-white text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal transition-colors">
                                        <span className="truncate">Coach</span>
                                        <input onChange={() => setUserType('coach')} checked={userType === 'coach'} className="invisible w-0" name="user_type" type="radio" value="Coach"/>
                                    </label>
                                </div>
                            </div>
                            <div className="flex flex-col gap-6">
                                <label className="flex flex-col flex-1">
                                    <p className="text-[#111318] dark:text-white text-base font-medium leading-normal pb-2">Email Address</p>
                                    <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111318] dark:text-white focus:outline-0 focus:ring-2 focus:ring-[#135bec]/50 border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-[#135bec] dark:focus:border-[#135bec] h-14 placeholder:text-[#616f89] p-[15px] text-base font-normal leading-normal" placeholder="Enter your email" type="email" />
                                </label>
                                <label className="flex flex-col flex-1">
                                    <p className="text-[#111318] dark:text-white text-base font-medium leading-normal pb-2">Password</p>
                                    <div className="flex w-full flex-1 items-stretch rounded-lg">
                                        <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-l-lg text-[#111318] dark:text-white focus:outline-0 focus:ring-2 focus:ring-[#135bec]/50 border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 focus:border-[#135bec] dark:focus:border-[#135bec] h-14 placeholder:text-[#616f89] p-[15px] border-r-0 text-base font-normal leading-normal" placeholder="Enter your password" type="password" />
                                        <button className="text-[#616f89] dark:text-gray-400 flex border border-[#dbdfe6] dark:border-gray-600 bg-white dark:bg-gray-800 items-center justify-center px-[15px] rounded-r-lg border-l-0 focus:outline-0 focus:ring-2 focus:ring-[#135bec]/50 focus:border-[#135bec] dark:focus:border-[#135bec]">
                                            <span className="material-symbols-outlined text-2xl">visibility</span>
                                        </button>
                                    </div>
                                </label>
                            </div>
                            <div className="flex flex-col gap-4">
                                <button onClick={() => onLogin(userType)} className="flex items-center justify-center gap-2 px-6 py-4 rounded-lg bg-[#135bec] text-white text-base font-bold leading-normal shadow-[0_4px_14px_rgba(19,91,236,0.3)] hover:bg-opacity-90 transition-colors focus:outline-none focus:ring-2 focus:ring-[#135bec] focus:ring-offset-2 dark:focus:ring-offset-[#101622]">
                                    <span>Log In</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default LoginPage;
