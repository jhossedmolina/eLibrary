from django.test import TestCase, Client
from django.urls import reverse
from .models import Prestamo
from usuarios.models import Usuario
from libros.models import Libro
from datetime import date
from django.utils import timezone

class PrestamoModelTest(TestCase):
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

class PrestamoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre='Maria Lopez',
            correo='maria@example.com',
            edad=25
        )
        self.libro = Libro.objects.create(
            titulo='1984',
            autor='George Orwell',
            año_publicacion=date(1949, 6, 8)
        )
        self.prestamo = Prestamo.objects.create(
            usuario=self.usuario,
            libro=self.libro
        )

    def test_listar_prestamos(self):
        response = self.client.get(reverse('prestamos:listar_prestamos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Lopez')
        self.assertTemplateUsed(response, 'prestamos/listar_prestamos.html')

    def test_detalle_prestamo(self):
        response = self.client.get(reverse('prestamos:detalle_prestamo', args=[self.prestamo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Lopez')
        self.assertTemplateUsed(response, 'prestamos/detalle_prestamo.html')

    def test_registrar_prestamo_post_valido(self):
        libro_disponible = Libro.objects.create(
            titulo='Libro Disponible',
            autor='Autor X',
            año_publicacion=date(2020, 1, 1)
        )
        response = self.client.post(reverse('prestamos:registrar_prestamo'), {
            'usuario': self.usuario.id,
            'libro': libro_disponible.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prestamo.objects.count(), 2)

    def test_registrar_devolucion(self):
        response = self.client.post(reverse('prestamos:registrar_devolucion', args=[self.prestamo.id]))
        self.assertEqual(response.status_code, 302)
        self.prestamo.refresh_from_db()
        self.assertIsNotNone(self.prestamo.fecha_devolucion)

    def test_eliminar_prestamo(self):
        response = self.client.post(reverse('prestamos:eliminar_prestamo', args=[self.prestamo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prestamo.objects.count(), 0)
