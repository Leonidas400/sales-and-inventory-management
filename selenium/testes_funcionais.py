import pytest
from selenium import webdriver
from login_module import LoginPage
from logout_module import LogoutPage
from products_module import Product_Registration
import time

@pytest.fixture(scope="class")
def setup(request):
    """Fixture para inicializar e finalizar o navegador"""
    driver = webdriver.Chrome()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestFunctional:

    def test_login(self):
        """Testa o login no sistema"""
        login_page = LoginPage(self.driver)
        login_page.perform_login("ian.teixeira__", "123456@I")
        # Espera ou verifica algo que indique login bem-sucedido
        assert "Dashboard" in self.driver.title or "Produtos" in self.driver.page_source
        print("Login testado com sucesso")

    def test_product_registration(self):
        """Testa o cadastro de um produto"""
        products_page = Product_Registration(self.driver)
        # Assumindo que o usuário já está logado
        result = products_page.perform_registry()
        assert result is True
        print("Cadastro de produto testado com sucesso")

    def test_logout(self):
        """Testa o logout do sistema"""
        logout_page = LogoutPage(self.driver)
        result = logout_page.perform_logout()
        assert result is True