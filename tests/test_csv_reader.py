"""
Tests para csv_reader service
"""
import pytest
from pathlib import Path
from src.services import csv_reader
from src.schemas.product_input import ProductInput


@pytest.mark.unit
class TestCSVReader:
    """Tests para el servicio de lectura de CSV"""
    
    def test_read_products_from_csv_valid(self, tmp_path):
        """Test leer productos de un CSV válido"""
        # Crear archivo CSV temporal
        csv_file = tmp_path / "products.csv"
        csv_content = """product_id,store_id,title,price
1,1|2,Product 1,19.99
2,3,Product 2,29.99
3,1|2|3,Product 3,39.99"""
        csv_file.write_text(csv_content)
        
        # Leer productos
        products = csv_reader.read_products_from_csv(csv_file)
        
        # Verificar resultados
        assert len(products) == 3
        assert all(isinstance(p, ProductInput) for p in products)
        
        # Verificar primer producto
        assert products[0].product_id == 1
        assert products[0].store_id == {1, 2}
        assert products[0].title == "Product 1"
        assert products[0].price == 19.99
        
        # Verificar segundo producto
        assert products[1].product_id == 2
        assert products[1].store_id == {3}
        assert products[1].title == "Product 2"
        
        # Verificar tercer producto
        assert products[2].product_id == 3
        assert products[2].store_id == {1, 2, 3}
    
    def test_read_products_from_csv_with_invalid_rows(self, tmp_path):
        """Test leer CSV con filas inválidas (deben ser omitidas)"""
        # Crear archivo CSV con una fila inválida
        csv_file = tmp_path / "products.csv"
        csv_content = """product_id,store_id,title,price
1,1,Valid Product,19.99
2,abc,Invalid Store,29.99
3,2,Another Valid,39.99"""
        csv_file.write_text(csv_content)
        
        # Leer productos
        products = csv_reader.read_products_from_csv(csv_file)
        
        # Solo los productos válidos deben ser retornados
        assert len(products) == 2
        assert products[0].product_id == 1
        assert products[1].product_id == 3
    
    def test_read_products_from_csv_empty_file(self, tmp_path):
        """Test leer un CSV vacío"""
        # Crear archivo CSV vacío
        csv_file = tmp_path / "products.csv"
        csv_content = """product_id,store_id,title,price"""
        csv_file.write_text(csv_content)
        
        # Leer productos
        products = csv_reader.read_products_from_csv(csv_file)
        
        # No debe haber productos
        assert len(products) == 0
    
    def test_read_products_from_csv_file_not_found(self, tmp_path):
        """Test leer un archivo que no existe"""
        # Intentar leer archivo inexistente
        non_existent_file = tmp_path / "non_existent.csv"
        products = csv_reader.read_products_from_csv(non_existent_file)
        
        # Debe retornar lista vacía
        assert products == []
    
    def test_read_products_from_csv_with_invalid_price(self, tmp_path):
        """Test leer CSV con precio inválido"""
        # Crear archivo CSV con precio inválido
        csv_file = tmp_path / "products.csv"
        csv_content = """product_id,store_id,title,price
1,1,Product 1,19.99
2,2,Product 2,-5.00
3,3,Product 3,29.99"""
        csv_file.write_text(csv_content)
        
        # Leer productos
        products = csv_reader.read_products_from_csv(csv_file)
        
        # Solo los productos válidos deben ser retornados (precio negativo es inválido)
        assert len(products) == 2
        assert products[0].product_id == 1
        assert products[1].product_id == 3
    
    def test_read_products_from_csv_with_empty_title(self, tmp_path):
        """Test leer CSV con título vacío"""
        # Crear archivo CSV con título vacío
        csv_file = tmp_path / "products.csv"
        csv_content = """product_id,store_id,title,price
1,1,Valid Product,19.99
2,2,   ,29.99
3,3,Another Valid,39.99"""
        csv_file.write_text(csv_content)
        
        # Leer productos
        products = csv_reader.read_products_from_csv(csv_file)
        
        # Solo los productos válidos deben ser retornados
        assert len(products) == 2
        assert products[0].product_id == 1
        assert products[1].product_id == 3
