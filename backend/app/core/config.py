from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str
    aws_region: str
    stripe_secret_key: str
    stripe_webhook_secret: str
    resend_api_key: str
    from_email: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    slack_webhook_url: str
    environment: str    
    
    class Config:
         env_file = ".env"
         env_file_encoding = "utf-8"
        

settings = Settings()
