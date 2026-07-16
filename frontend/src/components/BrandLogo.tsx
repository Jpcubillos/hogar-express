interface BrandLogoProps {
  className?: string;
  alt?: string;
}

export default function BrandLogo({ className = "", alt = "Hogar Express" }: BrandLogoProps) {
  return (
    <img
      className={`brand-logo ${className}`.trim()}
      src="/hogar-express-logo.png"
      alt={alt}
    />
  );
}
