import React, { forwardRef } from "react";
import type { FieldError } from "react-hook-form";

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: FieldError | undefined;
  helperText?: string;
}

export const FormInput = forwardRef<HTMLInputElement, FormInputProps>(
  ({ label, error, helperText, className = "", id, ...props }, ref) => {
    const inputId = id || props.name;

    return (
      <div className="space-y-1">
        <label
          htmlFor={inputId}
          className="block text-xs font-semibold text-slate-700"
        >
          {label} {props.required && <span className="text-rose-500">*</span>}
        </label>
        <input
          id={inputId}
          ref={ref}
          className={`w-full px-3.5 py-2 text-sm bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 transition-all disabled:bg-slate-100 disabled:text-slate-400 ${
            error
              ? "border-rose-400 focus:ring-rose-200 focus:border-rose-500"
              : "border-slate-200 focus:ring-indigo-200 focus:border-indigo-500"
          } ${className}`}
          {...props}
        />
        {error ? (
          <p className="text-xs text-rose-500 font-medium">{error.message}</p>
        ) : helperText ? (
          <p className="text-xs text-slate-400">{helperText}</p>
        ) : null}
      </div>
    );
  },
);

FormInput.displayName = "FormInput";
