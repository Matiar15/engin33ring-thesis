export interface BoundingBox {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  color: string;
}

export interface DetectionLog {
  id: string;
  timestamp: Date;
  signType: string;
  confidence: number;
}

export interface ArchiveEntry {
  id: string;
  thumbnail: string;
  date: Date;
  duration: string;
  signsDetected: number;
  detections: DetectionLog[];
}


