import type { ButtonHTMLAttributes } from 'react';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary';
};

export default function Button({ className = '', variant = 'primary', ...props }: Props) {
  const styles =
    variant === 'primary'
      ? 'bg-brand-500 text-white hover:bg-brand-700'
      : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50';

  return <button className={`rounded-xl px-4 py-2 font-medium transition ${styles} ${className}`} {...props} />;
}
