import React from 'react';
import { Search, X, LucideIcon } from 'lucide-react';
import { COLOR } from '../../styles/colors';

// --- BADGE ---
interface BadgeProps {
  children: React.ReactNode;
  color: string;
  bg: string;
  style?: React.CSSProperties;
}

export function Badge({ children, color, bg, style }: BadgeProps) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4, fontSize: 12, fontWeight: 600,
      color, background: bg, padding: "3px 10px", borderRadius: 20, whiteSpace: "nowrap", ...style
    }}>
      {children}
    </span>
  );
}

// --- CARD ---
interface CardProps {
  children: React.ReactNode;
  style?: React.CSSProperties;
  onClick?: () => void;
}

export function Card({ children, style, onClick }: CardProps) {
  return (
    <div
      onClick={onClick}
      style={{
        background: "white", border: `1px solid ${COLOR.borde}`, borderRadius: 10,
        padding: 20, cursor: onClick ? 'pointer' : 'default', ...style
      }}
    >
      {children}
    </div>
  );
}

// --- BUTTON ---
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost' | 'danger';
  icon?: LucideIcon;
  size?: 'sm' | 'md';
}

export function Button({ children, variant = "primary", icon: Icon, onClick, style, size = "md", ...props }: ButtonProps) {
  const variants = {
    primary: { background: COLOR.azul, color: "white", border: "none" },
    secondary: { background: "white", color: COLOR.carbon, border: `1px solid ${COLOR.borde}` },
    accent: { background: COLOR.mostaza, color: COLOR.carbon, border: "none" },
    ghost: { background: "transparent", color: COLOR.azul, border: "none" },
    danger: { background: COLOR.rojoClaro, color: COLOR.rojo, border: "none" },
  };
  const sizes = { sm: "6px 12px", md: "9px 16px" };
  return (
    <button
      onClick={onClick}
      style={{
        display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 6, fontSize: 13.5, fontWeight: 600,
        padding: sizes[size], borderRadius: 8, cursor: "pointer", fontFamily: "inherit",
        transition: "opacity 0.15s", ...variants[variant], ...style
      }}
      onMouseDown={(e) => e.currentTarget.style.opacity = "0.8"}
      onMouseUp={(e) => e.currentTarget.style.opacity = "1"}
      {...props}
    >
      {Icon && <Icon size={15} />}
      {children}
    </button>
  );
}

// --- PAGE HEADER ---
interface PageHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function PageHeader({ title, subtitle, action }: PageHeaderProps) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
      <div>
        <h1 style={{ fontFamily: "Georgia, serif", fontSize: 26, fontWeight: 700, color: COLOR.carbon, margin: 0 }}>{title}</h1>
        {subtitle && <p style={{ fontSize: 14, color: COLOR.carbonSuave, margin: "4px 0 0" }}>{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

// --- SEARCH BAR ---
interface SearchBarProps {
  placeholder: string;
  value: string;
  onChange: (val: string) => void;
}

export function SearchBar({ placeholder, value, onChange }: SearchBarProps) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 8, background: "white",
      border: `1px solid ${COLOR.borde}`, borderRadius: 8, padding: "8px 12px", width: 280
    }}>
      <Search size={15} color={COLOR.carbonSuave} />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{ border: "none", outline: "none", fontSize: 13.5, width: "100%", fontFamily: "inherit", background: "transparent" }}
      />
    </div>
  );
}

// --- MODAL ---
interface ModalProps {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  width?: number;
}

export function Modal({ title, onClose, children, width = 520 }: ModalProps) {
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(54,52,50,0.45)", display: "flex",
      alignItems: "center", justifyContent: "center", zIndex: 100, padding: 20
    }} onClick={onClose}>
      <div onClick={(e) => e.stopPropagation()} style={{
        background: "white", borderRadius: 12, width, maxHeight: "85vh", overflow: "auto",
        boxShadow: "0 12px 40px rgba(0,0,0,0.18)"
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "18px 22px", borderBottom: `1px solid ${COLOR.borde}`
        }}>
          <h3 style={{ fontFamily: "Georgia, serif", fontSize: 18, fontWeight: 700, margin: 0, color: COLOR.carbon }}>{title}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: COLOR.carbonSuave, padding: 4 }}>
            <X size={20} />
          </button>
        </div>
        <div style={{ padding: 22 }}>{children}</div>
      </div>
    </div>
  );
}

// --- FIELD ---
interface FieldProps {
  label: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export function Field({ label, children, style }: FieldProps) {
  return (
    <div style={{ marginBottom: 14, ...style }}>
      <label style={{ display: "block", fontSize: 12.5, fontWeight: 600, color: COLOR.carbonSuave, marginBottom: 5 }}>{label}</label>
      {children}
    </div>
  );
}

// --- INPUTS ---
const inputStyle: React.CSSProperties = {
  width: "100%", padding: "9px 11px", border: `1px solid ${COLOR.borde}`, borderRadius: 7,
  fontSize: 13.5, fontFamily: "inherit", outline: "none", boxSizing: "border-box"
};

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} style={{ ...inputStyle, ...props.style }} />;
}

export function Select({ children, ...props }: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return <select {...props} style={{ ...inputStyle, ...props.style }}>{children}</select>;
}
