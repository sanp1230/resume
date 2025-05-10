import React from 'react';
import { motion } from 'framer-motion';
import { cva, type VariantProps } from 'class-variance-authority';

const cardVariants = cva(
  'rounded-2xl bg-white transition-all duration-200',
  {
    variants: {
      variant: {
        default: 'shadow-sm hover:shadow-md',
        outline: 'border border-gray-200 hover:border-gray-300',
        ghost: 'bg-gray-50 hover:bg-gray-100',
        glow: 'shadow-lg hover:shadow-xl hover:shadow-red-500/10',
      },
      padding: {
        none: '',
        sm: 'p-4',
        md: 'p-6',
        lg: 'p-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      padding: 'md',
    },
  }
);

interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  animate?: boolean;
  delay?: number;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, padding, animate = true, delay = 0, children, ...props }, ref) => {
    const Component = animate ? motion.div : 'div';

    const animationProps = animate
      ? {
          initial: { opacity: 0, y: 20 },
          animate: { opacity: 1, y: 0 },
          transition: { duration: 0.5, delay },
        }
      : {};

    return (
      <Component
        ref={ref}
        className={cardVariants({ variant, padding, className })}
        {...animationProps}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Card.displayName = 'Card'; 