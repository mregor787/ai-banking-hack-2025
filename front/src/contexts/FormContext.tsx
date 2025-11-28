import React, { createContext, useContext, useMemo } from "react";
import { useForm, UseFormReturn, FieldValues } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

interface FormContextValue<T extends FieldValues = any> {
    form: UseFormReturn<T>;
    isLoading?: boolean;
}

const FormContext = createContext<FormContextValue | undefined>(undefined);

interface FormProviderProps<T extends FieldValues> {
    children: React.ReactNode;
    schema?: yup.ObjectSchema<T>;
    defaultValues?: T;
    isLoading?: boolean;
    onSubmit?: (data: T) => void;
}

export function FormProvider<T extends FieldValues>({
    children,
    schema,
    defaultValues,
    isLoading = false,
    onSubmit,
}: FormProviderProps<T>) {
    const form = useForm<T>({
        resolver: schema ? yupResolver(schema) : undefined,
        defaultValues: defaultValues as any,
        mode: "onChange",
    });

    const value = useMemo(
        () => ({
            form,
            isLoading,
        }),
        [form, isLoading]
    );

    return (
        <FormContext.Provider value={value}>
            {onSubmit ? <form onSubmit={form.handleSubmit(onSubmit)}>{children}</form> : children}
        </FormContext.Provider>
    );
}

export function useFormContext() {
    const context = useContext(FormContext);
    if (!context) {
        throw new Error("useFormContext must be used within a FormProvider");
    }
    return context;
}
