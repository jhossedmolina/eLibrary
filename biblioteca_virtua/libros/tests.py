from django.test import TestCase, Client
from django.urls import reverse
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
        self.libro = Libro.objects.create(
            titulo='1984',
            autor='George Orwell',
            año_publicacion=date(1949, 6, 8)
        )

    def test_listar_libros(self):
        response = self.client.get(reverse('libros:listar_libros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1984')
        self.assertTemplateUsed(response, 'libros/listar_libros.html')

    def test_detalle_libro(self):
        response = self.client.get(reverse('libros:detalle_libro', args=[self.libro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1984')
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    def test_registrar_libro_post_valido(self):
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': 'Cien años de soledad',
            'autor': 'Gabriel García Márquez',
            'año_publicacion': '1967-05-30'
        })
        self.assertEqual(response.status_code, 302) # Redirecciona tras éxito
        self.assertEqual(Libro.objects.count(), 2)

    def test_registrar_libro_post_invalido(self):
        response = self.client.post(reverse('libros:registrar_libro'), {
            'titulo': '', # Título vacío inválido
            'autor': 'Autor',
            'año_publicacion': '2023-01-01'
        })
        self.assertEqual(response.status_code, 200) # Se mantiene en la página mostrando errores
        self.assertEqual(Libro.objects.count(), 1) # No se crea nuevo libro

    def test_editar_libro(self):
        response = self.client.post(reverse('libros:editar_libro', args=[self.libro.id]), {
            'titulo': '1984 (Editado)',
            'autor': 'George Orwell',
            'año_publicacion': '1949-06-08'
        })
        self.assertEqual(response.status_code, 302)
        self.libro.refresh_from_db()
        self.assertEqual(self.libro.titulo, '1984 (Editado)')

    def test_eliminar_libro(self):
        response = self.client.post(reverse('libros:eliminar_libro', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Libro.objects.count(), 0)
