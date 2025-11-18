"""
Tests para product_repository
"""
import pytest
from src.repositories import product_repository
from src.db.models.product import Product


@pytest.mark.unit
class TestProductRepository:
    """Tests para las operaciones del repositorio de productos"""
    
    def test_create_product(self, db_session):
        """Test crear un producto en la base de datos"""
        product = product_repository.create_product(
            db_session,
            product_id=1,
            title="Test Product",
            price=19.99
        )
        
        assert product.product_id == 1
        assert product.title == "Test Product"
        assert product.price == 19.99
        
        # Verificar que se puede recuperar de la DB
        db_product = product_repository.get_product(db_session, 1)
        assert db_product is not None
        assert db_product.product_id == 1
    
    def test_get_product_existing(self, db_session):
        """Test obtener un producto existente"""
        # Crear producto
        product_repository.create_product(
            db_session,
            product_id=1,
            title="Test Product",
            price=19.99
        )
        
        # Recuperar producto
        product = product_repository.get_product(db_session, 1)
        assert product is not None
        assert product.product_id == 1
        assert product.title == "Test Product"
    
    def test_get_product_non_existing(self, db_session):
        """Test obtener un producto que no existe"""
        product = product_repository.get_product(db_session, 999)
        assert product is None
    
    def test_update_product(self, db_session):
        """Test actualizar un producto"""
        # Crear producto
        product = product_repository.create_product(
            db_session,
            product_id=1,
            title="Original Title",
            price=19.99
        )
        
        # Actualizar producto
        updated_product = product_repository.update_product(
            product,
            title="Updated Title",
            price=29.99
        )
        
        assert updated_product.title == "Updated Title"
        assert updated_product.price == 29.99
        
        # Verificar que el cambio persiste
        db_product = product_repository.get_product(db_session, 1)
        assert db_product.title == "Updated Title"
        assert db_product.price == 29.99
    
    def test_delete_product(self, db_session):
        """Test eliminar un producto"""
        # Crear producto
        product = product_repository.create_product(
            db_session,
            product_id=1,
            title="Test Product",
            price=19.99
        )
        db_session.commit()
        
        # Verificar que existe
        assert product_repository.get_product(db_session, 1) is not None
        
        # Eliminar producto
        product_repository.delete_product(db_session, product)
        db_session.commit()
        
        # Verificar que ya no existe
        assert product_repository.get_product(db_session, 1) is None
    
    def test_get_all_products(self, db_session):
        """Test obtener todos los productos"""
        # Crear varios productos
        product_repository.create_product(db_session, 1, "Product 1", 10.0)
        product_repository.create_product(db_session, 2, "Product 2", 20.0)
        product_repository.create_product(db_session, 3, "Product 3", 30.0)
        
        # Obtener todos
        products = product_repository.get_all_products(db_session)
        
        assert len(products) == 3
        assert all(isinstance(p, Product) for p in products)
        product_ids = {p.product_id for p in products}
        assert product_ids == {1, 2, 3}
    
    def test_get_all_products_empty(self, db_session):
        """Test obtener todos los productos cuando no hay ninguno"""
        products = product_repository.get_all_products(db_session)
        assert products == []
