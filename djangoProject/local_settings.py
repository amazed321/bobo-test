from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo11',
        'USER': 'root',
        'PASSWORD': '123321',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}