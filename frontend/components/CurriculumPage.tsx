
import React from 'react';
import { NavigationProps } from '../types';

const CurriculumPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="font-lexend">
        <div className="relative flex h-auto min-h-screen w-full flex-col bg-[#f6f6f8] dark:bg-[#101622] text-slate-800 dark:text-slate-200">
            <main className="flex-1 flex flex-col p-6 lg:p-10">
                <div className="flex flex-col gap-4 mb-6">
                    <div className="flex flex-wrap justify-between gap-3">
                        <div className="flex min-w-72 flex-col gap-2">
                            <p className="text-slate-900 dark:text-slate-100 text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">Curriculum Knowledge Graph</p>
                            <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Explore the connections between different topics and concepts on your learning path.</p>
                        </div>
                    </div>
                    <div className="max-w-md">
                        <label className="flex flex-col min-w-40 h-12 w-full">
                            <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                                <div className="text-slate-400 dark:text-slate-500 flex bg-white dark:bg-slate-900/50 items-center justify-center pl-4 rounded-l-lg border border-slate-200 dark:border-slate-800 border-r-0">
                                    <span className="material-symbols-outlined">search</span>
                                </div>
                                <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-slate-900 dark:text-slate-100 focus:outline-0 focus:ring-2 focus:ring-[#135bec]/50 border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/50 h-full placeholder:text-slate-400 dark:placeholder:text-slate-500 pl-2 text-base font-normal leading-normal" placeholder="Search for a specific topic..." />
                            </div>
                        </label>
                    </div>
                </div>
                <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-[600px]">
                    <div className="lg:col-span-2 relative flex flex-col bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
                        <div className="absolute top-4 left-4 z-10 flex gap-2 bg-white/70 dark:bg-[#101622]/70 backdrop-blur-sm p-1 rounded-lg border border-slate-200/80 dark:border-slate-800/80">
                            <button className="p-2 text-slate-700 dark:text-slate-300 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                                <span className="material-symbols-outlined">zoom_in</span>
                            </button>
                            <button className="p-2 text-slate-700 dark:text-slate-300 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                                <span className="material-symbols-outlined">zoom_out</span>
                            </button>
                            <button className="p-2 text-slate-700 dark:text-slate-300 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                                <span className="material-symbols-outlined">fullscreen_exit</span>
                            </button>
                        </div>
                        <div className="flex w-full grow bg-white dark:bg-slate-900/50 p-3 rounded-xl">
                            <div className="w-full bg-center bg-no-repeat bg-cover aspect-auto rounded-lg flex-1" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDpqKzhkDYXW464rY0yK0HyweFkfwc85iorj-x7zLs0Qxoze6ciZDid2tLYp0-OeWF3XT_YBv64O10d1_rVOdObKwPzoMnH0VNRSIzrCBrZzLzwwtiB3pN25tV78UF_-6EUAQMytEepIuzv8-6-3lvpUJH6DspIqFxJqPbh1p6duLjrvXqhGZigGYaFOGni07M97CVuNgU5lCGBDiaNUqkPbZ8p6VScj-BAAZV_PUZ0jxlbX22uhPzimwJ_chGTTYAJAQ6A5WBZAA")'}}></div>
                        </div>
                    </div>
                    <aside className="lg:col-span-1 flex flex-col bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 space-y-6">
                        <div className="flex flex-col gap-2">
                            <div className="flex items-center gap-3">
                                <h3 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Linear Equations</h3>
                                <span className="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/40 px-3 py-1 text-xs font-medium text-green-700 dark:text-green-300">Completed</span>
                            </div>
                            <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">This topic covers the fundamentals of linear equations, including how to solve for variables, graph lines, and understand slope-intercept form. It's a foundational concept in algebra.</p>
                        </div>
                        <div className="flex flex-col gap-4">
                            <h4 className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Prerequisites</h4>
                            <a className="flex items-center gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 transition-colors" href="#">
                                <span className="material-symbols-outlined text-[#135bec] text-xl">link</span>
                                <span className="font-medium text-slate-800 dark:text-slate-200">Introduction to Algebra</span>
                            </a>
                        </div>
                        <div className="flex flex-col gap-4">
                            <h4 className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Key Concepts</h4>
                            <ul className="space-y-2">
                                <li className="flex items-start gap-3">
                                    <span className="material-symbols-outlined text-[#135bec]/80 mt-0.5">check_circle</span>
                                    <span className="text-slate-700 dark:text-slate-300">Solving for 'x'</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="material-symbols-outlined text-[#135bec]/80 mt-0.5">check_circle</span>
                                    <span className="text-slate-700 dark:text-slate-300">Graphing lines on a Cartesian plane</span>
                                </li>
                                <li className="flex items-start gap-3">
                                    <span className="material-symbols-outlined text-[#135bec]/80 mt-0.5">check_circle</span>
                                    <span className="text-slate-700 dark:text-slate-300">Understanding slope-intercept form (y=mx+b)</span>
                                </li>
                            </ul>
                        </div>
                        <div className="pt-4 mt-auto">
                            <button className="w-full flex items-center justify-center gap-2 rounded-lg bg-[#135bec] h-12 px-6 text-base font-medium text-white shadow-sm transition-all hover:bg-[#135bec]/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#135bec]">
                                <span className="material-symbols-outlined">refresh</span>
                                Review Topic
                            </button>
                        </div>
                    </aside>
                </div>
            </main>
        </div>
    </div>
  );
};

export default CurriculumPage;
