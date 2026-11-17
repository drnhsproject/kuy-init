"""Users API."""
MAX_USERS = 10
cache: dict = {}

class UserService(Base):
    """Handles users."""
    def get(self, user_id: int) -> dict:
        """Fetch one user."""
        return {}

async def list_users(limit: int = 5):
    return []
