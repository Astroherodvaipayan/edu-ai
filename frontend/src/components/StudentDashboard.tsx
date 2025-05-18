'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import LearningProfile from './LearningProfile';
import KnowledgeState from './KnowledgeState';

interface StudentDashboardProps {
  userId: string;
}

export default function StudentDashboard({ userId }: StudentDashboardProps) {
  const [profile, setProfile] = useState(null);
  const [knowledgeState, setKnowledgeState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    async function fetchStudentData() {
      if (!userId) return;
      
      try {
        const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${backendUrl}/api/student/profile/${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch student profile');
        }
        
        const data = await response.json();
        if (data.success) {
          setProfile(data.profile);
          setKnowledgeState(data.knowledge_state);
        } else {
          setError(data.error);
        }
      } catch (err: any) {
        setError(err.message || 'An error occurred');
      } finally {
        setLoading(false);
      }
    }

    fetchStudentData();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-emerald-800 mb-8">Learning Profile</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {profile && (
          <div className="col-span-1">
            <LearningProfile profile={profile} />
          </div>
        )}
        
        {knowledgeState && (
          <div className="col-span-1">
            <KnowledgeState knowledgeState={knowledgeState} />
          </div>
        )}
      </div>
    </div>
  );
} 