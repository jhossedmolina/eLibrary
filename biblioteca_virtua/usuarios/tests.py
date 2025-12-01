from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Juan Perez',
            correo='juan@example.com',
            edad=30
        )

    def test_usuario_creacion(self):
        self.assertEqual(self.usuario.nombre, 'Juan Perez')
        self.assertEqual(self.usuario.correo, 'juan@example.com')
        self.assertEqual(self.usuario.edad, 30)
        self.assertTrue(self.usuario.activo)

    def test_usuario_str(self):
        self.assertEqual(str(self.usuario), 'Juan Perez (juan@example.com)')

class UsuarioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre='Maria Lopez',
            correo='maria@example.com',
            edad=25
        )

    def test_registrar_usuario_post_valido(self):
        response = self.client.post(reverse('usuarios:registrar_usuario'), {
            'nombre': 'Carlos Ruiz',
            'correo': 'carlos@example.com',
            'edad': 40
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Usuario.objects.count(), 2)

    def test_registrar_usuario_post_invalido(self):
        response = self.client.post(reverse('usuarios:registrar_usuario'), {
            'nombre': '',
            'correo': 'invalid-email',
            'edad': -5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_confirmacion_usuario(self):
        response = self.client.get(reverse('usuarios:confirmacion_usuario', args=[self.usuario.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Lopez')
        self.assertTemplateUsed(response, 'usuarios/confirmacion.html')
