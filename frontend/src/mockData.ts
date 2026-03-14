import {generateMockDetection} from "@/features/analysis/mocks";
import {ArchiveEntry} from "@/features/analysis/types";

export const initialArchiveData: ArchiveEntry[] = [
  {
    id: '1',
    thumbnail: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
    date: new Date('2025-01-28T14:30:00'),
    duration: '02:45',
    signsDetected: 12,
    detections: Array.from({ length: 12 }, generateMockDetection),
  },
  {
    id: '2',
    thumbnail: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop',
    date: new Date('2025-01-27T09:15:00'),
    duration: '05:22',
    signsDetected: 28,
    detections: Array.from({ length: 28 }, generateMockDetection),
  },
  {
    id: '3',
    thumbnail: 'https://images.unsplash.com/photo-1476973422084-e0fa66ff9456?w=400&h=300&fit=crop',
    date: new Date('2025-01-25T18:45:00'),
    duration: '01:58',
    signsDetected: 7,
    detections: Array.from({ length: 7 }, generateMockDetection),
  },
];
