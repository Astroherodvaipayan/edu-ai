from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Supabase URL and key from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Create Supabase client only if URL and key are available
_supabase_client: Client = None

def get_supabase_client() -> Client:
    """
    Returns the Supabase client instance.
    Initializes it if not already initialized.
    """
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client
        
    if not supabase_url or not supabase_key:
        logger.error("Supabase URL or key not found in environment variables")
        if not supabase_url:
            logger.error("SUPABASE_URL is missing")
        if not supabase_key:
            logger.error("SUPABASE_KEY is missing")
        raise ValueError("Supabase configuration is missing")
        
    try:
        logger.info(f"Initializing Supabase client with URL: {supabase_url}")
        _supabase_client = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized successfully")
        return _supabase_client
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {e}")
        raise