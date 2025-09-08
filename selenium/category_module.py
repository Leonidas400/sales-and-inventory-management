from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CategoryPage:
    def __init__(self, driver):
        self.driver = driver

    def find_dropdown_products(self):
        """Encontra e clica no Dropdown de products"""
        try:
            products_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "productsDropdown"))
            )
            products_dropdown.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível encontrar o dropdown de products")
            return False
        
    def find_categories_button(self):
        """Encontra e clica no botão de Categories"""
        try:
            categories_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dropdown-item.text-light[href='/categories/']"))
            )
            categories_button.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível encontrar o botão de 'Categories")
            return False
        
    def add_categories_button(self):
        """Encontra e clica no botão de Add Category"""
        try:
            categories_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-success[href='/categories/create/']"))
            )
            categories_button.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível encontrar o botão de 'Add Categories'")
            return False
        
    #id_name
    def enter_category_name(self):
        """Adicionar uma categoria"""
        try:
            categories_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id_name"))
            )
            categories_button.send_keys("LIVROS")
            time.sleep(1)
            return True
        except:
            print("Não foi possível adicionar o nome da categoria'")
            return False
        
    def save_category(self):
        """Salvar categorias"""
        try:
            categories_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success"))
            )
            categories_button.click()
            time.sleep(1)
            return True
        except:
            print("Não foi possível salvar essa categoria")
            return False
        
    def perform_registry_category(self):
        """Fluxo completo para cadastrar uma categoria"""
        if not self.find_dropdown_products():
            return False
        if not self.find_categories_button():
            return False
        if not self.add_categories_button():
            return False
        if not self.enter_category_name():
            return False
        if not self.save_category():
            return False
        time.sleep(2)
        return True