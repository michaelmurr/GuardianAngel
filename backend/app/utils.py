
from fastapi import HTTPException, status
from jwt.algorithms import RSAAlgorithm
import json

from app.models.alchemy.route import Route as RouteDB
from sqlalchemy.orm import Session

def get_rsa_key_from_jwks(jwks, kid):
    
    for key in jwks.get('keys', []):
        if key.get('kid') == kid:
            return RSAAlgorithm.from_jwk(json.dumps(key))
    return None

async def delete_users_route(
    user_id: str,
    db: Session
):
    route = db.query(RouteDB).filter(RouteDB.user_id == user_id).first()

    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")

    try:
        route_id = route.user_id
        db.delete(route)
        db.commit()
        return {"message": f"Route {route_id} deleted successfully"}
        

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete route")