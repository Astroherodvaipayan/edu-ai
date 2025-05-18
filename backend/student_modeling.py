from typing import List, Dict, Optional, Any
import numpy as np
from datetime import datetime
from supabase_client import get_supabase_client

class LearningStyleProfile:
    def __init__(self):
        self.perceptual_mode = {
            'visual': 0.0,
            'auditory': 0.0,
            'reading_writing': 0.0,
            'kinesthetic': 0.0
        }
        self.cognitive_style = {
            'global': 0.0,
            'analytical': 0.0
        }
        self.social_preference = {
            'independent': 0.0,
            'collaborative': 0.0
        }
        self.instruction_style = {
            'direct': 0.0,
            'constructivist': 0.0,
            'inquiry_based': 0.0,
            'project_based': 0.0
        }
        self.assessment_preference = {
            'formative': 0.0,
            'summative': 0.0,
            'performance': 0.0
        }
        self.cognitive_metrics = {
            'beginner_level': 0.0,
            'intermediate_level': 0.0,
            'advanced_level': 0.0,
            'total_quizzes_taken': 0,
            'quiz_scores': [],  # List of quiz scores
            'concept_detective_scores': [],  # List of concept detective scores
            'overall_progress': 0.0  # Weighted average of all cognitive metrics
        }
        self.behavioral_metrics = {
            'average_time_per_quiz': 0.0,  # in minutes
            'average_time_per_concept': 0.0,  # in minutes
            'total_learning_time': 0.0,  # in minutes
            'session_completion_rate': 0.0,  # percentage of started sessions completed
            'engagement_score': 0.0
        }
        self.learning_metrics = {
            'completion_rate': 0.0,
            'time_to_learn': 0.0,  # Average time in minutes
            'engagement_score': 0.0
        }
        self.last_updated = datetime.now()

class KnowledgeState:
    def __init__(self):
        self.topics = {}  # Topic -> Confidence mapping
        self.misconceptions = []
        self.strengths = []
        self.areas_for_improvement = []
        self.last_updated = datetime.now()

class QuizAttempt:
    def __init__(self, quiz_id: str, score: float, time_taken: float, level: str):
        self.quiz_id = quiz_id
        self.score = score  # percentage correct
        self.time_taken = time_taken  # in minutes
        self.level = level  # 'beginner', 'intermediate', or 'advanced'
        self.timestamp = datetime.now()

class ConceptDetectiveAttempt:
    def __init__(self, concept_id: str, score: float, time_taken: float, level: str):
        self.concept_id = concept_id
        self.score = score  # overall score for the concept
        self.time_taken = time_taken  # in minutes
        self.level = level  # difficulty level
        self.timestamp = datetime.now()

class LLMInteraction:
    def __init__(self, question: str, response: str, interaction_type: str):
        self.question = question
        self.response = response
        self.interaction_type = interaction_type  # 'quiz', 'concept_detective', 'chat'
        self.timestamp = datetime.now()
        self.evaluation_score = 0.0
        self.learning_indicators = {}

