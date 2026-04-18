"""
Authentication system using JWT tokens (lightweight implementation)
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
import hashlib
import secrets
import json
import base64

# In production, use environment variables
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

class AuthManager:
    """Manages user authentication and JWT tokens"""
    
    # Mock database of users - in production use real database
    users_db: Dict[str, Dict] = {}
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt with salt"""
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against bcrypt hash"""
        import bcrypt
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    
    @classmethod
    def create_user(cls, email: str, password: str, plan: str = "free") -> Dict:
        """Create new user account"""
        if email in cls.users_db:
            return {"error": "User already exists"}
        
        user = {
            "email": email,
            "password_hash": cls.hash_password(password),
            "plan": plan,
            "created_at": datetime.utcnow().isoformat(),
            "api_calls": 0,
            "limit": cls._get_plan_limit(plan),
            "api_key": secrets.token_urlsafe(32)
        }
        cls.users_db[email] = user
        return {"success": True, "user_id": email, "api_key": user["api_key"]}
    
    @classmethod
    def authenticate_user(cls, email: str, password: str) -> Dict:
        """Authenticate user and return JWT token"""
        if email not in cls.users_db:
            return {"error": "User not found"}
        
        user = cls.users_db[email]
        if not cls.verify_password(password, user["password_hash"]):
            return {"error": "Invalid password"}
        
        # Create JWT token
        token = cls.create_access_token({"sub": email, "plan": user["plan"]})
        return {"access_token": token, "token_type": "bearer", "plan": user["plan"]}
    
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT-like access token (simplified implementation)"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire.isoformat()})
        
        # Simple token encoding (in production use real JWT library)
        token_string = json.dumps(to_encode)
        token_bytes = base64.b64encode(token_string.encode()).decode()
        return token_bytes
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """Verify JWT-like token and return payload"""
        try:
            token_string = base64.b64decode(token.encode()).decode()
            payload = json.loads(token_string)
            
            # Check expiration
            exp_time = datetime.fromisoformat(payload.get("exp", ""))
            if exp_time < datetime.utcnow():
                return None
            
            return payload
        except Exception:
            return None
    
    @staticmethod
    def _get_plan_limit(plan: str) -> int:
        """Get API call limit for plan"""
        limits = {
            "free": 100,
            "pro": 5000,
            "enterprise": 50000
        }
        return limits.get(plan, 100)
    
    @classmethod
    def check_rate_limit(cls, email: str) -> bool:
        """Check if user has API calls remaining"""
        if email not in cls.users_db:
            return False
        
        user = cls.users_db[email]
        return user["api_calls"] < user["limit"]
    
    @classmethod
    def increment_api_calls(cls, email: str) -> None:
        """Increment API call count"""
        if email in cls.users_db:
            cls.users_db[email]["api_calls"] += 1
    
    @classmethod
    def upgrade_plan(cls, email: str, new_plan: str) -> Dict:
        """Upgrade user plan"""
        if email not in cls.users_db:
            return {"error": "User not found"}
        
        cls.users_db[email]["plan"] = new_plan
        cls.users_db[email]["limit"] = cls._get_plan_limit(new_plan)
        cls.users_db[email]["api_calls"] = 0  # Reset counter
        return {"success": True, "new_plan": new_plan}
