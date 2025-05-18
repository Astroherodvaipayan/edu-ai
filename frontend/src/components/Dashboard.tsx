'use client';

import { useAuth } from '@/contexts/AuthContext';
import StudentDashboard from './StudentDashboard';

export default function Dashboard() {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return <StudentDashboard userId={user.id} />;
} 