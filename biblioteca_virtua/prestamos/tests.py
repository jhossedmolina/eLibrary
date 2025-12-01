import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from .models import Prestamo
from usuarios.models import Usuario
from libros.models import Libro
from datetime import date
from django.utils import timezone

class PrestamoModelTest(TestCase):
    """Tests de modelo - requieren DB"""
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Juan Perez',
            correo='juan@example.com',
            edad=30
        )
        self.libro = Libro.objects.create(
            titulo='El Principito',
            autor='Antoine de Saint-Exupéry',
            año_publicacion=date(1943, 4, 6)
        )
        self.prestamo = Prestamo.objects.create(
            usuario=self.usuario,
            libro=self.libro
        )

    def test_prestamo_creacion(self):
        self.assertEqual(self.prestamo.usuario, self.usuario)
        self.assertEqual(self.prestamo.libro, self.libro)
        self.assertIsNotNone(self.prestamo.fecha_prestamo)
        self.assertIsNone(self.prestamo.fecha_devolucion)

    def test_prestamo_str(self):
        expected_str = f'{self.libro} prestado a {self.usuario} (Estado del libro: Prestado)'
        self.assertEqual(str(self.prestamo), expected_str)


class PrestamoViewTest(unittest.TestCase):
    """Tests de vistas - usan mocks, NO requieren DB"""
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    @patch('prestamos.models.Prestamo.objects')
    def test_listar_prestamos(self, mock_prestamo_objects):
        mock_prestamo = Mock(spec=Prestamo)
        mock_usuario = Mock(spec=Usuario)
        mock_usuario.nombre = 'Maria Lopez'
        mock_prestamo.usuario = mock_usuario
        mock_prestamo_objects.all.return_value = [mock_prestamo]
        
        response = self.client.get(reverse('prestamos:listar_prestamos'))
        self.assertEqual(response.status_code, 200)

    @patch('prestamos.models.Prestamo.objects')
    def test_detalle_prestamo(self, mock_prestamo_objects):
        mock_prestamo = Mock(spec=Prestamo)
        mock_prestamo.id = 1
        mock_usuario = Mock(spec=Usuario)
        mock_usuario.nombre = 'Maria Lopez'
        mock_prestamo.usuario = mock_usuario
        mock_prestamo_objects.get.return_value = mock_prestamo
        
        response = self.client.get(reverse('prestamos:detalle_prestamo', args=[1]))
        self.assertEqual(response.status_code, 200)

    @patch('prestamos.forms.PrestamoForm')
    def test_registrar_prestamo_post_valido(self, mock_form_class):
        mock_form = MagicMock()
        mock_form.is_valid.return_value = True
        mock_prestamo = Mock(spec=Prestamo)
        mock_form.save.return_value = mock_prestamo
        mock_form_class.return_value = mock_form
        
        response = self.client.post(reverse('prestamos:registrar_prestamo'), {
            'usuario': 1,
            'libro': 1
        })
        self.assertEqual(response.status_code, 302)

    @patch('prestamos.models.Prestamo.objects')
    def test_registrar_devolucion(self, mock_prestamo_objects):
        mock_prestamo = Mock(spec=Prestamo)
        mock_prestamo.id = 1
        mock_prestamo.fecha_devolucion = None
        mock_prestamo_objects.get.return_value = mock_prestamo
        
        response = self.client.post(reverse('prestamos:registrar_devolucion', args=[1]))
        self.assertEqual(response.status_code, 302)

    @patch('prestamos.models.Prestamo.objects')
    def test_eliminar_prestamo(self, mock_prestamo_objects):
        mock_prestamo = Mock(spec=Prestamo)
        mock_prestamo.id = 1
        mock_prestamo_objects.get.return_value = mock_prestamo
        
        response = self.client.post(reverse('prestamos:eliminar_prestamo', args=[1]))
        self.assertEqual(response.status_code, 302)
        mock_prestamo.delete.assert_called_once()

