
import React from 'react';
import { NavigationProps, Page } from '../types';

const CoachDashboard: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
<div className="font-display bg-[#f6f6f8] dark:bg-[#101622] text-[#333333] dark:text-white min-h-screen">
    <main className="w-full max-w-screen-2xl mx-auto p-6 lg:p-8">
        <div className="grid grid-cols-12 gap-6 lg:gap-8">
            <aside className="col-span-12 lg:col-span-3">
                <div className="flex flex-col gap-6">
                    <div className="sticky top-8 flex h-full flex-col justify-between bg-white dark:bg-[#101622] rounded-xl p-4 border border-gray-200 dark:border-gray-800">
                        <div className="flex flex-col gap-4">
                            <div className="flex items-center gap-3">
                                <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCfUl1mXsBlUa7bS3e5iPev3pCrvdGy9ux8PMWduOJs9-nziYSUg_kwjZFE2PMyYpAKdGCGeI2W0f7ycirFY0OBwEloa9xQp2VHW05CGDSDkb6MYHk_gU_ZYqBC1AP8qzeai6HZ_N8hIbBLgcLGOkW5oPKvF5E-Q0sVRdAaa-YfA4o_a2A7eHEYGxRrD9B8MsqTC8bMbuP6Ajz7Itk3Kdbg2hlhG5e_8z5Ch7wGKSuxfLkmnIBtnrb_3Brg0tyVVo_EdCB9Uai4yg")'}}></div>
                                <div className="flex flex-col">
                                    <h1 className="text-base font-medium leading-normal">Eleanor Vance</h1>
                                    <p className="text-[#7F8C8D] text-sm font-normal leading-normal">LAVA Coach</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white dark:bg-[#101622] p-4 rounded-xl border border-gray-200 dark:border-gray-800">
                        <h2 className="text-lg font-bold leading-tight tracking-[-0.015em] pb-3">My Students</h2>
                        <div className="flex items-center justify-start -space-x-3">
                            <div className="bg-center bg-no-repeat aspect-square bg-cover border-white dark:border-[#101622] rounded-full size-11 border-2" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDKSSYrwrxxYDmBhou03Ab9AtFj3qjIzuJS6uH9ztKsPWxlf2WTdALFzlojpgI3BmpmI2toFoF3NRJ0loDNiFnj78Lc9BbfCWxJ2hGEQ959P5iVzU26gry_5eS8_3yHtPAxObxH6iBFYW-TKyN5VQiOiv2Fiz3TLjpaGA0GXscjIJ5M-IZPW-lcX2zOswrM8IDuWYJBdW9Y02PJShyOYDNQuQ43NAVJDUAElTdLXS2nihBoCJXaaD6pz95lTJXeE-5RxivIPv2XGQ")'}}></div>
                            <div className="bg-center bg-no-repeat aspect-square bg-cover border-white dark:border-[#101622] rounded-full size-11 border-2" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDpBCELwnzwPPsdiKyygFhJdInlxhmDwtwDZOGX018p-EJIvvWZaoqd7ExNlvGe9ATrJPyZfG_kplTRMqMUrxMIVYZr428FCjlK4rydegAt6WcFWXKFGE4-WiN2JDoCXxZ1tnNg8qeTcdhWHT7Cqk5JYd7R5YD141RoY667hZ33ahtbmugeD5wazK50VRQt_7sPxdJ6ojiuXRw8n4PWTNUl4S5CoCuxHwN5SYaS9Ds_pqcs2IZ8HFecwxWxeeNOTAmu1k53JYRyuA")'}}></div>
                            <div className="bg-center bg-no-repeat aspect-square bg-cover border-white dark:border-[#101622] rounded-full size-11 border-2" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuBfc8vnjfD8ea34dZhiC37Gg06jBdDCNWBEF9Fe_7bQR9LvoR4MbDthKmrT4SHn6-m3WUVcTwFmeu1JPcoMp_EHW_zpWIfWEWANoZqhKWUzWTzmOsX4w4RlsfGPdxMNyNzEhKV9F5j4a6oDlh-7baEpAkgqzcekgHRmOiLBzp1XstRvRdAbvUqVeuwHoiGqAUqTSOocnltvvkOg9APS2d6Eu6lFfBudYUvpiJA5bD9QWoFOdZ1qXqHQ-0uE5UgMyjFkOp-m70wCFg")'}}></div>
                            <div className="bg-center bg-no-repeat aspect-square bg-cover border-white dark:border-[#101622] rounded-full size-11 border-2" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDqvY6evJSNBSI9H52vWfV54DB5NAJXJ5i4LzN_Okr6dBZWgDO8Yt6yKC1I2RDbPnbv-CPFawxav7S0_PVx0VJ-sr0ZSNDVWI5xEZNeie8kZ2K0okW68JC6X4_eSPfbF0y1z8a5iCIFF6SbUVKljYDGx-zaWc6aaDOsIf8o6NzxdNyRX-sjZXd1af_wJbH_6OqVhlw_X-1gjIMNQkvXswJ4gH282RuPYWE2AW85glHHAriH30NnBmPiDsnLA0JOAv584fBNeSu3RQ")'}}></div>
                            <div className="bg-gray-100 text-[#7F8C8D] border-white dark:border-[#101622] dark:bg-gray-800 rounded-full flex items-center justify-center size-11 border-2 font-semibold text-xs">
                                +12
                            </div>
                        </div>
                    </div>
                </div>
            </aside>
            <div className="col-span-12 lg:col-span-6">
                <div className="flex flex-col gap-6">
                    <div className="flex flex-wrap justify-between gap-3 items-center">
                        <h1 className="text-4xl font-black leading-tight tracking-[-0.033em]">Submissions to Review</h1>
                    </div>
                    <div className="bg-white dark:bg-[#101622] p-4 sm:p-6 rounded-xl border border-gray-200 dark:border-gray-800">
                        <div className="border-b border-gray-200 dark:border-gray-700">
                            <nav aria-label="Tabs" className="flex space-x-4">
                                <a className="px-3 py-2 font-medium text-sm rounded-t-lg border-b-2 border-[#135bec] text-[#135bec]" href="#">Pending (3)</a>
                                <a className="px-3 py-2 font-medium text-sm rounded-t-lg border-b-2 border-transparent text-[#7F8C8D] hover:text-[#333333] dark:hover:text-white" href="#">In Progress</a>
                                <a className="px-3 py-2 font-medium text-sm rounded-t-lg border-b-2 border-transparent text-[#7F8C8D] hover:text-[#333333] dark:hover:text-white" href="#">Reviewed</a>
                            </nav>
                        </div>
                        <div className="mt-4 flex flex-col gap-4">
                            <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:shadow-sm">
                                <div className="flex items-center gap-4">
                                    <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuA0QyQf_dQKHJBLJF0lBcJO0zn-vHL_GGtLVVH-n50uJMJy-gEf6O5SB_Qs7lUZkypdOkXF6ZWT_I0xx2yHGwCOnKOtLpxrDZ9wz1WBGYE7TCfiCDq2pk5EbEQh-X5-YGkxZHvVoxMXpMdSQFaAkCyKQWa9_DiWLb0kDKoxJ-kkt4ZqmSTIX0I3uRlhG18lAO0l__jos_s1ezy7slm2fqmSfeumQMMToCFdNZjMvsIZwn5JT7YOWoajfzSq_3rCytcq9oql4GupdQ")'}}></div>
                                    <div>
                                        <p className="font-semibold text-[#333333] dark:text-white">Marcus Holloway</p>
                                        <p className="text-sm text-[#7F8C8D]">Quantum Mechanics: Problem Set 3</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <div className="text-right">
                                        <p className="text-sm text-[#7F8C8D]">Due in 2 days</p>
                                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-[#F39C12]/20 text-[#F39C12]">Pending</span>
                                    </div>
                                    <button onClick={() => navigateTo(Page.AssignmentReview)} className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#135bec] text-white text-sm font-bold">Review Now</button>
                                </div>
                            </div>
                             <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:shadow-sm">
                                <div className="flex items-center gap-4">
                                    <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuA5dOkKkdFRH9ji0-EeePgk_3ebxst6Zz49tPadPnEuCnmGVH1XRHBjl__xT33nkgksyyN66iIQ-eSAkw3Iocibh5CW-FmYWoqf4XBL7TYL7igJeX5kosPlGU6Hdy0cgTBMlmu07B33FI4jJ9AcTNPmHKroIZmRqn4OL6NKK85lKjTEImHzCKUvLAhh9Mv-7Xqn_pNw77MhLvAbbscOneMw5gi6kgn8kVt0pbjD66D02I1SYq0FjWAO1QSU9qvotE9BQGiAwbYrUQ")'}}></div>
                                    <div>
                                        <p className="font-semibold text-[#333333] dark:text-white">Clara Lille</p>
                                        <p className="text-sm text-[#7F8C8D]">Advanced Astrophysics: Thesis Draft</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <div className="text-right">
                                        <p className="text-sm text-[#7F8C8D]">Due in 5 days</p>
                                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-[#F39C12]/20 text-[#F39C12]">Pending</span>
                                    </div>
                                    <button onClick={() => navigateTo(Page.AssignmentReview)} className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#135bec] text-white text-sm font-bold">Review Now</button>
                                </div>
                            </div>
                            <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:shadow-sm">
                                <div className="flex items-center gap-4">
                                    <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAdjwzSiQLFplMS3tgXOeGBrWkHysW-S7-qsWF3lHGXPlvaO4_6zvEKWjF62XdgbNwqf51DMrLjsicnz6ZSF-LzlhPjFVrBKI5xrNjcpgo76pgAXt5NPCAniRvKQ3y6OoPIHz6WQUDVlJRe9bw5lNHELKkaZNANDU-qfECEc46IAfL3lPkWkqb5w86ezup8UAtFf_tKfrulkkMqeTorURWN1kgZzNjpEskbCcRAByAF6ShqJMoyoIJiM36NBE6uSP_Xin4hvmIEDQ")'}}></div>
                                    <div>
                                        <p className="font-semibold text-[#333333] dark:text-white">Aiden Pearce</p>
                                        <p className="text-sm text-[#7F8C8D]">Organic Chemistry: Lab Report</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <div className="text-right">
                                        <p className="text-sm text-[#7F8C8D]">Due Yesterday</p>
                                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300">Overdue</span>
                                    </div>
                                    <button onClick={() => navigateTo(Page.AssignmentReview)} className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#135bec] text-white text-sm font-bold">Review Now</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <aside className="col-span-12 lg:col-span-3">
                <div className="sticky top-8 flex flex-col gap-6">
                    <div className="bg-white dark:bg-[#101622] p-4 rounded-xl border border-gray-200 dark:border-gray-800">
                        <h3 className="text-lg font-bold leading-tight tracking-[-0.015em] pb-4">Weekly Report Summary</h3>
                        <div className="flex flex-col gap-4">
                            <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                                <div>
                                    <p className="text-sm text-[#7F8C8D]">Submissions Reviewed</p>
                                    <p className="text-2xl font-bold text-[#333333] dark:text-white">14</p>
                                </div>
                                <div className="text-[#2ECC71]">
                                    <span className="material-symbols-outlined text-4xl">task_alt</span>
                                </div>
                            </div>
                            <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                                <div>
                                    <p className="text-sm text-[#7F8C8D]">Avg. Turnaround Time</p>
                                    <p className="text-2xl font-bold text-[#333333] dark:text-white">2.1 days</p>
                                </div>
                                <div className="text-[#135bec]">
                                    <span className="material-symbols-outlined text-4xl">hourglass_top</span>
                                </div>
                            </div>
                            <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                                <div>
                                    <p className="text-sm text-[#7F8C8D]">Student Engagement</p>
                                    <p className="text-2xl font-bold text-[#333333] dark:text-white">89%</p>
                                </div>
                                <div className="text-[#F39C12]">
                                    <span className="material-symbols-outlined text-4xl">trending_up</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>
        </div>
    </main>
</div>
  );
};

export default CoachDashboard;
