from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:8000/accounts/login/"
    
    def open_login_page(self):
        """Abre a página de login"""
        self.driver.get(self.url)
        print("Página de login carregada")
    
    def enter_username(self, username):
        """Preenche o campo de usuário"""
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys(username)
        time.sleep(1)
        print("Username preenchido")
    
    def enter_password(self, password):
        """Preenche o campo de senha"""
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys(password)
        time.sleep(1)
        print("Password preenchido")
    
    def click_login_button(self):
        """Clica no botão de login"""
        login_button = self.driver.find_element(By.XPATH, "//button[@name='button']")
        login_button.click()
        time.sleep(2)
        print("Botão de login clicado")
    
    def perform_login(self, username, password):
        """Executa o fluxo completo de login"""
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        print("Login realizado com sucesso!")