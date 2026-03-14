import { useCallback, useState } from 'react';
import * as React from "react";

interface UseFileDropOptions {
  accept?: string;
  onFileSelect: (file: File, url: string) => void;
  validateFile?: (file: File) => string | null;
}

export function useFileDrop({ accept = 'video/*', onFileSelect, validateFile }: UseFileDropOptions) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFileType = useCallback((file: File): boolean => {
    const acceptType = accept.replace('/*', '/');
    if (!file.type.startsWith(acceptType)) {
      setError(`Please upload a valid ${accept.split('/')[0]} file`);
      return false;
    }
    return true;
  }, [accept]);

  const processFile = useCallback((file: File) => {
    setError(null);

    if (!validateFileType(file)) return;
    const customError = validateFile?.(file);
    if (customError) {
      setError(customError);
      return;
    }

    const url = URL.createObjectURL(file);
    onFileSelect(file, url);
  }, [onFileSelect, validateFileType, validateFile]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files?.[0]) {
      processFile(files[0]);
    }
  }, [processFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files?.[0]) {
      processFile(files[0]);
    }
  }, [processFile]);

  const dragProps = {
    onDragEnter: handleDragEnter,
    onDragLeave: handleDragLeave,
    onDragOver: handleDragOver,
    onDrop: handleDrop,
  };

  return {
    isDragging,
    error,
    dragProps,
    handleFileInput,
  };
}
