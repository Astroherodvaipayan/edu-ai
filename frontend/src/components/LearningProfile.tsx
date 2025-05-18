'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

interface LearningStyleProfile {
  perceptual_mode: {
    visual: number;
    auditory: number;
    reading_writing: number;
    kinesthetic: number;
  };
  cognitive_style: {
    global: number;
    analytical: number;
  };
  social_preference: {
    independent: number;
    collaborative: number;
  };
  instruction_style: {
    direct: number;
    constructivist: number;
    inquiry_based: number;
    project_based: number;
  };
  assessment_preference: {
    formative: number;
    summative: number;
    performance: number;
  };
  cognitive_metrics: {
    beginner_level: number;
    intermediate_level: number;
    advanced_level: number;
    total_quizzes_taken: number;
    quiz_scores: number[];
    concept_detective_scores: number[];
    overall_progress: number;
  };
  behavioral_metrics: {
    average_time_per_quiz: number;
    average_time_per_concept: number;
    total_learning_time: number;
    session_completion_rate: number;
    engagement_score: number;
  };
  last_updated: string;
}

interface Props {
  profile: LearningStyleProfile;
}

export default function LearningProfile({ profile }: Props) {
  // Transform data for charts
  const perceptualData = Object.entries(profile?.perceptual_mode || {}).map(([name, value]) => ({
    name: name.replace('_', ' ').toUpperCase(),
    value: value * 100
  }));

  const cognitiveData = Object.entries(profile?.cognitive_style || {}).map(([name, value]) => ({
    name: name.toUpperCase(),
    value: value * 100
  }));

  const socialData = Object.entries(profile?.social_preference || {}).map(([name, value]) => ({
    name: name.toUpperCase(),
    value: value * 100
  }));

  const instructionData = Object.entries(profile?.instruction_style || {}).map(([name, value]) => ({
    name: name.replace('_', ' ').toUpperCase(),
    value: value * 100
  }));

  const assessmentData = Object.entries(profile?.assessment_preference || {}).map(([name, value]) => ({
    name: name.toUpperCase(),
    value: value * 100
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Learning Style Profile</h2>
      
      {/* Cognitive Metrics Section */}
      <div className="space-y-4 mb-8">
        <h3 className="text-lg font-semibold text-gray-700">Cognitive Metrics</h3>
        <div className="space-y-4">
          {/* Overall Progress */}
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Overall Progress</span>
              <span className="text-sm font-medium text-gray-700">{Math.round((profile?.cognitive_metrics?.overall_progress || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className="bg-emerald-600 h-2.5 rounded-full transition-all duration-500" 
                style={{ width: `${(profile?.cognitive_metrics?.overall_progress || 0) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Level-specific Progress */}
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Beginner Level</span>
              <span className="text-sm font-medium text-gray-700">{Math.round((profile?.cognitive_metrics?.beginner_level || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-400 h-2 rounded-full transition-all duration-500" 
                style={{ width: `${(profile?.cognitive_metrics?.beginner_level || 0) * 100}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Intermediate Level</span>
              <span className="text-sm font-medium text-gray-700">{Math.round((profile?.cognitive_metrics?.intermediate_level || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
                style={{ width: `${(profile?.cognitive_metrics?.intermediate_level || 0) * 100}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Advanced Level</span>
              <span className="text-sm font-medium text-gray-700">{Math.round((profile?.cognitive_metrics?.advanced_level || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-800 h-2 rounded-full transition-all duration-500" 
                style={{ width: `${(profile?.cognitive_metrics?.advanced_level || 0) * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="text-sm text-gray-600">
            Total Quizzes Taken: {profile?.cognitive_metrics?.total_quizzes_taken || 0}
          </div>
        </div>
      </div>

      {/* Behavioral Metrics Section */}
      <div className="space-y-4 mb-8">
        <h3 className="text-lg font-semibold text-gray-700">Behavioral Metrics</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">Session Completion Rate</span>
              <span className="text-sm font-medium text-gray-700">{Math.round((profile?.behavioral_metrics?.session_completion_rate || 0) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className="bg-purple-600 h-2.5 rounded-full transition-all duration-500" 
                style={{ width: `${(profile?.behavioral_metrics?.session_completion_rate || 0) * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
            <div>
              <span className="font-medium">Average Time per Quiz:</span>
              <br />
              {Math.round(profile?.behavioral_metrics?.average_time_per_quiz || 0)} minutes
            </div>
            <div>
              <span className="font-medium">Average Time per Concept:</span>
              <br />
              {Math.round(profile?.behavioral_metrics?.average_time_per_concept || 0)} minutes
            </div>
            <div>
              <span className="font-medium">Total Learning Time:</span>
              <br />
              {Math.round(profile?.behavioral_metrics?.total_learning_time || 0)} minutes
            </div>
            <div>
              <span className="font-medium">Engagement Score:</span>
              <br />
              {Math.round((profile?.behavioral_metrics?.engagement_score || 0) * 100)}%
            </div>
          </div>
        </div>
      </div>

      {/* Learning Style Charts */}
      <div className="space-y-8">
        {/* Perceptual Mode */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Perceptual Learning Style</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={perceptualData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#4F46E5" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cognitive Style */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Cognitive Style</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cognitiveData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#10B981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Social Preference */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Social Learning Preference</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={socialData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#F59E0B" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Instruction Style */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Preferred Instruction Style</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={instructionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#EC4899" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Assessment Preference */}
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Assessment Preference</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={assessmentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#8B5CF6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-500 mt-4">
        Last updated: {profile?.last_updated ? new Date(profile.last_updated).toLocaleString() : 'Not available'}
      </div>
    </div>
  );
} 