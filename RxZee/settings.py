from pathlib import Path

SITE_ID = 1
SITE_URL = 'https://rxzee.com'
ADMIN_PATH = "admin/"
AUTH_USER_MODEL = 'app.User'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads"
GZIP_LEVEL = 6

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'c47a7f48a12b3e2f849f03eb582cfce6b658874a738194012f683eecfe317954a8191cb41eca4084551fa6575ba653e0a776f3dbce37559bcb617efe8662d'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
ROOT_URLCONF = 'RxZee.urls'
WSGI_APPLICATION = 'RxZee.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
X_FRAME_OPTIONS = 'DENY'
STATIC_URL = 'static/'
MEDIA_URL = '/images/'
MEDIA_ROOT = BASE_DIR / 'media/'
STATIC_ROOT = BASE_DIR / 'static/'
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'rxzee_postgres', 'USER': 'rxzee_postgres', 'PASSWORD': 'rxzee_postgres', 'HOST': 'localhost', 'PORT': ''}}
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / "database.sqlite3"}}

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your email
# EMAIL_HOST_PASSWORD = 'your-email-password'  # Replace with your email password
CKEDITOR_CONFIGS = {"default": {"toolbar": [['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],['NumberedList', 'BulletedList', 'Outdent', 'Indent', 'Blockquote'],['Link', 'Unlink', 'Anchor'],['Image', 'Table', 'HorizontalRule', 'SpecialChar'],['Subscript', 'Superscript']],'height': '500px','width': '100%','toolbarCanCollapse': True,'removePlugins': ['elementspath', "exportpdf"],'resize_enabled': False,'extraPlugins': 'divarea','allowedContent': True,}}
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.sites', 'django.contrib.sitemaps', 'app', 'ckeditor', 'ckeditor_uploader']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.middleware.gzip.GZipMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware', 'app.middleware.CheckUserSessionMiddleware']
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]