from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
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

    def registry_item(self):
        """Encontra e preenche o campo de product name"""
        product_name = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_name"))
        )
        product_name.send_keys("Produto teste")
        time.sleep(1)

        """Encontra e preenche o campo de category"""
        category_button = Select(self.driver.find_element(By.NAME, "category"))
        category_button.select_by_visible_text("Category: LIVROS")
        time.sleep(1)

        """Encontra e preenche o campo de description"""
        description_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_description"))
        )
        description_button.send_keys("Teste teste teste")
        time.sleep(1)

        """Encontra e preenche o campo de quantity"""
        quantity_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_quantity"))
        )
        quantity_button.send_keys("1")
        time.sleep(1)

        """Encontra e preenche o campo de selling price"""
        price_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_price"))
        )
        price_button.send_keys("1")
        time.sleep(1)

        """Encontra e preenche o campo de expiring date"""
        # Espera o elemento estar clicável
        expiring_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "id_expiring_date"))
        )
        expiring_button.send_keys("01012025")
        expiring_button.send_keys(Keys.ARROW_RIGHT)
        expiring_button.send_keys("1900")
        time.sleep(1)

        """CLica no botão de Vendor para selecionar um fornecedor"""
        vendor_select = Select(self.driver.find_element(By.ID, "id_vendor"))
        vendor_select.select_by_visible_text("Pedro Augusto")
        time.sleep(1)

        """CLica no botão de Submit para cadastrar um produto"""
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-success') and text()[contains(., 'Submit')]]"))
        )
        submit_button.click()
        time.sleep(1)

        return True   

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