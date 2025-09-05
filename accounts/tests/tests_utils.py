# accounts/tests/test_utils.py

from django.test import TestCase
from ..utils import custom_slugify

class UtilsTest(TestCase):
    """Test suite for utility functions in the accounts app."""

    def test_custom_slugify_with_email(self):
        """
        Verifica se a função slugify converte um e-mail corretamente,
        substituindo '@' e '.' por hífens.
        """
        email = 'exemplo.teste@meu-site.com'
        expected_slug = 'exemplo-teste-meu-site-com'
        result = custom_slugify(email)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_regular_string(self):
        """
        Verifica se a função funciona como o slugify padrão do Django
        para strings sem '@' ou '.'.
        """
        text = 'Um Título Com Espaços e Ç'
        expected_slug = 'um-titulo-com-espacos-e-c'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_no_special_chars(self):
        """Verifica o comportamento com uma string que não precisa de alteração."""
        text = 'jasilva'
        expected_slug = 'jasilva'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_mixed_chars(self):
        """Verifica uma mistura de caracteres especiais."""
        text = 'nome.sobrenome@empresa_CORPORATIVA.com'
        expected_slug = 'nome-sobrenome-empresa-corporativa-com'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)