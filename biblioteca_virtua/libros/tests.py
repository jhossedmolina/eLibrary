from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import Mock, patch, MagicMock
from .models import Libro
from datetime import date

class LibroModelTest(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(
            titulo='El Principito',
            autor='Antoine de Saint-Exupéry',
            año_publicacion=date(1943, 4, 6)
        )

    def test_libro_creacion(self):
        self.assertEqual(self.libro.titulo, 'El Principito')
        self.assertEqual(self.libro.autor, 'Antoine de Saint-Exupéry')
        self.assertEqual(self.libro.año_publicacion, date(1943, 4, 6))

    def test_libro_str(self):
        self.assertEqual(str(self.libro), 'El Principito (Antoine de Saint-Exupéry)')

class LibroViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('libros.models.Libro.objects')
    def test_listar_libros(self, mock_libro_objects):
        mock_libro = Mock(spec=Libro)
        mock_libro.titulo = '1984'
        mock_libro.autor = 'George Orwell'
        mock_libro_objects.all.return_value = [mock_libro]
        
        response = self.client.get(reverse('libros:listar_libros'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/listar_libros.html')

    @patch('libros.models.Libro.objects')
    def test_detalle_libro(self, mock_libro_objects):
        mock_libro = Mock(spec=Libro)
        mock_libro.id = 1
        mock_libro.titulo = '1984'
        mock_libro_objects.get.return_value = mock_libro
        
        response = self.client.get(reverse('libros:detalle_libro', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    @patch('libros.forms.LibroForm.is_valid')
    @patch('libros.forms.LibroForm.save')
    def test_registrar_libro_post_valido(self, mock_save, mock_is_valid):
        mock_is_valid.return_value = True
        mock_libro = Mock(spec=Libro)
        mock_save.return_value = mock_libro
        
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': 'Cien años de soledad',
            'autor': 'Gabriel García Márquez',
            'año_publicacion': '1967-05-30'
        })
        self.assertEqual(response.status_code, 302)

    @patch('libros.forms.LibroForm.is_valid')
    def test_registrar_libro_post_invalido(self, mock_is_valid):
        mock_is_valid.return_value = False
        
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': '',
            'autor': 'Autor',
            'año_publicacion': '2023-01-01'
        })
        self.assertEqual(response.status_code, 200)

    @patch('libros.models.Libro.objects')
    @patch('libros.forms.LibroForm.is_valid')
    @patch('libros.forms.LibroForm.save')
    def test_editar_libro(self, mock_save, mock_is_valid, mock_libro_objects):
        mock_libro = Mock(spec=Libro)
        mock_libro.id = 1
        mock_libro_objects.get.return_value = mock_libro
        mock_is_valid.return_value = True
        
        response = self.client.post(reverse('libros:editar_libro', args=[1]), {
            'titulo': '1984 (Editado)',
            'autor': 'George Orwell',
            'año_publicacion': '1949-06-08'
        })
        self.assertEqual(response.status_code, 302)

    @patch('libros.models.Libro.objects')
    def test_eliminar_libro(self, mock_libro_objects):
        mock_libro = Mock(spec=Libro)
        mock_libro.id = 1
        mock_libro_objects.get.return_value = mock_libro
        
        response = self.client.post(reverse('libros:eliminar_libro', args=[1]))
        self.assertEqual(response.status_code, 302)
        mock_libro.delete.assert_called_once()
