from django.test import TestCase
from ..utils import custom_slugify

class UtilsTest(TestCase):

    def test_custom_slugify_with_email(self):
        email = 'jorge.teste@site.com'
        expected_slug = 'jorge-teste-site-com'
        result = custom_slugify(email)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_regular_string(self):
        text = 'Um Título muito criativo Com Espaços e Ç'
        expected_slug = 'um-titulo-muito-criativo-com-espacos-e-c'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_no_special_chars(self):
        text = 'josilva'
        expected_slug = 'josilva'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)

    def test_custom_slugify_with_mixed_chars(self):
        text = 'junin.robo@empresa_COORPORATIVA.com'
        expected_slug = 'junin-robo-empresa-coorporativa-com'
        result = custom_slugify(text)
        self.assertEqual(result, expected_slug)