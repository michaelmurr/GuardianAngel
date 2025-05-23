
from jwt.algorithms import RSAAlgorithm
import json
def get_rsa_key_from_jwks(jwks, kid):
    
    for key in jwks.get('keys', []):
        if key.get('kid') == kid:
            return RSAAlgorithm.from_jwk(json.dumps(key))
    return None