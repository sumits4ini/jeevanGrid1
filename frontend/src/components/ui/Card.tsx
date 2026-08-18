import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: "default" | "surface" | "bordered" | "highlight";
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  variant = "default",
  ...props
}) => {
  const variantStyles = {
    default: "bg-surface-100 border border-surface-border backdrop-blur-sm shadow-sm",
    surface: "bg-surface-200 border border-surface-border",
    bordered: "bg-transparent border border-surface-border",
    highlight: "bg-surface-100 border border-cyan-500/40 shadow-lg shadow-cyan-950/10",
  };

  return (
    <div
      className={cn(
        "rounded-xl p-5 text-foreground transition-all duration-200",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<{
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  badge?: React.ReactNode;
  className?: string;
}> = ({ title, subtitle, action, badge, className }) => (
  <div className={cn("flex items-start justify-between pb-4 border-b border-surface-border mb-4", className)}>
    <div>
      <div className="flex items-center gap-2">
        <h3 className="text-base font-semibold tracking-wide text-foreground">{title}</h3>
        {badge}
      </div>
      {subtitle && <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{subtitle}</p>}
    </div>
    {action && <div className="flex items-center gap-2">{action}</div>}
  </div>
);