def analyze_message_for_learning_style(message: str) -> Dict[str, float]:
    """
    Analyzes a single message for learning style indicators using comprehensive psychological markers
    Returns confidence scores for different style aspects
    """
    # Enhanced psychological markers for each dimension
    indicators = {
        'visual': [
            'see', 'look', 'picture', 'diagram', 'graph', 'image', 'visualize', 'draw',
            'color', 'observe', 'view', 'watch', 'appear', 'show', 'visible'
        ],
        'auditory': [
            'hear', 'sound', 'tell', 'explain', 'discuss', 'listen', 'speak', 'talk',
            'voice', 'audio', 'noise', 'silence', 'loud', 'quiet'
        ],
        'reading_writing': [
            'read', 'write', 'note', 'text', 'book', 'document', 'list', 'word',
            'essay', 'paper', 'journal', 'summary', 'definition'
        ],
        'kinesthetic': [
            'do', 'try', 'practice', 'experiment', 'hands-on', 'build', 'create',
            'feel', 'touch', 'move', 'action', 'physical', 'experience'
        ],
        'global': [
            'overall', 'big picture', 'generally', 'concept', 'broad', 'whole',
            'context', 'relationship', 'connection', 'pattern'
        ],
        'analytical': [
            'detail', 'specific', 'step', 'analyze', 'break down', 'precise',
            'exact', 'particular', 'component', 'element'
        ],
        'independent': [
            'self', 'alone', 'individual', 'my own', 'personally', 'independent',
            'autonomy', 'self-directed', 'private'
        ],
        'collaborative': [
            'group', 'team', 'together', 'share', 'discuss', 'collaborate',
            'partner', 'peer', 'collective', 'community'
        ],
        'formative': [
            'feedback', 'improve', 'progress', 'learn from', 'guidance',
            'development', 'growth', 'adjust', 'refine'
        ],
        'summative': [
            'test', 'exam', 'final', 'grade', 'assessment', 'evaluation',
            'measure', 'score', 'performance'
        ],
        'performance': [
            'project', 'demonstrate', 'show', 'present', 'portfolio',
            'exhibit', 'display', 'practical', 'real-world'
        ]
    }
    
    # Context patterns for more accurate analysis
    context_patterns = {
        'visual': r'(prefer|like|need)\s+to\s+(see|visualize)',
        'auditory': r'(better|best)\s+when\s+I\s+(hear|listen)',
        'reading_writing': r'(learn|understand)\s+by\s+(reading|writing)',
        'kinesthetic': r'(learn|work)\s+best\s+with\s+hands[-\s]on',
        'global': r'(understand|see)\s+the\s+big\s+picture',
        'analytical': r'(break|break\s+down|analyze)\s+step\s+by\s+step',
        'independent': r'(prefer|like)\s+to\s+work\s+alone',
        'collaborative': r'(enjoy|prefer)\s+group\s+work',
        'formative': r'(want|need)\s+regular\s+feedback',
        'summative': r'(focus|concerned)\s+about\s+(grades|scores)',
        'performance': r'(show|demonstrate)\s+what\s+I\s+(know|learned)'
    }
    
    scores = {style: 0.0 for style in indicators.keys()}
    message = message.lower()
    
    # Word-based analysis
    for style, words in indicators.items():
        for word in words:
            if word in message:
                scores[style] += 0.2  # Base score for word matches
                
    # Context-based analysis
    import re
    for style, pattern in context_patterns.items():
        if re.search(pattern, message):
            scores[style] += 0.4  # Higher score for contextual matches
    
    # Consider sentence structure and emphasis
    emphasis_patterns = {
        r'really\s+(\w+)': 0.3,
        r'definitely\s+(\w+)': 0.3,
        r'always\s+(\w+)': 0.3,
        r'prefer\s+(\w+)': 0.4
    }
    
    for pattern, bonus in emphasis_patterns.items():
        matches = re.finditer(pattern, message)
        for match in matches:
            emphasized_word = match.group(1)
            for style, words in indicators.items():
                if any(word in emphasized_word for word in words):
                    scores[style] += bonus
    
    # Normalize scores
    total = sum(scores.values()) + 1e-10  # Avoid division by zero
    normalized_scores = {k: min(v/total, 1.0) for k, v in scores.items()}
    
    return normalized_scores

def extract_learning_styles(chat_history: List[str]) -> LearningStyleProfile:
    """
    Analyzes chat history to extract learning style preferences with temporal weighting
    """
    profile = LearningStyleProfile()
    
    if not chat_history:
        return profile
    
    # Initialize weighted scores
    style_scores = []
    
    # Apply temporal weighting - recent messages have more influence
    message_count = len(chat_history)
    for i, message in enumerate(chat_history):
        # Calculate temporal weight (more recent messages have higher weight)
        temporal_weight = 0.5 + 0.5 * (i / max(1, message_count - 1))
        
        # Analyze message
        message_scores = analyze_message_for_learning_style(message)
        
        # Apply temporal weight
        weighted_scores = {
            style: score * temporal_weight 
            for style, score in message_scores.items()
        }
        style_scores.append(weighted_scores)
    
    # Aggregate scores
    aggregated_scores = {}
    for style in style_scores[0].keys():
        style_values = [score[style] for score in style_scores]
        # Use exponential moving average for smoother transitions
        alpha = 0.7  # Smoothing factor
        ema = style_values[0]
        for value in style_values[1:]:
            ema = alpha * value + (1 - alpha) * ema
        aggregated_scores[style] = ema
    
    # Update profile with aggregated scores
    for style, score in aggregated_scores.items():
        if style in profile.perceptual_mode:
            profile.perceptual_mode[style] = score
        elif style in profile.cognitive_style:
            profile.cognitive_style[style] = score
        elif style in profile.social_preference:
            profile.social_preference[style] = score
        elif style in profile.instruction_style:
            profile.instruction_style[style] = score
        elif style in profile.assessment_preference:
            profile.assessment_preference[style] = score
    
    return profile

