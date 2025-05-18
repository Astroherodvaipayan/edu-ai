from supabase_client import get_supabase_client
import logging

logger = logging.getLogger(__name__)

async def setup_student_profiles_table():
    """
    Creates the student_profiles table in Supabase if it doesn't exist
    """
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Cannot setup tables: Supabase client not available")
        return False

    try:
        # Create the student_profiles table
        await supabase.table('student_profiles').execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id TEXT REFERENCES auth.users(id) NOT NULL,
                perceptual_mode JSONB NOT NULL,
                cognitive_style JSONB NOT NULL,
                social_preference JSONB NOT NULL,
                instruction_style JSONB NOT NULL,
                assessment_preference JSONB NOT NULL,
                cognitive_metrics JSONB NOT NULL DEFAULT '{
                    "beginner_level": 0,
                    "intermediate_level": 0,
                    "advanced_level": 0,
                    "total_quizzes_taken": 0,
                    "quiz_scores": [],
                    "concept_detective_scores": [],
                    "overall_progress": 0
                }'::jsonb,
                behavioral_metrics JSONB NOT NULL DEFAULT '{
                    "average_time_per_quiz": 0,
                    "average_time_per_concept": 0,
                    "total_learning_time": 0,
                    "session_completion_rate": 0,
                    "engagement_score": 0
                }'::jsonb,
                last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(user_id)
            );
        """)
        
        # Create indexes
        await supabase.table('student_profiles').execute("""
            CREATE INDEX IF NOT EXISTS idx_student_profiles_user_id ON student_profiles(user_id);
            CREATE INDEX IF NOT EXISTS idx_student_profiles_last_updated ON student_profiles(last_updated);
        """)
        
        logger.info("Student profiles table setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up student profiles table: {e}")
        return False

async def setup_knowledge_states_table():
    """
    Creates the knowledge_states table in Supabase if it doesn't exist
    """
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Cannot setup tables: Supabase client not available")
        return False

    try:
        # Create the knowledge_states table
        await supabase.table('knowledge_states').execute("""
            CREATE TABLE IF NOT EXISTS knowledge_states (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id TEXT REFERENCES auth.users(id) NOT NULL,
                topics JSONB NOT NULL DEFAULT '{}',
                misconceptions TEXT[] DEFAULT ARRAY[]::TEXT[],
                strengths TEXT[] DEFAULT ARRAY[]::TEXT[],
                areas_for_improvement TEXT[] DEFAULT ARRAY[]::TEXT[],
                last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        
        # Create indexes
        await supabase.table('knowledge_states').execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_states_user_id ON knowledge_states(user_id);
            CREATE INDEX IF NOT EXISTS idx_knowledge_states_last_updated ON knowledge_states(last_updated);
        """)
        
        logger.info("Knowledge states table setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up knowledge states table: {e}")
        return False

# Create a new table for quiz and concept detective attempts
async def setup_learning_attempts_table():
    """
    Creates the learning_attempts table in Supabase if it doesn't exist
    """
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Cannot setup tables: Supabase client not available")
        return False

    try:
        # Create the learning_attempts table
        await supabase.table('learning_attempts').execute("""
            CREATE TABLE IF NOT EXISTS learning_attempts (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id TEXT REFERENCES auth.users(id) NOT NULL,
                attempt_type TEXT NOT NULL CHECK (attempt_type IN ('quiz', 'concept_detective')),
                content_id TEXT NOT NULL,
                score FLOAT NOT NULL,
                time_taken FLOAT NOT NULL,
                level TEXT NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                metadata JSONB DEFAULT '{}'::jsonb
            );
        """)
        
        # Create indexes
        await supabase.table('learning_attempts').execute("""
            CREATE INDEX IF NOT EXISTS idx_learning_attempts_user_id ON learning_attempts(user_id);
            CREATE INDEX IF NOT EXISTS idx_learning_attempts_type ON learning_attempts(attempt_type);
            CREATE INDEX IF NOT EXISTS idx_learning_attempts_timestamp ON learning_attempts(timestamp);
        """)
        
        logger.info("Learning attempts table setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up learning attempts table: {e}")
        return False

async def setup_all_tables():
    """
    Sets up all required tables for the student modeling system
    """
    success = True
    success &= await setup_student_profiles_table()
    success &= await setup_knowledge_states_table()
    success &= await setup_learning_attempts_table()
    return success 