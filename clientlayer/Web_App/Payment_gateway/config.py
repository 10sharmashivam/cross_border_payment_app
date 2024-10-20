import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    FLYTE_PROJECT = 'payment_project'
    FLYTE_DOMAIN = 'development'