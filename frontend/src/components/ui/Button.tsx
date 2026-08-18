import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost" | "outline";
  size?: "sm" | "md" | "lg";
  icon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "secondary",
  size = "md",
  icon,
  className,
  disabled,
  ...props
}) => {
  const variantStyles = {
    primary: "bg-cyan-600 hover:bg-cyan-500 text-white shadow-md shadow-cyan-950/20 border border-cyan-400/30 font-semibold",
    secondary: "bg-surface-200 hover:bg-surface-50 text-foreground border border-surface-border",
    danger: "bg-rose-600 hover:bg-rose-500 text-white shadow-md shadow-rose-950/20 border border-rose-400/30 font-semibold",
    ghost: "bg-transparent hover:bg-surface-200 text-foreground",
    outline: "bg-transparent hover:bg-surface-200 text-foreground border border-surface-border",
  };

  const sizeStyles = {
    sm: "px-2.5 py-1.5 text-xs rounded-lg gap-1.5",
    md: "px-3.5 py-2 text-sm rounded-lg gap-2",
    lg: "px-5 py-2.5 text-base rounded-xl gap-2.5",
  };

  return (
    <button
      disabled={disabled}
      className={cn(
        "inline-flex items-center justify-center font-medium transition-all duration-150 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none disabled:active:scale-100",
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      {children}
    </button>
  );
};
