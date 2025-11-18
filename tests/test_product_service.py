"""
Tests para product_service
"""
import pytest
from src.services import product_service
from src.schemas.product_input import ProductInput
from src.repositories import product_repository, store_repository, product_store_repository


@pytest.mark.unit
class TestProductService:
    """Tests para el servicio de procesamiento de productos"""
    
    def test_process_new_product(self, db_session):
        """Test procesar un producto nuevo"""
        # Crear producto input
        product_input = ProductInput(
            product_id=1,
            store_id="1|2",
            title="New Product",
            price=19.99
        )
        
        # Procesar producto
        product_service.process_one_product(db_session, product_input)
        db_session.commit()
        
        # Verificar que se creó el producto
        product_db = product_repository.get_product(db_session, 1)
        assert product_db is not None
        assert product_db.title == "New Product"
        assert product_db.price == 19.99
        
        # Verificar que se crearon las tiendas
        store1 = store_repository.get_store(db_session, 1)
        store2 = store_repository.get_store(db_session, 2)
        assert store1 is not None
        assert store2 is not None
        
        # Verificar que se crearon las relaciones
        product_stores = product_store_repository.get_product_stores(db_session, 1)
        assert len(product_stores) == 2
        store_ids = {ps.store_id for ps in product_stores}
        assert store_ids == {1, 2}
    
    def test_process_existing_product_no_changes(self, db_session):
        """Test procesar un producto existente sin cambios"""
        # Crear producto existente
        product_repository.create_product(db_session, 1, "Existing Product", 19.99)
        store_repository.create_store(db_session, 1)
        product_store_repository.add_product_store(db_session, 1, 1)
        db_session.commit()
        
        # Crear producto input con mismos datos
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="Existing Product",
            price=19.99
        )
        
        # Procesar producto
        product_service.process_one_product(db_session, product_input)
        db_session.commit()
        
        # Verificar que no cambió
        product_db = product_repository.get_product(db_session, 1)
        assert product_db.title == "Existing Product"
        assert product_db.price == 19.99
    
    def test_process_existing_product_with_changes(self, db_session):
        """Test procesar un producto existente con cambios"""
        # Crear producto existente
        product_repository.create_product(db_session, 1, "Old Title", 19.99)
        store_repository.create_store(db_session, 1)
        product_store_repository.add_product_store(db_session, 1, 1)
        db_session.commit()
        
        # Crear producto input con datos modificados
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="New Title",
            price=29.99
        )
        
        # Procesar producto
        product_service.process_one_product(db_session, product_input)
        db_session.commit()
        
        # Verificar que se actualizó
        product_db = product_repository.get_product(db_session, 1)
        assert product_db.title == "New Title"
        assert product_db.price == 29.99
    
    def test_sync_product_stores_add_stores(self, db_session):
        """Test añadir tiendas a un producto existente"""
        # Crear producto con una tienda
        product_repository.create_product(db_session, 1, "Product", 19.99)
        store_repository.create_store(db_session, 1)
        product_store_repository.add_product_store(db_session, 1, 1)
        db_session.commit()
        
        # Procesar con más tiendas
        product_input = ProductInput(
            product_id=1,
            store_id="1|2|3",
            title="Product",
            price=19.99
        )
        
        product_service.process_one_product(db_session, product_input)
        db_session.commit()
        
        # Verificar que se añadieron las tiendas
        product_stores = product_store_repository.get_product_stores(db_session, 1)
        assert len(product_stores) == 3
        store_ids = {ps.store_id for ps in product_stores}
        assert store_ids == {1, 2, 3}
    
    def test_sync_product_stores_remove_stores(self, db_session):
        """Test eliminar tiendas de un producto existente"""
        # Crear producto con tres tiendas
        product_repository.create_product(db_session, 1, "Product", 19.99)
        store_repository.create_store(db_session, 1)
        store_repository.create_store(db_session, 2)
        store_repository.create_store(db_session, 3)
        product_store_repository.add_product_store(db_session, 1, 1)
        product_store_repository.add_product_store(db_session, 1, 2)
        product_store_repository.add_product_store(db_session, 1, 3)
        db_session.commit()
        
        # Procesar con menos tiendas
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="Product",
            price=19.99
        )
        
        product_service.process_one_product(db_session, product_input)
        db_session.commit()
        
        # Verificar que se eliminaron las tiendas
        product_stores = product_store_repository.get_product_stores(db_session, 1)
        assert len(product_stores) == 1
        assert product_stores[0].store_id == 1
    
    def test_is_product_changed_title(self, db_session):
        """Test detectar cambio en título"""
        product = product_repository.create_product(db_session, 1, "Old Title", 19.99)
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="New Title",
            price=19.99
        )
        
        assert product_service._is_product_changed(product, product_input) is True
    
    def test_is_product_changed_price(self, db_session):
        """Test detectar cambio en precio"""
        product = product_repository.create_product(db_session, 1, "Title", 19.99)
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="Title",
            price=29.99
        )
        
        assert product_service._is_product_changed(product, product_input) is True
    
    def test_is_product_not_changed(self, db_session):
        """Test detectar cuando no hay cambios"""
        product = product_repository.create_product(db_session, 1, "Title", 19.99)
        product_input = ProductInput(
            product_id=1,
            store_id="1",
            title="Title",
            price=19.99
        )
        
        assert product_service._is_product_changed(product, product_input) is False
