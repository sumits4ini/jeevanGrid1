import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "critical" | "warning" | "success" | "info" | "outline" | "brand";
  size?: "sm" | "md";
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  size = "sm",
  dot = false,
  className,
  ...props
}) => {
  const variantStyles = {
    default: "bg-slate-800 text-slate-300 border-slate-700",
    critical: "bg-rose-500/10 text-rose-400 border-rose-500/30",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    info: "bg-sky-500/10 text-sky-400 border-sky-500/30",
    brand: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
    outline: "bg-transparent text-slate-400 border-slate-700",
  };

  const dotColors = {
    default: "bg-slate-400",
    critical: "bg-rose-500",
    warning: "bg-amber-500",
    success: "bg-emerald-500",
    info: "bg-sky-500",
    brand: "bg-cyan-400",
    outline: "bg-slate-500",
  };

  const sizeStyles = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-2.5 py-1 text-xs font-medium",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 font-medium rounded-full border tracking-wide",
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {dot && <span className={cn("w-1.5 h-1.5 rounded-full animate-pulse", dotColors[variant])} />}
      {children}
    </span>
  );
};
