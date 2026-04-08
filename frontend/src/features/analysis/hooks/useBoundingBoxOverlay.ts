import { useRef, useEffect, useCallback, useState } from 'react';
import { BoundingBox } from '@/features/analysis/types';
import * as React from "react";

interface UseBoundingBoxOverlayOptions {
  boxes: BoundingBox[];
  containerRef: React.RefObject<HTMLDivElement | null>;
  isPaused?: boolean;
}

export function useBoundingBoxOverlay({
  boxes,
  containerRef,
  isPaused = false,
}: UseBoundingBoxOverlayOptions) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 });

  const drawBox = useCallback((
    ctx: CanvasRenderingContext2D,
    box: BoundingBox,
    canvasWidth: number,
    canvasHeight: number
  ) => {
    const color = isPaused ? '#888888' : box.color;

    const x = (box.x / 100) * canvasWidth;
    const y = (box.y / 100) * canvasHeight;
    const w = (box.width / 100) * canvasWidth;
    const h = (box.height / 100) * canvasHeight;
    const cornerSize = 10;

    // Glow effect
    ctx.shadowColor = color;
    ctx.shadowBlur = isPaused ? 0 : 15;

    // Box outline
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, w, h);

    // Corner accents
    ctx.lineWidth = 3;

    // Top-left
    ctx.beginPath();
    ctx.moveTo(x, y + cornerSize);
    ctx.lineTo(x, y);
    ctx.lineTo(x + cornerSize, y);
    ctx.stroke();

    // Top-right
    ctx.beginPath();
    ctx.moveTo(x + w - cornerSize, y);
    ctx.lineTo(x + w, y);
    ctx.lineTo(x + w, y + cornerSize);
    ctx.stroke();

    // Bottom-left
    ctx.beginPath();
    ctx.moveTo(x, y + h - cornerSize);
    ctx.lineTo(x, y + h);
    ctx.lineTo(x + cornerSize, y + h);
    ctx.stroke();

    // Bottom-right
    ctx.beginPath();
    ctx.moveTo(x + w - cornerSize, y + h);
    ctx.lineTo(x + w, y + h);
    ctx.lineTo(x + w, y + h - cornerSize);
    ctx.stroke();

    // Label background
    ctx.shadowBlur = 0;
    ctx.fillStyle = color;
    const labelWidth = ctx.measureText(box.label).width + 16;
    ctx.fillRect(x, y - 24, labelWidth, 22);

    // Label text
    ctx.fillStyle = isPaused ? '#ffffff' : '#000';
    ctx.font = 'bold 12px Rajdhani';
    ctx.fillText(box.label, x + 8, y - 8);
  }, [isPaused]);

  // Resize canvas when container changes
  useEffect(() => {
    const resizeCanvas = () => {
      if (canvasRef.current && containerRef.current) {
        const w = containerRef.current.offsetWidth;
        const h = containerRef.current.offsetHeight;
        canvasRef.current.width = w;
        canvasRef.current.height = h;
        setCanvasSize({ width: w, height: h });
      }
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    return () => window.removeEventListener('resize', resizeCanvas);
  }, [containerRef]);

  // Draw boxes when they change or canvas is resized
  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear and redraw
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    boxes.forEach(box => drawBox(ctx, box, canvas.width, canvas.height));
  }, [boxes, drawBox, canvasSize, isPaused]);

  return { canvasRef };
}