def update_knowledge_trace(chat_history: List[str]) -> KnowledgeState:
    """
    Updates the knowledge state based on chat history
    """
    knowledge_state = KnowledgeState()
    
    # Simple keyword-based topic extraction
    topics = set()
    for message in chat_history:
        # Add sophisticated topic extraction logic here
        pass
        
    return knowledge_state

async def save_student_profile(user_id: str, profile: LearningStyleProfile):
    """
    Saves the student profile to Supabase
    """
    profile_data = {
        'user_id': user_id,
        'perceptual_mode': profile.perceptual_mode,
        'cognitive_style': profile.cognitive_style,
        'social_preference': profile.social_preference,
        'instruction_style': profile.instruction_style,
        'assessment_preference': profile.assessment_preference,
        'cognitive_metrics': profile.cognitive_metrics,
        'behavioral_metrics': profile.behavioral_metrics,
        'learning_metrics': profile.learning_metrics,
        'last_updated': profile.last_updated.isoformat()
    }
    
    try:
        response = await get_supabase_client().table('student_profiles').upsert(profile_data).execute()
        return response.data
    except Exception as e:
        print(f"Error saving student profile: {e}")
        return None

async def get_student_profile(user_id: str) -> Optional[LearningStyleProfile]:
    """
    Retrieves the student profile from Supabase
    """
    try:
        response = await get_supabase_client().table('student_profiles').select('*').eq('user_id', user_id).execute()
        if response.data:
            profile = LearningStyleProfile()
            data = response.data[0]
            profile.perceptual_mode = data['perceptual_mode']
            profile.cognitive_style = data['cognitive_style']
            profile.social_preference = data['social_preference']
            profile.instruction_style = data['instruction_style']
            profile.assessment_preference = data['assessment_preference']
            profile.cognitive_metrics = data['cognitive_metrics']
            profile.behavioral_metrics = data['behavioral_metrics']
            profile.learning_metrics = data['learning_metrics']
            profile.last_updated = datetime.fromisoformat(data['last_updated'])
            return profile
        return None
    except Exception as e:
        print(f"Error retrieving student profile: {e}")
        return None

async def get_knowledge_state(user_id: str) -> Optional[KnowledgeState]:
    """
    Retrieves the knowledge state from Supabase
    """
    try:
        response = await get_supabase_client().table('knowledge_states').select('*').eq('user_id', user_id).execute()
        if response.data:
            knowledge_state = KnowledgeState()
            data = response.data[0]
            knowledge_state.topics = data['topics']
            knowledge_state.misconceptions = data['misconceptions']
            knowledge_state.strengths = data['strengths']
            knowledge_state.areas_for_improvement = data['areas_for_improvement']
            knowledge_state.last_updated = datetime.fromisoformat(data['last_updated'])
            return knowledge_state
        return None
    except Exception as e:
        print(f"Error retrieving knowledge state: {e}")
        return None

async def save_knowledge_state(user_id: str, state: KnowledgeState):
    """
    Saves the knowledge state to Supabase
    """
    state_data = {
        'user_id': user_id,
        'topics': state.topics,
        'misconceptions': state.misconceptions,
        'strengths': state.strengths,
        'areas_for_improvement': state.areas_for_improvement,
        'last_updated': state.last_updated.isoformat()
    }
    
    try:
        response = await get_supabase_client().table('knowledge_states').upsert(state_data).execute()
        return response.data
    except Exception as e:
        print(f"Error saving knowledge state: {e}")
        return None

