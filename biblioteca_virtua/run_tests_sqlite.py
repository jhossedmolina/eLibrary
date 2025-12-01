#!/usr/bin/env python
"""
Script para ejecutar tests con SQLite en memoria
"""
import os
import sys
from pathlib import Path

# Determinar BASE_DIR
BASE_DIR = Path(__file__).resolve().parent

# IMPORTANTE: Configurar variable de entorno ANTES de importar Django
os.environ['TESTING'] = '1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_virtua.settings')

# Ahora importar y forzar configuración
import django
from django.conf import settings

# Forzar SQLite ANTES de django.setup()
if not settings.configured:
    settings.configure(
        DEBUG=True,
        BASE_DIR=BASE_DIR,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'core',
            'usuarios',
            'libros',
            'prestamos',
        ],
        SECRET_KEY='test-secret-key-for-testing-only',
        ROOT_URLCONF='biblioteca_virtua.urls',
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'biblioteca_virtua' / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        STATIC_URL='/static/',
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    )
else:
    # Si ya está configurado, forzar SQLite de todas formas
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

print("⚙️ MODO TEST: Forzando SQLite en memoria")
print(f"   Base de datos: {settings.DATABASES['default']['ENGINE']}")
print(f"   Templates DIR: {settings.TEMPLATES[0]['DIRS']}")

# Ejecutar el comando test
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    # Construir argumentos para el comando test
    argv = ['manage.py', 'test'] + sys.argv[1:]
    
    print(f"   Ejecutando: {' '.join(argv)}\n")
    execute_from_command_line(argv)
