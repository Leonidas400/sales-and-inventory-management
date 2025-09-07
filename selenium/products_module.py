from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Product_Registration:
    def __init__(self, driver):
        self.driver = driver
    
    def find_dropdown_products(self):
        """Encontra e clica no Dropdown de products"""
        try:
            products_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "productsDropdown"))
            )
            products_dropdown.click()
            return True
        except:
            print("Não foi possível encontrar o dropdown de products")
            return False

    def find_products_button(self):
        """Encontra e clica no botão de All Products"""
        try:
            products_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "All Products"))
            )
            products_button.click()
            return True
        except:
            print("Não foi possível encontrar o botão de 'All products'")
            return False

    def find_AddItem_button(self):
        """Encontra e clica no botão de adicionar item"""
        try:
            add_item_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.btn-sm.rounded-pill.shadow-sm"))
            )
            add_item_button.click()
            return True
        except:
            print("Não foi possível encontrar o botão de 'Add item'")
            return False
    
    def find_AddItem_button(self):
        """Encontra e clica no botão de adicionar item"""
        try:
            add_item_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success.btn-sm.rounded-pill.shadow-sm"))
            )
            add_item_button.click()
            return True
        except:
            print("Não foi possível encontrar o botão de 'Add item'")
            return False

    def registry_item(self):
        # Encontra e preenche o campo de product name
        product_name = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_name"))
        )
        product_name.send_keys("Produto teste")
        time.sleep(1)

        # Encontra e preenche o campo de category
        category_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_category"))
        )
        time.sleep(1)

        # Encontra e preenche o campo de description
        description_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_description"))
        )
        description_button.send_keys("Teste teste teste")
        time.sleep(1)

        # Encontra e preenche o campo de quantity
        quantity_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_quantity"))
        )
        quantity_button.send_keys("1")
        time.sleep(1)

        # Encontra e preenche o campo de price
        price_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_price"))
        )
        price_button.send_keys("1")
        time.sleep(1)

        # Encontra e preenche o campo de selling price
        selling_price = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_expiring_date"))
        )
        selling_price.send_keys("01/01/2025")
        time.sleep(1)

        # Encontra e preenche o campo de expiring date
        expiring_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_expiring_date"))
        )
        expiring_button.send_keys("01/01/2025")
        time.sleep(1)

        # CLica no botão de Submit para cadastrar um produto
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "btn btn-success btn-lg"))
        )
        submit_button.submit()
        time.sleep(1)

    def perform_registry(self):
        """Executa o fluxo completo de cadastro de produto"""
        try:
            if self.find_dropdown_products():
                time.sleep(1)
                if self.find_products_button():
                    time.sleep(1)
                    if self.find_AddItem_button():
                        time.sleep(1)
                        if self.registry_item():
                            time.sleep(1)
                            print("Produto cadastrado com sucesso!")
                            return True
            return False
        except Exception as e:
            print(f"Erro durante o cadastro: {e}")
            return False