def update_cognitive_metrics(profile: LearningStyleProfile, quiz_attempts: List[QuizAttempt], concept_attempts: List[ConceptDetectiveAttempt]) -> LearningStyleProfile:
    """
    Updates cognitive metrics based on quiz and concept detective performance
    """
    if not profile:
        profile = LearningStyleProfile()

    # Calculate level-specific progress
    level_scores = {'beginner': [], 'intermediate': [], 'advanced': []}
    
    # Process quiz attempts
    for attempt in quiz_attempts:
        level_scores[attempt.level].append(attempt.score)
        profile.cognitive_metrics['quiz_scores'].append(attempt.score)
    
    # Process concept detective attempts
    for attempt in concept_attempts:
        level_scores[attempt.level].append(attempt.score)
        profile.cognitive_metrics['concept_detective_scores'].append(attempt.score)
    
    # Update level-specific progress
    if level_scores['beginner']:
        profile.cognitive_metrics['beginner_level'] = sum(level_scores['beginner']) / len(level_scores['beginner'])
    if level_scores['intermediate']:
        profile.cognitive_metrics['intermediate_level'] = sum(level_scores['intermediate']) / len(level_scores['intermediate'])
    if level_scores['advanced']:
        profile.cognitive_metrics['advanced_level'] = sum(level_scores['advanced']) / len(level_scores['advanced'])
    
    # Calculate overall progress (weighted average)
    weights = {'beginner': 0.3, 'intermediate': 0.3, 'advanced': 0.4}
    total_progress = 0
    total_weight = 0
    
    for level, weight in weights.items():
        if level_scores[level]:
            total_progress += profile.cognitive_metrics[f'{level}_level'] * weight
            total_weight += weight
    
    if total_weight > 0:
        profile.cognitive_metrics['overall_progress'] = total_progress / total_weight
    
    profile.cognitive_metrics['total_quizzes_taken'] = len(quiz_attempts) + len(concept_attempts)
    
    return profile

def update_behavioral_metrics(profile: LearningStyleProfile, quiz_attempts: List[QuizAttempt], concept_attempts: List[ConceptDetectiveAttempt]) -> LearningStyleProfile:
    """
    Updates behavioral metrics based on time spent and engagement
    """
    if not profile:
        profile = LearningStyleProfile()
    
    # Calculate average times
    quiz_times = [attempt.time_taken for attempt in quiz_attempts]
    concept_times = [attempt.time_taken for attempt in concept_attempts]
    
    if quiz_times:
        profile.behavioral_metrics['average_time_per_quiz'] = sum(quiz_times) / len(quiz_times)
    
    if concept_times:
        profile.behavioral_metrics['average_time_per_concept'] = sum(concept_times) / len(concept_times)
    
    # Update total learning time
    profile.behavioral_metrics['total_learning_time'] = sum(quiz_times) + sum(concept_times)
    
    # Calculate session completion rate
    total_attempts = len(quiz_attempts) + len(concept_attempts)
    if total_attempts > 0:
        completed_attempts = len([a for a in quiz_attempts if a.score > 0]) + len([a for a in concept_attempts if a.score > 0])
        profile.behavioral_metrics['session_completion_rate'] = completed_attempts / total_attempts
    
    # Calculate engagement score based on completion rate and time spent
    time_factor = min(1.0, profile.behavioral_metrics['total_learning_time'] / (60 * 8))  # Cap at 8 hours
    completion_factor = profile.behavioral_metrics['session_completion_rate']
    profile.behavioral_metrics['engagement_score'] = (time_factor * 0.4) + (completion_factor * 0.6)
    
    return profile 

def evaluate_llm_interaction(interaction: LLMInteraction) -> Dict[str, float]:
    """
    Evaluates an LLM interaction for learning indicators and quality
    """
    # Initialize evaluation metrics
    evaluation = {
        'comprehension': 0.0,
        'depth': 0.0,
        'engagement': 0.0,
        'critical_thinking': 0.0
    }
    
    # Analyze question complexity
    question_indicators = {
        'what': 0.3,  # Basic comprehension
        'how': 0.6,   # Process understanding
        'why': 0.8,   # Deep understanding
        'compare': 0.7,
        'analyze': 0.8,
        'evaluate': 0.9
    }
    
    # Calculate question complexity score
    question = interaction.question.lower()
    for indicator, weight in question_indicators.items():
        if indicator in question:
            evaluation['depth'] += weight
    
    # Analyze response quality
    response = interaction.response.lower()
    
    # Check for explanation patterns
    if 'because' in response or 'therefore' in response:
        evaluation['comprehension'] += 0.5
    
    # Check for critical thinking indicators
    critical_indicators = ['however', 'although', 'on the other hand', 'alternatively']
    for indicator in critical_indicators:
        if indicator in response:
            evaluation['critical_thinking'] += 0.3
    
    # Calculate engagement based on response length and detail
    words = len(response.split())
    evaluation['engagement'] = min(1.0, words / 100)  # Cap at 1.0
    
    # Normalize scores
    for metric in evaluation:
        evaluation[metric] = min(1.0, evaluation[metric])
    
    return evaluation

