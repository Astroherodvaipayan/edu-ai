'use client';

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip
} from 'recharts';

interface KnowledgeStateType {
  topics: Record<string, number>;
  misconceptions: string[];
  strengths: string[];
  areas_for_improvement: string[];
  last_updated: string;
}

interface Props {
  knowledgeState: KnowledgeStateType;
}

export default function KnowledgeState({ knowledgeState }: Props) {
  // Transform topics data for radar chart
  const topicsData = Object.entries(knowledgeState?.topics || {}).map(([topic, mastery]) => ({
    topic,
    mastery: (mastery as number) * 100
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Knowledge State</h2>

      {/* Topics Radar Chart */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Topic Mastery</h3>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={topicsData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="topic" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar
                name="Mastery Level"
                dataKey="mastery"
                stroke="#4F46E5"
                fill="#4F46E5"
                fillOpacity={0.6}
              />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Strengths */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Strengths</h3>
        <div className="bg-green-50 rounded-lg p-4">
          {knowledgeState?.strengths && knowledgeState.strengths.length > 0 ? (
            <ul className="list-disc list-inside space-y-1">
              {knowledgeState.strengths.map((strength, index) => (
                <li key={index} className="text-green-700">{strength}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic">No strengths identified yet</p>
          )}
        </div>
      </div>

      {/* Areas for Improvement */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Areas for Improvement</h3>
        <div className="bg-yellow-50 rounded-lg p-4">
          {knowledgeState?.areas_for_improvement && knowledgeState.areas_for_improvement.length > 0 ? (
            <ul className="list-disc list-inside space-y-1">
              {knowledgeState.areas_for_improvement.map((area, index) => (
                <li key={index} className="text-yellow-700">{area}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic">No areas for improvement identified yet</p>
          )}
        </div>
      </div>

      {/* Misconceptions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">Misconceptions to Address</h3>
        <div className="bg-red-50 rounded-lg p-4">
          {knowledgeState?.misconceptions && knowledgeState.misconceptions.length > 0 ? (
            <ul className="list-disc list-inside space-y-1">
              {knowledgeState.misconceptions.map((misconception, index) => (
                <li key={index} className="text-red-700">{misconception}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic">No misconceptions identified yet</p>
          )}
        </div>
      </div>

      <div className="text-sm text-gray-500 mt-4">
        Last updated: {knowledgeState?.last_updated ? new Date(knowledgeState.last_updated).toLocaleString() : 'Not available'}
      </div>
    </div>
  );
} 