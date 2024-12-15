from datetime import timedelta
from typing import Literal, NewType


JwtSecret = NewType("JwtSecret", str)
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
JwtAccessTokenTtlMin = NewType("JwtAccessTokenTtlMin", timedelta)
SessionRefreshThreshold = NewType("SessionRefreshThreshold", float)
