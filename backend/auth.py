from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
from supabase_client import get_supabase_client
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Using SUPABASE_KEY for consistency with your supabase_client.py
SUPABASE_KEY = os.getenv("SUPABASE_KEY") 

headers = {
    "apikey": SUPABASE_KEY,  # Changed from SUPABASE_API_KEY
    "Content-Type": "application/json"
}

# Create router
router = APIRouter(prefix="/auth", tags=["auth"])

# Get Supabase client
supabase = get_supabase_client()

# Security scheme for protected routes
security = HTTPBearer()

# Models
class UserSignUp(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

# Helper function to check Supabase client
def check_supabase():
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service not available. Check Supabase client initialization, .env variables, and server logs."
        )

# Endpoints
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_input: UserSignUp):
    """
    Create a new user account with email and password
    """
    check_supabase()
    
    try:
        # Following the Supabase docs for sign-up
        response = supabase.auth.sign_up({
            "email": user_input.email,
            "password": user_input.password
        })
        
        if response.user:
            # You might want to be more specific about what user details are returned
            user_details = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": response.user.created_at
            }
            return {
                "message": "User created successfully! Please check your email for verification.",
                "user": user_details
            }
        # Supabase specific error handling if response.error exists
        elif hasattr(response, 'error') and response.error:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.error.message)
        else:
            # Fallback error if user is not created and no specific Supabase error
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user account.")
    
    except HTTPException as e:
        raise e # Re-raise HTTPException to keep original status code and detail
    except Exception as e:
        error_msg = str(e)
        # Check for common Supabase error messages
        if "User already registered" in error_msg or ("already exists" in error_msg and "users_email_key" in error_msg):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during signup: {error_msg}")

@router.post("/login", response_model=Token)
async def login(user_input: UserLogin):
    """
    Authenticate user and return access token
    """
    check_supabase()
    
    try:
        # Following the Supabase docs for sign-in
        response = supabase.auth.sign_in_with_password({
            "email": user_input.email,
            "password": user_input.password
        })
        
        if response.session and response.user:
            user_details = {
                "id": response.user.id,
                "email": response.user.email,
                "aud": response.user.aud, # Audience
                "created_at": response.user.created_at
            }
            return {
                "access_token": response.session.access_token,
                "token_type": "bearer", # Added missing token_type
                "user": user_details
            }
        elif hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response.error.message)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed. No session or user data returned.")
    
    except HTTPException as e:
        raise e
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during login: {error_msg}")

@router.post("/logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Sign out the current user
    """
    check_supabase()
    
    try:
        # Following the Supabase docs for sign-out
        api_response_error = supabase.auth.sign_out() # Returns an APIResponseError if it fails, None otherwise
        if api_response_error:
            # This is less common for sign_out, but good to handle
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Logout failed: {str(api_response_error)}")
        return {"message": "Logged out successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Logout failed: {str(e)}")

@router.get("/user", response_model=Dict[str, Any])
async def get_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user's information
    """
    check_supabase()
    
    try:
        token = credentials.credentials
        response = supabase.auth.get_user(token)
        if response.user:
            user_details = {
                "id": response.user.id,
                "email": response.user.email,
                "aud": response.user.aud,
                "created_at": response.user.created_at
                # Add other user fields you need
            }
            return user_details
        elif hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response.error.message)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or unable to retrieve user.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving user: {str(e)}")

# API routes can use this to verify the user is authenticated
@router.get("/verify")
async def verify_token_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify if a token is valid
    """
    check_supabase()
    
    try:
        token = credentials.credentials
        response = supabase.auth.get_supabase_client() # This was supabase.auth.get_user(token)
        if response.user: # Assuming get_user returns an object with a user attribute
            return {"valid": True, "user_id": response.user.id, "email": response.user.email}
        else:
            error_detail = "Invalid token"
            if hasattr(response, 'error') and response.error and hasattr(response.error, 'message'):
                error_detail = response.error.message
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_detail)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Token verification failed: {str(e)}")

async def signup_user(email: str, password: str):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            headers=headers,
            json={"email": email, "password": password}
        )
        response_data = response.json()
        if response.status_code >= 400: # Check for HTTP error status
            error_detail = response_data.get("msg") or response_data.get("message") or "Signup failed"
            if "User already registered" in str(response_data):
                 error_detail = "User already registered"
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response_data

async def login_user(email: str, password: str):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            headers=headers,
            json={"email": email, "password": password}
        )
        response_data = response.json()
        if response.status_code >= 400: # Check for HTTP error status
            error_detail = response_data.get("error_description") or response_data.get("msg") or "Login failed"
            if "Invalid login credentials" in str(response_data):
                error_detail = "Invalid login credentials"
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        return response_data 