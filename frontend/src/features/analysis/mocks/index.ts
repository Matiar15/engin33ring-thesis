import { DetectionLog, BoundingBox } from "@/features/analysis/types";

export const TRAFFIC_SIGNS = [
  'Speed Limit 30',
  'Speed Limit 50',
  'Speed Limit 60',
  'Speed Limit 80',
  'Stop Sign',
  'Yield',
  'No Entry',
  'One Way',
  'Pedestrian Crossing',
  'School Zone',
  'No Parking',
  'Turn Right',
  'Turn Left',
  'Roundabout',
  'Highway Exit',
];

export const BOX_COLORS = [
    '#00FF88', // neon green
    '#00FFFF', // cyan
    '#FF00FF', // magenta
    '#FFFF00', // yellow
    '#FF6600', // orange
];

export const generateMockDetection = (): DetectionLog => ({
    id: crypto.randomUUID(),
    timestamp: new Date(),
    signType: TRAFFIC_SIGNS[Math.floor(Math.random() * TRAFFIC_SIGNS.length)],
    confidence: Math.floor(Math.random() * 20) + 80,
});

export const generateMockBoundingBox = (): BoundingBox => {
  const size = 40 + Math.random() * 60;
  return {
    id: crypto.randomUUID(),
    x: Math.random() * 70 + 10,
    y: Math.random() * 60 + 15,
    width: size,
    height: size,
    label: TRAFFIC_SIGNS[Math.floor(Math.random() * TRAFFIC_SIGNS.length)],
    color: BOX_COLORS[Math.floor(Math.random() * BOX_COLORS.length)],
  };
};

