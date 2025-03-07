/**
 * Day 61: Building a Modular Button Component System with TypeScript
 * 
 * This file demonstrates how to build a comprehensive, accessible button 
 * component system with TypeScript, React, and modern best practices.
 * 
 * Features:
 * - Strict TypeScript typing
 * - Compound component pattern
 * - Accessibility built-in
 * - Tailwind CSS integration
 * - Comprehensive prop validation
 * - Animation support
 * - Loading states
 * - Icon support
 * - Test cases
 */

import React, { 
    ButtonHTMLAttributes, 
    forwardRef, 
    ReactNode, 
    createContext, 
    useContext, 
    useState,
    useEffect,
    useMemo
  } from 'react';
  import { cva, type VariantProps } from 'class-variance-authority';
  import { twMerge } from 'tailwind-merge';
  import { Slot } from '@radix-ui/react-slot';
  
  // ============================================================================
  // Utility Types
  // ============================================================================
  
  type OmitCommonProps<Target, OmitAdditionalProps extends keyof any = never> = Omit<
    Target,
    'as' | 'className' | OmitAdditionalProps
  >;
  
  type PolymorphicComponentProp<
    C extends React.ElementType,
    Props = {}
  > = {
    as?: C;
  } & Props;
  
  type PolymorphicRef<C extends React.ElementType> = React.ComponentPropsWithRef<C>['ref'];
  
  type PolymorphicComponentPropWithRef<
    C extends React.ElementType,
    Props = {}
  > = PolymorphicComponentProp<C, Props> & { ref?: PolymorphicRef<C> };
  
  // ============================================================================
  // Button Variants using class-variance-authority
  // ============================================================================
  
  const buttonVariants = cva(
    [
      'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
      'disabled:opacity-50 disabled:pointer-events-none',
      'ring-offset-background',
    ],
    {
      variants: {
        variant: {
          primary: [
            'bg-primary text-primary-foreground hover:bg-primary/90',
            'focus-visible:ring-primary',
          ],
          secondary: [
            'bg-secondary text-secondary-foreground hover:bg-secondary/90',
            'focus-visible:ring-secondary',
          ],
          outline: [
            'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
            'focus-visible:ring-accent',
          ],
          ghost: [
            'hover:bg-accent hover:text-accent-foreground',
            'focus-visible:ring-accent',
          ],
          link: [
            'text-primary underline-offset-4 hover:underline',
            'focus-visible:ring-primary',
          ],
          danger: [
            'bg-destructive text-destructive-foreground hover:bg-destructive/90',
            'focus-visible:ring-destructive',
          ],
          success: [
            'bg-success text-success-foreground hover:bg-success/90',
            'focus-visible:ring-success',
          ],
        },
        size: {
          xs: 'h-7 px-2 text-xs',
          sm: 'h-9 px-3',
          md: 'h-10 px-4',
          lg: 'h-11 px-6',
          xl: 'h-12 px-8',
          icon: 'h-10 w-10',
        },
        fullWidth: {
          true: 'w-full',
        },
        rounded: {
          none: 'rounded-none',
          sm: 'rounded-sm',
          md: 'rounded-md',
          lg: 'rounded-lg',
          full: 'rounded-full',
        },
      },
      defaultVariants: {
        variant: 'primary',
        size: 'md',
        rounded: 'md',
      },
    }
  );
  
  // ============================================================================
  // Button Context
  // ============================================================================
  
  interface ButtonContextValue {
    isLoading: boolean;
    isDisabled: boolean;
    size: NonNullable<ButtonVariantProps['size']>;
    variant: NonNullable<ButtonVariantProps['variant']>;
  }
  
  const ButtonContext = createContext<ButtonContextValue | undefined>(undefined);
  
  const useButtonContext = () => {
    const context = useContext(ButtonContext);
    if (!context) {
      throw new Error('Button compound components must be used within a Button component');
    }
    return context;
  };
  
  // ============================================================================
  // Button Component Types
  // ============================================================================
  
  type ButtonVariantProps = VariantProps<typeof buttonVariants>;
  
  export interface ButtonProps extends 
    OmitCommonProps<ButtonHTMLAttributes<HTMLButtonElement>>,
    ButtonVariantProps {
    /** Custom class names to apply to the button */
    className?: string;
    /** Content to render inside the button */
    children?: ReactNode;
    /** If true, the button will be disabled and show a loading spinner */
    isLoading?: boolean;
    /** If true, the button will take up the full width of its container */
    fullWidth?: boolean;
    /** Indicates if the button should render as a child component */
    asChild?: boolean;
    /** Optional click handler */
    onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
    /** Optional right side content like an icon */
    rightIcon?: ReactNode;
    /** Optional left side content like an icon */
    leftIcon?: ReactNode;
    /** Animation preset for the button */
    animation?: 'none' | 'pulse' | 'bounce';
    /** Optional tooltip text */
    tooltip?: string;
    /** Data test id for testing */
    'data-testid'?: string;
  }
  
  // ============================================================================
  // Main Button Component
  // ============================================================================
  
  export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    (
      {
        className,
        variant = 'primary',
        size = 'md',
        rounded = 'md',
        fullWidth = false,
        isLoading = false,
        asChild = false,
        animation = 'none',
        tooltip,
        'data-testid': testId,
        disabled,
        children,
        rightIcon,
        leftIcon,
        ...props
      },
      ref
    ) => {
      const Comp = asChild ? Slot : 'button';
      const isDisabled = disabled || isLoading;
      
      // Animation classes based on the animation prop
      const animationClasses = useMemo(() => {
        switch (animation) {
          case 'pulse':
            return 'hover:animate-pulse';
          case 'bounce':
            return 'hover:animate-bounce';
          default:
            return '';
        }
      }, [animation]);
  
      // Combine all classes
      const buttonClasses = twMerge(
        buttonVariants({ 
          variant, 
          size, 
          fullWidth, 
          rounded
        }),
        animationClasses,
        className
      );
  
      // Context value for compound components
      const contextValue = useMemo(() => ({
        isLoading,
        isDisabled: !!isDisabled,
        size,
        variant,
      }), [isLoading, isDisabled, size, variant]);
  
      return (
        <ButtonContext.Provider value={contextValue}>
          <Comp
            className={buttonClasses}
            ref={ref}
            disabled={isDisabled}
            data-testid={testId}
            title={tooltip}
            {...props}
          >
            {isLoading && <ButtonSpinner className="mr-2" />}
            {!isLoading && leftIcon && (
              <span className="mr-2 inline-flex">{leftIcon}</span>
            )}
            {children}
            {!isLoading && rightIcon && (
              <span className="ml-2 inline-flex">{rightIcon}</span>
            )}
          </Comp>
        </ButtonContext.Provider>
      );
    }
  );
  
  Button.displayName = 'Button';
  
  // ============================================================================
  // Button Spinner Component
  // ============================================================================
  
  interface ButtonSpinnerProps {
    className?: string;
  }
  
  const ButtonSpinner = ({ className }: ButtonSpinnerProps) => {
    const { size } = useButtonContext();
    
    // Size mapping for the spinner
    const spinnerSize = useMemo(() => {
      switch (size) {
        case 'xs': return 'w-3 h-3';
        case 'sm': return 'w-4 h-4';
        case 'md': return 'w-5 h-5';
        case 'lg': return 'w-6 h-6';
        case 'xl': return 'w-7 h-7';
        default: return 'w-5 h-5';
      }
    }, [size]);
  
    return (
      <div className={twMerge('animate-spin', spinnerSize, className)} aria-hidden="true">
        <svg 
          className="w-full h-full" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle 
            className="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            strokeWidth="4"
          />
          <path 
            className="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </div>
    );
  };
  
  ButtonSpinner.displayName = 'ButtonSpinner';
  
  // ============================================================================
  // Button Icon Component
  // ============================================================================
  
  interface ButtonIconProps {
    children: ReactNode;
    position?: 'left' | 'right';
    className?: string;
  }
  
  export const ButtonIcon = ({ 
    children, 
    position = 'left',
    className,
  }: ButtonIconProps) => {
    const { isLoading } = useButtonContext();
    
    if (isLoading) return null;
    
    const positionClasses = position === 'left' ? 'mr-2' : 'ml-2';
    
    return (
      <span className={twMerge('inline-flex items-center', positionClasses, className)}>
        {children}
      </span>
    );
  };
  
  ButtonIcon.displayName = 'ButtonIcon';
  
  // ============================================================================
  // Button Text Component
  // ============================================================================
  
  interface ButtonTextProps {
    children: ReactNode;
    className?: string;
  }
  
  export const ButtonText = ({ children, className }: ButtonTextProps) => {
    return (
      <span className={twMerge('flex-grow', className)}>
        {children}
      </span>
    );
  };
  
  ButtonText.displayName = 'ButtonText';
  
  // ============================================================================
  // Button Group Component
  // ============================================================================
  
  interface ButtonGroupProps {
    children: ReactNode;
    orientation?: 'horizontal' | 'vertical';
    spacing?: 'none' | 'sm' | 'md' | 'lg';
    className?: string;
  }
  
  export const ButtonGroup = ({
    children,
    orientation = 'horizontal',
    spacing = 'md',
    className,
  }: ButtonGroupProps) => {
    // Determine classes based on orientation and spacing
    const orientationClasses = orientation === 'horizontal' 
      ? 'flex flex-row' 
      : 'flex flex-col';
    
    const spacingClasses = useMemo(() => {
      if (spacing === 'none') return '';
      
      const gap = {
        sm: orientation === 'horizontal' ? 'gap-x-2' : 'gap-y-2',
        md: orientation === 'horizontal' ? 'gap-x-4' : 'gap-y-4',
        lg: orientation === 'horizontal' ? 'gap-x-6' : 'gap-y-6',
      }[spacing];
      
      return gap;
    }, [orientation, spacing]);
  
    return (
      <div 
        className={twMerge(
          orientationClasses, 
          spacingClasses, 
          'items-center',
          className
        )}
        role="group"
      >
        {children}
      </div>
    );
  };
  
  ButtonGroup.displayName = 'ButtonGroup';
  
  // ============================================================================
  // Usage Examples
  // ============================================================================
  
  export const BasicUsageExample = () => {
    return (
      <div className="space-y-4 p-6">
        <h2 className="text-xl font-bold">Button Variants</h2>
        <div className="flex gap-4 flex-wrap">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
          <Button variant="danger">Danger</Button>
          <Button variant="success">Success</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button Sizes</h2>
        <div className="flex gap-4 items-center flex-wrap">
          <Button size="xs">Extra Small</Button>
          <Button size="sm">Small</Button>
          <Button size="md">Medium</Button>
          <Button size="lg">Large</Button>
          <Button size="xl">Extra Large</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button States</h2>
        <div className="flex gap-4 flex-wrap">
          <Button isLoading>Loading</Button>
          <Button disabled>Disabled</Button>
          <Button fullWidth>Full Width</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button with Icons</h2>
        <div className="flex gap-4 flex-wrap">
          <Button 
            leftIcon={
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
              </svg>
            }
          >
            Add Item
          </Button>
          <Button 
            rightIcon={
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            }
          >
            Continue
          </Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button Animations</h2>
        <div className="flex gap-4 flex-wrap">
          <Button animation="pulse">Pulse</Button>
          <Button animation="bounce">Bounce</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button Rounded Variants</h2>
        <div className="flex gap-4 flex-wrap">
          <Button rounded="none">Square</Button>
          <Button rounded="sm">Slightly Rounded</Button>
          <Button rounded="md">Medium Rounded</Button>
          <Button rounded="lg">Large Rounded</Button>
          <Button rounded="full">Fully Rounded</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button with Tooltip</h2>
        <div className="flex gap-4 flex-wrap">
          <Button tooltip="This is a helpful tooltip">Hover Me</Button>
        </div>
  
        <h2 className="text-xl font-bold mt-6">Button Group</h2>
        <ButtonGroup>
          <Button variant="outline">Previous</Button>
          <Button>Save</Button>
          <Button variant="outline">Next</Button>
        </ButtonGroup>
  
        <h2 className="text-xl font-bold mt-6">Compound Component Pattern</h2>
        <Button>
          <ButtonIcon position="left">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
            </svg>
          </ButtonIcon>
          <ButtonText>Bookmark</ButtonText>
        </Button>
      </div>
    );
  };
  
  // ============================================================================
  // Storybook Stories
  // ============================================================================
  
  /**
   * This would normally be in a separate file, but for the purpose of this
   * exercise, we're including it in the same file.
   * 
   * In a real project, you would create a Button.stories.tsx file.
   */
  
  // Storybook metadata
  export default {
    title: 'Components/Button',
    component: Button,
    argTypes: {
      variant: {
        control: 'select',
        options: ['primary', 'secondary', 'outline', 'ghost', 'link', 'danger', 'success'],
        defaultValue: 'primary',
      },
      size: {
        control: 'select',
        options: ['xs', 'sm', 'md', 'lg', 'xl', 'icon'],
        defaultValue: 'md',
      },
      rounded: {
        control: 'select',
        options: ['none', 'sm', 'md', 'lg', 'full'],
        defaultValue: 'md',
      },
      isLoading: {
        control: 'boolean',
        defaultValue: false,
      },
      disabled: {
        control: 'boolean',
        defaultValue: false,
      },
      fullWidth: {
        control: 'boolean',
        defaultValue: false,
      },
      animation: {
        control: 'select',
        options: ['none', 'pulse', 'bounce'],
        defaultValue: 'none',
      },
    },
  };
  
  // Basic story
  export const Basic = (args: ButtonProps) => (
    <Button {...args}>Button</Button>
  );
  
  // With icon story
  export const WithIcon = (args: ButtonProps) => (
    <Button 
      {...args}
      leftIcon={
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
        </svg>
      }
    >
      With Icon
    </Button>
  );
  
  // Loading state story
  export const Loading = (args: ButtonProps) => (
    <Button {...args} isLoading>Loading</Button>
  );
  
  // Button group story
  export const GroupedButtons = (args: ButtonProps) => (
    <ButtonGroup>
      <Button {...args} variant="outline">Previous</Button>
      <Button {...args}>Save</Button>
      <Button {...args} variant="outline">Next</Button>
    </ButtonGroup>
  );
  
  // ============================================================================
  // Unit Tests
  // ============================================================================
  
  /**
   * This would normally be in a separate file, but for the purpose of this
   * exercise, we're including it in the same file.
   * 
   * In a real project, you would create a Button.test.tsx file.
   */
  
  /*
  import { render, screen, fireEvent } from '@testing-library/react';
  import { Button, ButtonGroup, ButtonIcon, ButtonText } from './Button';
  
  describe('Button Component', () => {
    test('renders correctly', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
    });
  
    test('calls onClick when clicked', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Click me</Button>);
      fireEvent.click(screen.getByRole('button', { name: /click me/i }));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
  
    test('is disabled when isLoading is true', () => {
      render(<Button isLoading>Click me</Button>);
      expect(screen.getByRole('button', { name: /click me/i })).toBeDisabled();
    });
  
    test('shows spinner when isLoading is true', () => {
      render(<Button isLoading>Click me</Button>);
      expect(screen.getByRole('button', { name: /click me/i })).toContainElement(
        screen.getByRole('status')
      );
    });
  
    test('applies the correct classes for variants', () => {
      const { rerender } = render(<Button variant="primary">Primary</Button>);
      expect(screen.getByRole('button')).toHaveClass('bg-primary');
  
      rerender(<Button variant="secondary">Secondary</Button>);
      expect(screen.getByRole('button')).toHaveClass('bg-secondary');
    });
  
    test('renders with icons', () => {
      render(
        <Button 
          leftIcon={<span data-testid="left-icon" />}
          rightIcon={<span data-testid="right-icon" />}
        >
          With Icons
        </Button>
      );
      expect(screen.getByTestId('left-icon')).toBeInTheDocument();
      expect(screen.getByTestId('right-icon')).toBeInTheDocument();
    });
  
    test('renders full width when fullWidth is true', () => {
      render(<Button fullWidth>Full Width</Button>);
      expect(screen.getByRole('button')).toHaveClass('w-full');
    });
  
    test('button group renders children correctly', () => {
      render(
        <ButtonGroup>
          <Button data-testid="button-1">Button 1</Button>
          <Button data-testid="button-2">Button 2</Button>
        </ButtonGroup>
      );
      expect(screen.getByTestId('button-1')).toBeInTheDocument();
      expect(screen.getByTestId('button-2')).toBeInTheDocument();
    });
  
    test('compound component pattern works correctly', () => {
      render(
        <Button>
          <ButtonIcon position="left">
            <span data-testid="icon" />
          </ButtonIcon>
          <ButtonText>Compound</ButtonText>
        </Button>
      );
      expect(screen.getByTestId('icon')).toBeInTheDocument();
      expect(screen.getByText('Compound')).toBeInTheDocument();
    });
  });
  */
  
  // ============================================================================
  // Custom Hook for Button Behavior
  // ============================================================================
  
  interface UseButtonProps {
    onClick?: () => void;
    disabled?: boolean;
    loading?: boolean;
    debounce?: number;
  }
  
  export function useButton({
    onClick,
    disabled = false,
    loading = false,
    debounce = 0,
  }: UseButtonProps = {}) {
    const [isLoading, setIsLoading] = useState(loading);
    const [isDebouncing, setIsDebouncing] = useState(false);
  
    // Update loading state when the loading prop changes
    useEffect(() => {
      setIsLoading(loading);
    }, [loading]);
  
    const handleClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
      if (disabled || isLoading || isDebouncing) return;
  
      if (debounce > 0) {
        setIsDebouncing(true);
        setTimeout(() => {
          setIsDebouncing(false);
        }, debounce);
      }
  
      if (onClick) {
        try {
          const result = onClick();
          
          // If the onClick returns a promise, handle loading state
          if (result instanceof Promise) {
            setIsLoading(true);
            await result;
            setIsLoading(false);
          }
        } catch (error) {
          setIsLoading(false);
          console.error('Button click handler error:', error);
        }
      }
    };
  
    return {
      isLoading: isLoading || loading,
      isDisabled: disabled || isLoading || isDebouncing,
      handleClick,
    };
  }
  
  // ============================================================================
  // Exports
  // ============================================================================
  
  // Re-export everything as a component object
  export const ButtonComponents = {
    Button,
    ButtonIcon,
    ButtonText,
    ButtonGroup,
    useButton
  };
  
  export default Button;