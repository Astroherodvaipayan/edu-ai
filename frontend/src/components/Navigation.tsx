'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

export default function Navigation() {
  const router = useRouter();
  const { user, signOut } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleSignOut = async () => {
    try {
      await signOut();
      router.push('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const mainFeatures = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Audio Upload', path: '/audio' },
    { name: 'YouTube Learning', path: '/youtube' },
    { name: 'PDF Analysis', path: '/pdf' },
    { name: 'Chat', path: '/chat' },
    { name: 'Concept Detective', path: '/concept-detective' },
  ];

  const additionalFeatures = [
    { name: 'Voice Chat', path: '/features/voice-chat' },
    { name: 'Learning Analytics', path: '/features/analytics' },
    { name: 'Study Groups', path: '/features/groups' },
    { name: 'Resource Library', path: '/features/resources' },
  ];

  if (!user) return null;

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Main Features */}
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-emerald-600">EduAIthon</span>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-4">
              {mainFeatures.map((feature) => (
                <button
                  key={feature.path}
                  onClick={() => router.push(feature.path)}
                  className="text-gray-600 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  {feature.name}
                </button>
              ))}
            </div>
          </div>

          {/* User Menu and Additional Features */}
          <div className="flex items-center space-x-4">
            {/* Additional Features Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="bg-emerald-50 text-emerald-600 hover:bg-emerald-100 px-4 py-2 rounded-lg text-sm font-medium flex items-center space-x-1"
              >
                <span>More Features</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {showDropdown && (
                <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                  <div className="py-1">
                    {additionalFeatures.map((feature) => (
                      <button
                        key={feature.path}
                        onClick={() => {
                          router.push(feature.path);
                          setShowDropdown(false);
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-emerald-50"
                      >
                        {feature.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Profile Button */}
            <button
              onClick={() => router.push('/profile')}
              className="bg-emerald-600 text-white hover:bg-emerald-500 px-4 py-2 rounded-lg text-sm font-medium"
            >
              Profile
            </button>

            {/* Sign Out Button */}
            <button
              onClick={handleSignOut}
              className="text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className="sm:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1">
          {mainFeatures.map((feature) => (
            <button
              key={feature.path}
              onClick={() => router.push(feature.path)}
              className="block w-full text-left px-3 py-2 text-base font-medium text-gray-600 hover:text-emerald-600 hover:bg-emerald-50 rounded-md"
            >
              {feature.name}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
} 