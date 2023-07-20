from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL")
JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITHM = env.str("JWT_ALGORITHM", "HS256")
REDIS_URL = env.str("REDIS_URL", "redis://localhost:6379/2")
PUBLIC_ROUTES = env.list("PUBLIC_ROUTES", [])
TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN")
TWILIO_MESSAGE_SERVICE_SID = env.str("TWILIO_MESSAGE_SERVICE_SID")
SENTRY_DSN = env.str("SENTRY_DSN")
