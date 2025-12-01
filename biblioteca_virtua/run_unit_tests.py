#!/usr/bin/env python
"""
Ejecuta solo los tests unitarios mockeados (ViewTest)
que NO requieren base de datos
"""
import os
import sys
from pathlib import Path
import unittest

# Determinar BASE_DIR
BASE_DIR = Path(__file__).resolve().parent

# NO establecer DJANGO_SETTINGS_MODULE
# Configurar Django manualmente para forzar SQLite en memoria
from django.conf import settings

# Configurar Django manualmente (sin usar settings.py)
# Esto evita que Django intente usar MySQL
if not settings.configured:
    settings.configure(
        DEBUG=True,
        BASE_DIR=BASE_DIR,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'TEST': {
                    'NAME': ':memory:',
                }
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
        AUTH_USER_MODEL='auth.User',
    )

# Inicializar Django
import django
django.setup()

print("⚙️ MODO TEST: SQLite en memoria configurado manualmente")
print(f"   Base de datos: {settings.DATABASES['default']['ENGINE']}")
print(f"   NAME: {settings.DATABASES['default']['NAME']}")

if __name__ == '__main__':
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar solo los tests que usan unittest.TestCase (ViewTest)
    # Estos NO requieren base de datos porque usan mocks
    suite.addTests(loader.loadTestsFromName('libros.tests.LibroViewTest'))
    suite.addTests(loader.loadTestsFromName('usuarios.tests.UsuarioViewTest'))
    suite.addTests(loader.loadTestsFromName('prestamos.tests.PrestamoViewTest'))
    
    print("=" * 70)
    print("🧪 EJECUTANDO TESTS UNITARIOS CON MOCKS (sin base de datos)")
    print("=" * 70)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)
