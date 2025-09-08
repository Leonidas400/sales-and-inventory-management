import pytest
from selenium import webdriver
from login_module import LoginPage
from logout_module import LogoutPage
from products_module import Product_Registration
from category_module import CategoryPage
from create_account_module import CreateAccountPage
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

    def test_create_account(self):
        """Testa o cadastro de uma conta"""
        global create_account
        create_account = CreateAccountPage(self.driver, "Usuario_Teste_01", "emaildousuario01@gmail.com", "123456@I")
        # Espera ou verifica algo que indique que a conta foi criada
        assert create_account.perform_create_account() is True, "Falha ao cadastrar uma conta"
        print("Cadastro de categoria testado com sucesso")
        time.sleep(3)

    def test_login(self):
        """Testa o login no sistema"""
        username = create_account.username
        password = create_account.password

        login_page = LoginPage(self.driver)
        login_page.perform_login("ian.teixeira__", "123456@I")
        # Espera ou verifica algo que indique login bem-sucedido
        assert "Dashboard" in self.driver.title or "Produtos" in self.driver.page_source
        print("Login testado com sucesso")

    def test_category_registration(self):
        """Testa o cadastro de uma categoria"""
        category_page = CategoryPage(self.driver)
        # Espera ou verifica algo que indique que a categoria foi salva
        assert category_page.perform_registry_category() is True, "Falha ao salvar a categoria"
        print("Cadastro de categoria testado com sucesso")

    def test_product_registration(self):
        """Testa o cadastro de um produto"""
        products_page = Product_Registration(self.driver)
        # Assumindo que o usuário já está logado
        result = products_page.perform_registry()
        assert result is True, "Falha ao tentar registrar um produto"
        print("Cadastro de produto testado com sucesso")

    def test_logout(self):
        """Testa o logout do sistema"""
        logout_page = LogoutPage(self.driver)
        result = logout_page.perform_logout()
        assert result is True, "Falha ao tentar dar logout"