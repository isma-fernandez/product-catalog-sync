"""
Tests para el schema ProductInput
"""
import pytest
from pydantic import ValidationError
from src.schemas.product_input import ProductInput


@pytest.mark.unit
class TestProductInput:
    """Tests para la validación de ProductInput"""
    
    def test_valid_product_single_store(self):
        """Test con un producto válido con una sola tienda"""
        product = ProductInput(
            product_id=1,
            store_id="1",
            title="Test Product",
            price=19.99
        )
        assert product.product_id == 1
        assert product.store_id == {1}
        assert product.title == "Test Product"
        assert product.price == 19.99
    
    def test_valid_product_multiple_stores(self):
        """Test con un producto válido con múltiples tiendas"""
        product = ProductInput(
            product_id=2,
            store_id="1|2|3",
            title="Multi-Store Product",
            price=29.99
        )
        assert product.product_id == 2
        assert product.store_id == {1, 2, 3}
        assert product.title == "Multi-Store Product"
        assert product.price == 29.99
    
    def test_invalid_negative_product_id(self):
        """Test con product_id negativo debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=-1,
                store_id="1",
                title="Test",
                price=10.0
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("product_id",) for error in errors)
    
    def test_invalid_empty_title(self):
        """Test con título vacío debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=1,
                store_id="1",
                title="   ",
                price=10.0
            )
        errors = exc_info.value.errors()
        assert any("title" in error["loc"] for error in errors)
    
    def test_invalid_zero_price(self):
        """Test con precio cero debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=1,
                store_id="1",
                title="Test",
                price=0
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("price",) for error in errors)
    
    def test_invalid_negative_price(self):
        """Test con precio negativo debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=1,
                store_id="1",
                title="Test",
                price=-5.0
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("price",) for error in errors)
    
    def test_invalid_store_id_format(self):
        """Test con formato inválido de store_id debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=1,
                store_id="abc",
                title="Test",
                price=10.0
            )
        errors = exc_info.value.errors()
        assert any("store_id" in error["loc"] for error in errors)
    
    def test_invalid_store_id_with_spaces(self):
        """Test con espacios en store_id debe fallar"""
        with pytest.raises(ValidationError) as exc_info:
            ProductInput(
                product_id=1,
                store_id="1 | 2",
                title="Test",
                price=10.0
            )
        errors = exc_info.value.errors()
        assert any("store_id" in error["loc"] for error in errors)
    
    def test_str_representation(self):
        """Test de la representación en string del producto"""
        product = ProductInput(
            product_id=1,
            store_id="1|2",
            title="Test Product",
            price=19.99
        )
        str_repr = str(product)
        assert "Test Product" in str_repr
        assert "1" in str_repr
        assert "19.99" in str_repr