def update_learning_profile_from_llm(profile: LearningStyleProfile, 
                                   interaction: LLMInteraction,
                                   evaluation: Dict[str, float]) -> LearningStyleProfile:
    """
    Updates the learning profile based on LLM interaction evaluation
    """
    # Update cognitive metrics based on evaluation
    if interaction.interaction_type == 'quiz':
        profile.cognitive_metrics['quiz_scores'].append(evaluation['comprehension'] * 100)
        level_score = evaluation['depth']
        
        if level_score < 0.4:
            profile.cognitive_metrics['beginner_level'] = (
                profile.cognitive_metrics['beginner_level'] * 0.7 + level_score * 0.3
            )
        elif level_score < 0.7:
            profile.cognitive_metrics['intermediate_level'] = (
                profile.cognitive_metrics['intermediate_level'] * 0.7 + level_score * 0.3
            )
        else:
            profile.cognitive_metrics['advanced_level'] = (
                profile.cognitive_metrics['advanced_level'] * 0.7 + level_score * 0.3
            )
    
    # Update behavioral metrics
    profile.behavioral_metrics['engagement_score'] = (
        profile.behavioral_metrics['engagement_score'] * 0.7 + 
        evaluation['engagement'] * 0.3
    )
    
    # Update learning style preferences based on interaction patterns
    question_patterns = {
        'visual': ['see', 'look', 'picture', 'diagram'],
        'auditory': ['hear', 'sound', 'explain'],
        'reading_writing': ['read', 'write', 'note'],
        'kinesthetic': ['do', 'try', 'practice']
    }
    
    # Analyze question for learning style indicators
    question = interaction.question.lower()
    for style, patterns in question_patterns.items():
        if any(pattern in question for pattern in patterns):
            profile.perceptual_mode[style] = (
                profile.perceptual_mode[style] * 0.8 + 0.2
            )
    
    # Calculate overall progress
    total_scores = (
        profile.cognitive_metrics['beginner_level'] +
        profile.cognitive_metrics['intermediate_level'] * 1.5 +
        profile.cognitive_metrics['advanced_level'] * 2
    )
    profile.cognitive_metrics['overall_progress'] = min(1.0, total_scores / 4.5)
    
    # Update timestamp
    profile.last_updated = datetime.now()
    
    return profile

async def process_llm_interaction(user_id: str, 
                                question: str, 
                                response: str, 
                                interaction_type: str = 'chat') -> Dict[str, Any]:
    """
    Process and evaluate an LLM interaction, updating the student profile
    """
    # Create interaction object
    interaction = LLMInteraction(question, response, interaction_type)
    
    # Evaluate the interaction
    evaluation = evaluate_llm_interaction(interaction)
    
    # Get or create student profile
    profile = await get_student_profile(user_id)
    if not profile:
        profile = LearningStyleProfile()
    
    # Update profile with evaluation results
    updated_profile = update_learning_profile_from_llm(profile, interaction, evaluation)
    
    # Save updated profile
    await save_student_profile(user_id, updated_profile)
    
    # Return evaluation results and updated profile metrics
    return {
        'evaluation': evaluation,
        'profile_metrics': {
            'overall_progress': updated_profile.cognitive_metrics['overall_progress'] * 100,
            'engagement_score': updated_profile.behavioral_metrics['engagement_score'] * 100,
            'learning_style': max(updated_profile.perceptual_mode.items(), key=lambda x: x[1])[0],
            'current_level': get_current_level(updated_profile)
        }
    }

def get_current_level(profile: LearningStyleProfile) -> str:
    """
    Determines the current learning level based on cognitive metrics
    """
    levels = {
        'beginner': profile.cognitive_metrics['beginner_level'],
        'intermediate': profile.cognitive_metrics['intermediate_level'],
        'advanced': profile.cognitive_metrics['advanced_level']
    }
    return max(levels.items(), key=lambda x: x[1])[0] 