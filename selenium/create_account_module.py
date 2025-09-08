from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CreateAccountPage:
    def __init__(self, driver, username, email, password):
        self.driver = driver
        self.url = "http://127.0.0.1:8000/accounts/login/"
        self.username = username
        self.password = password
        self.email = email

    def open_login_page(self):
        """Abre a página de login"""
        self.driver.get(self.url)
        print("Página de login carregada")
        time.sleep(2)
        return True
    
    def click_on_create_account(self):
        try:
            create_account_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Create an account"))
            )   
            create_account_button.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível clicar na opção de criar conta")
            return False

    def fill_username_field(self):
        """Preenche o campo de Username"""
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_username"))
            )
            username_field.send_keys(self.username)
            time.sleep(1)
            return True
        except:
            print("Não foi possível preencher o campo de username")
            return False
        
    def fill_email_field(self):
        """Preenche o campo de Email"""
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_email"))
            )
            email_field.send_keys(self.email)
            time.sleep(1)
            return True
        except:
            print("Não foi possível preencher o campo de Email")
            return False
        
    def fill_password_field(self):
        """Preenche o campo de senha"""
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_password1"))
            )
            password_field.send_keys(self.password)
            time.sleep(1)
            return True
        except:
            print("Não foi possível preencher o campo de senha")
            return False
        
    def fill_confirm_password_field(self):
        """Preenche o campo de confirmação da senha"""
        try:
            confirm_password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_password2"))
            )
            confirm_password_field.send_keys(self.password)
            time.sleep(1)
            return True
        except:
            print("Não foi possível preencher o campo de confirmação de senha")
            return False
        
    def registry_account(self):
        """Clica no butão de registrar"""
        try:
            registry_account = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_password2"))
            )
            registry_account.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível preencher o campo de confirmação de senha")
            return False
        
    def perform_create_account(self):
        """Executa o fluxo completo de criar a conta"""
        if not self.open_login_page():
            return False
        if not self.click_on_create_account():
            return False
        if not self.fill_username_field():
            return False
        if not self.fill_email_field():
            return False
        if not self.fill_password_field():
            return False
        if not self.fill_confirm_password_field():
            return False
        time.sleep(1)
        return True