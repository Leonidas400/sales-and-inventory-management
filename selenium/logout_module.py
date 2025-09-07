from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver

    def find_logout_button_css(self):
        """Encontra o botão de logout por CSS Selector"""
        try:
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-danger"))
            )
            return logout_button
        except:
            return None
    
    def find_logout_button_xpath(self):
        """Encontra o botão de logout por XPath (alternativa)"""
        try:
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Logout')]"))
            )
            return logout_button
        except:
            return None
    
    def click_logout(self):
        """Clica no botão de logout"""
        # Tentar primeiro por CSS
        logout_button = self.find_logout_button_css()
        
        # Se não encontrar, tentar por XPath
        if not logout_button:
            logout_button = self.find_logout_button_xpath()
        
        if logout_button:
            logout_button.click()
            time.sleep(2)
            print("Logout realizado com sucesso!")
            return True
        else:
            print("Não foi possível encontrar o botão de logout")
            return False
    
    def perform_logout(self):
        """Executa o fluxo completo de logout"""
        return self.click_logout()