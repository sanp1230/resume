import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Navbar } from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
  },
  exit: {
    opacity: 0,
    y: -20,
  },
};

export const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <AnimatePresence mode="wait">
        <motion.main
          className="pt-16" // Space for fixed navbar
          variants={pageVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.main>
      </AnimatePresence>
      
      <footer className="mt-auto py-8 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">© 2024 Rezoomé</span>
              <span className="text-gray-300">|</span>
              <a href="/about" className="text-sm text-gray-500 hover:text-gray-900">
                About
              </a>
              <a href="/privacy" className="text-sm text-gray-500 hover:text-gray-900">
                Privacy
              </a>
              <a href="/terms" className="text-sm text-gray-500 hover:text-gray-900">
                Terms
              </a>
            </div>
            <div className="flex items-center space-x-4">
              <a href="/contact" className="text-sm text-gray-500 hover:text-gray-900">
                Contact
              </a>
              <span className="text-sm text-gray-500">
                Made with ❤️ for job seekers
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}; 