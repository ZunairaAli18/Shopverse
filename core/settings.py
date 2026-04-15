from pathlib import Path
from decouple import config          # ← ADD THIS

BASE_DIR = Path(__file__).resolve().parent.parent


# ─── Security ─────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')    # ← CHANGE (was hardcoded string)
DEBUG = config('DEBUG', default=True, cast=bool)  # ← CHANGE
STRIPE_PUBLIC_KEY  = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY  = config('STRIPE_SECRET_KEY')
STRIPE_CURRENCY    = config('STRIPE_CURRENCY', default='pkr')
ALLOWED_HOSTS = ['*']                # ← CHANGE (was empty list)


# ─── Installed Apps ────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps ← ADD THESE 8
    'users',
    'stores',
    'products',
    'cart',
    'orders',
    'payments',
    'reviews',
    'notifications',
]

# ─── Middleware ─────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# ↑ KEEP THIS EXACTLY AS IS

ROOT_URLCONF = 'core.urls'  # ← KEEP

# ─── Templates ─────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← CHANGE (was empty list [])
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'  # ← KEEP

# ─── Database ───────────────────────────────────────────
DATABASES = {
     'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST'),
        'PORT':     config('DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 60,  # reuse connections for 60 seconds
    }
}

# ─── Custom User Model ──────────────────────────────────
AUTH_USER_MODEL = 'users.User'       # ← ADD THIS (very important!)

# ─── Password Validators ────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# ↑ KEEP THIS EXACTLY AS IS

# ─── Internationalisation ───────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'           # ← CHANGE (was UTC)
USE_I18N = True
USE_TZ = True
# ↑ rest stays the same

# ─── Static & Media ─────────────────────────────────────
STATIC_URL = '/static/'              # ← CHANGE (add leading slash)
STATICFILES_DIRS = [BASE_DIR / 'static']  # ← ADD
STATIC_ROOT = BASE_DIR / 'staticfiles'   # ← ADD

MEDIA_URL = '/media/'                # ← ADD
MEDIA_ROOT = BASE_DIR / 'media'     # ← ADD

# ─── Auth Redirects ─────────────────────────────────────
LOGIN_URL = '/users/login/'          # ← ADD
LOGIN_REDIRECT_URL = '/'             # ← ADD
LOGOUT_REDIRECT_URL = '/users/login/' # ← ADD

# ─── Default Primary Key ────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # ← KEEP (already there)