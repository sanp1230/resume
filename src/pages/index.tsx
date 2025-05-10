import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Search, Play, MessageSquare } from 'lucide-react';
import Link from 'next/link';
import { FeatureCard } from '@/components/ui/FeatureCard';
import { Navbar } from '@/components/layout/Navbar';

const features = [
  {
    icon: FileText,
    title: 'Resume Analysis',
    description: 'Analyze your resume, get an ATS score, and tailored suggestions',
    href: '/resume-tools/analysis',
    buttonText: 'Get Started',
  },
  {
    icon: Search,
    title: 'Job Search',
    description: 'Find relevant job opportunities quickly and easily',
    href: '/jobs/search',
    buttonText: 'Find Jobs',
  },
  {
    icon: Play,
    title: 'Course Suggestions',
    description: 'Discover free courses to develop the skills you need',
    href: '/learning/courses',
    buttonText: 'Explore Courses',
  },
  {
    icon: MessageSquare,
    title: 'Resume Coach chatbot',
    description: 'Chat with our AI assistant to enhance your resume',
    href: '/ai/resume-coach',
    buttonText: 'Chat Now',
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* Hero Section */}
      <div className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <h1 className="text-[64px] font-bold tracking-tight text-gray-900 mb-6">
              Craft Your Future
            </h1>
            <p className="text-xl leading-relaxed text-gray-600 max-w-3xl mx-auto mb-12">
              Enhance your resume and accelerate your career with our suite of AI-powered tools.
            </p>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                href="/resume-tools/analysis"
                className="inline-flex items-center justify-center rounded-full bg-black px-8 py-4 text-base font-medium text-white shadow-sm hover:bg-gray-900 transition-colors"
              >
                Get Started
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-32">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature) => (
            <FeatureCard key={feature.title} {...feature} />
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-center space-x-8">
          <Link href="/about" className="text-sm text-gray-500 hover:text-gray-900">
            About
          </Link>
          <Link href="/privacy" className="text-sm text-gray-500 hover:text-gray-900">
            Privacy
          </Link>
          <Link href="/terms" className="text-sm text-gray-500 hover:text-gray-900">
            Terms
          </Link>
          <Link href="/contact" className="text-sm text-gray-500 hover:text-gray-900">
            Contact
          </Link>
        </div>
      </footer>
    </div>
  );
} 