import { useRef, useEffect, useCallback } from 'react';
import { BoundingBox } from '@/features/analysis/types';
import * as React from "react";

interface UseBoundingBoxOverlayOptions {
  boxes: BoundingBox[];
  containerRef: React.RefObject<HTMLDivElement | null>;
}

export function useBoundingBoxOverlay({
  boxes,
  containerRef,
}: UseBoundingBoxOverlayOptions) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const drawBox = useCallback((
    ctx: CanvasRenderingContext2D,
    box: BoundingBox,
    canvasWidth: number,
    canvasHeight: number
  ) => {
    const x = (box.x / 100) * canvasWidth;
    const y = (box.y / 100) * canvasHeight;
    const w = (box.width / 100) * canvasWidth;
    const h = (box.height / 100) * canvasHeight;
    const cornerSize = 10;

    // Glow effect
    ctx.shadowColor = box.color;
    ctx.shadowBlur = 15;

    // Box outline
    ctx.strokeStyle = box.color;
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
    ctx.fillStyle = box.color;
    const labelWidth = ctx.measureText(box.label).width + 16;
    ctx.fillRect(x, y - 24, labelWidth, 22);

    // Label text
    ctx.fillStyle = '#000';
    ctx.font = 'bold 12px Rajdhani';
    ctx.fillText(box.label, x + 8, y - 8);
  }, []);

  // Resize canvas when container changes
  useEffect(() => {
    const resizeCanvas = () => {
      if (canvasRef.current && containerRef.current) {
        canvasRef.current.width = containerRef.current.offsetWidth;
        canvasRef.current.height = containerRef.current.offsetHeight;
      }
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    return () => window.removeEventListener('resize', resizeCanvas);
  }, [containerRef]);

  // Draw boxes when they change
  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear and redraw
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    boxes.forEach(box => drawBox(ctx, box, canvas.width, canvas.height));
  }, [boxes, drawBox]);

  return { canvasRef };
}

