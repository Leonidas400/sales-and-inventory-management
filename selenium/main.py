from selenium import webdriver
from login_module import LoginPage
from logout_module import LogoutPage
from products_module import Product_Registration
import time

class TestAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.logout_page = LogoutPage(self.driver)
        self.products_page = Product_Registration(self.driver)
    
    def run_test(self):
        """Executa o teste completo"""
        try:
            # Dados de login
            username = "ian.teixeira__"
            password = "123456@I"
            
            # Realizar login
            self.login_page.perform_login(username, password)
            
            # Aguardar um pouco após login
            time.sleep(3)
            
            # Realizar cadastro de um produto
            self.products_page.perform_registry()

            # Aguardar um pouco após cadastro do produto
            time.sleep(3)

            # Realizar logout
            self.logout_page.perform_logout()
            
            # Manter aberto para visualização
            time.sleep(3)
            
        except Exception as e:
            print(f"Erro durante execução: {e}")
        
        finally:
            self.driver.quit()
            print("Navegador fechado")

if __name__ == "__main__":
    test = TestAutomation()
    test.run_test()