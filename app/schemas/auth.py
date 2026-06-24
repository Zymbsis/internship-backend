from app.schemas.user import UserCreate, UserCredentials, UserDetailResponse


class SignUpRequest(UserCreate):
    pass


class SignUpResponse(UserDetailResponse):
    pass


class SignInRequest(UserCredentials):
    pass
