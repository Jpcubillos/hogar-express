import React, { useEffect } from 'react';
import { Search, X, type LucideIcon } from 'lucide-react';

interface BadgeProps {
  children: React.ReactNode;
  color: string;
  bg: string;
  style?: React.CSSProperties;
  className?: string;
}

export function Badge({ children, color, bg, style, className = "" }: BadgeProps) {
  return (
    <span className={`ui-badge ${className}`.trim()} style={{ color, background: bg, ...style }}>
      <span className="ui-badge__dot" style={{ background: color }} />
      {children}
    </span>
  );
}

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  onClick?: () => void;
}

export function Card({ children, className = "", onClick, ...props }: CardProps) {
  return (
    <div
      className={`ui-card ${onClick ? 'ui-card--interactive' : ''} ${className}`.trim()}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (event) => {
        if (event.key === 'Enter' || event.key === ' ') onClick();
      } : undefined}
      {...props}
    >
      {children}
    </div>
  );
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost' | 'danger';
  icon?: LucideIcon;
  size?: 'sm' | 'md';
}

export function Button({ children, variant = "primary", icon: Icon, className = "", size = "md", type = "button", ...props }: ButtonProps) {
  return (
    <button
      type={type}
      className={`ui-button ui-button--${variant} ui-button--${size} ${className}`.trim()}
      {...props}
    >
      {Icon && <Icon size={size === 'sm' ? 15 : 17} strokeWidth={2.2} aria-hidden="true" />}
      <span>{children}</span>
    </button>
  );
}

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  eyebrow?: string;
  action?: React.ReactNode;
}

export function PageHeader({ title, subtitle, eyebrow, action }: PageHeaderProps) {
  return (
    <header className="page-header">
      <div className="page-header__copy">
        {eyebrow && <span className="page-header__eyebrow">{eyebrow}</span>}
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {action && <div className="page-header__actions">{action}</div>}
    </header>
  );
}

interface SearchBarProps {
  placeholder: string;
  value: string;
  onChange: (val: string) => void;
  className?: string;
}

export function SearchBar({ placeholder, value, onChange, className = "" }: SearchBarProps) {
  return (
    <label className={`ui-search ${className}`.trim()}>
      <Search size={17} aria-hidden="true" />
      <input value={value} onChange={(event) => onChange(event.target.value)} placeholder={placeholder} />
      {value && (
        <button type="button" onClick={() => onChange("")} aria-label="Limpiar búsqueda">
          <X size={15} />
        </button>
      )}
    </label>
  );
}

interface ModalProps {
  title: string;
  subtitle?: string;
  onClose: () => void;
  children: React.ReactNode;
  width?: number;
}

export function Modal({ title, subtitle, onClose, children, width = 560 }: ModalProps) {
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => event.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [onClose]);

  return (
    <div className="ui-modal-backdrop" onMouseDown={onClose}>
      <section
        className="ui-modal"
        style={{ '--modal-width': `${width}px` } as React.CSSProperties}
        onMouseDown={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <header className="ui-modal__header">
          <div>
            <h2 id="modal-title">{title}</h2>
            {subtitle && <p>{subtitle}</p>}
          </div>
          <button type="button" onClick={onClose} className="icon-button" aria-label="Cerrar ventana">
            <X size={19} />
          </button>
        </header>
        <div className="ui-modal__body">{children}</div>
      </section>
    </div>
  );
}

interface FieldProps {
  label: string;
  hint?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export function Field({ label, hint, children, style }: FieldProps) {
  return (
    <label className="ui-field" style={style}>
      <span className="ui-field__label">{label}</span>
      {children}
      {hint && <span className="ui-field__hint">{hint}</span>}
    </label>
  );
}

export function Input({ className = "", ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input className={`ui-input ${className}`.trim()} {...props} />;
}

export function Select({ children, className = "", ...props }: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return <select className={`ui-input ui-select ${className}`.trim()} {...props}>{children}</select>;
}

interface SectionTitleProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function SectionTitle({ title, description, action }: SectionTitleProps) {
  return (
    <div className="section-title">
      <div>
        <h2>{title}</h2>
        {description && <p>{description}</p>}
      </div>
      {action}
    </div>
  );
}
