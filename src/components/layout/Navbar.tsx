import React from 'react';
import Link from 'next/link';
import { Lock } from 'lucide-react';

const navigation = [
  {
    name: 'Resume Tools',
    href: '/resume-tools',
  },
  {
    name: 'Job & Career',
    href: '/jobs',
  },
  {
    name: 'Learning & Coaching',
    href: '/learning',
  },
  {
    name: 'AI Assistants',
    href: '/ai',
  },
  {
    name: 'Settings',
    href: '/settings',
  },
];

export const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-full bg-black flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="w-5 h-5 text-white" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m-8-8h16" />
              </svg>
            </div>
            <span className="text-xl font-semibold text-gray-900">Rezoomé</span>
          </Link>

          {/* Navigation */}
          <div className="hidden md:flex items-center justify-center flex-1 px-16">
            <div className="flex space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>

          {/* No resume data stored */}
          <div className="flex items-center space-x-2 px-4 py-1.5 bg-gray-50 rounded-full">
            <Lock className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-xs text-gray-500">No resume data stored</span>
          </div>
        </div>
      </div>
    </nav>
  );
}; 