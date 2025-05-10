import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { LucideIcon } from 'lucide-react';

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  href: string;
  buttonText: string;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({
  icon: Icon,
  title,
  description,
  href,
  buttonText,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className="bg-white rounded-[32px] p-8 shadow-[0_4px_24px_-1px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_32px_-1px_rgba(0,0,0,0.08)] transition-all duration-300"
    >
      <div className="flex flex-col h-full">
        <div className="flex items-start space-x-6">
          <div className="flex-shrink-0">
            <Icon className="h-8 w-8 text-gray-900" strokeWidth={1.5} />
          </div>
          <div>
            <h3 className="text-[22px] font-semibold text-gray-900 mb-2">
              {title}
            </h3>
            <p className="text-base leading-relaxed text-gray-600">
              {description}
            </p>
          </div>
        </div>
        <div className="mt-8">
          <Link
            href={href}
            className="group inline-flex items-center text-base font-medium text-gray-900"
          >
            {buttonText}
            <svg
              className="ml-2.5 h-4 w-4 transition-transform duration-300 group-hover:translate-x-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </Link>
        </div>
      </div>
    </motion.div>
  );
}; 