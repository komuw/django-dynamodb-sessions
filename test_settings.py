from botocore.config import Config

SESSION_ENGINE = 'dynamodb_sessions.backends.dynamodb'
SECRET_KEY = 'foobar'
DYNAMODB_SESSIONS_AWS_ACCESS_KEY_ID = 'anything'
DYNAMODB_SESSIONS_AWS_SECRET_ACCESS_KEY = 'anything'
DYNAMODB_SESSIONS_AWS_REGION_NAME = 'eu-west-1'
LOCAL_DYNAMODB_SERVER = 'http://dynamoDb:8000'
BOTO_CORE_CONFIG = Config(
    connect_timeout=1,
    read_timeout=1,
    retries=dict(
        max_attempts=0
    )
)

INSTALLED_APPS = (
    'dynamodb_sessions',
)

DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
