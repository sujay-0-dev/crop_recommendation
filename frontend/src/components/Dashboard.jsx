import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const Dashboard = ({ user }) => {
    const { t, i18n } = useTranslation();
    const [dashboardData, setDashboardData] = useState({ leaderboard: [], advisories: {} });

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                // In a real app, this data would be fetched from the backend
                // For now, we'll use the data passed from props or fetch it
                const response = await axios.get('http://localhost:5000/api/dashboard');
                setDashboardData(response.data);
            } catch (error) {
                console.error("Failed to fetch dashboard data:", error);
            }
        };
        fetchDashboardData();
    }, []);
    
    const currentAdvisory = dashboardData.advisories?.[i18n.language] || dashboardData.advisories?.en;

    return (
        <div className="p-4 md:p-8">
            <h2 className="text-2xl font-bold text-center mb-6 text-green-800">{t('dashboard')}</h2>
            
            {/* Today's Advisory */}
            {currentAdvisory && (
                <div className="bg-blue-50 border-l-4 border-blue-500 text-blue-800 p-4 rounded-lg shadow-md mb-6">
                    <h3 className="font-bold text-lg mb-2">{t('advisory')}</h3>
                    <p>{currentAdvisory}</p>
                </div>
            )}
            
            {/* Progress Tracker */}
            <div className="bg-white p-4 rounded-xl shadow-md mb-6">
                <h3 className="text-xl font-bold mb-4 text-green-800">{t('progress')}</h3>
                <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-600">{user?.progress?.currentStage}</span>
                    <span className="font-bold text-green-600">{user?.progress?.completion}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                        className="bg-green-500 h-4 rounded-full transition-all duration-500"
                        style={{ width: `${user?.progress?.completion}%` }}
                    ></div>
                </div>
            </div>

            {/* Badges */}
            <div className="bg-white p-4 rounded-xl shadow-md mb-6">
                 <h3 className="text-xl font-bold mb-4 text-green-800">{t('badges')}</h3>
                <div className="grid grid-cols-3 gap-4 text-center">
                    {user?.badges && Object.entries(user.badges).map(([key, earned]) => (
                        <div key={key} className={`p-2 rounded-xl transition-opacity ${earned ? 'bg-green-100' : 'bg-gray-100 opacity-50'}`}>
                            <div className="text-4xl mb-1">{key === 'firstHarvest' ? '🥇' : key === 'savedWater' ? '💧' : '🛡️'}</div>
                            <span className="text-xs font-medium">{t(key)}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Leaderboard */}
            <div className="bg-white p-4 rounded-xl shadow-md">
                <h3 className="text-xl font-bold mb-4 text-green-800">{t('leaderboard')}</h3>
                {dashboardData.leaderboard.map((player, index) => (
                    <div key={index} className="flex items-center justify-between py-2 border-b last:border-0">
                        <span className="font-medium text-gray-700">{index + 1}. {player.name}</span>
                        <span className="text-green-600 font-bold">{player.yield} kg/acre</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;