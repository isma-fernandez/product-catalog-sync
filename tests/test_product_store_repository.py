"""
Tests para product_store_repository
"""
import pytest
from src.repositories import product_repository, store_repository, product_store_repository


@pytest.mark.unit
class TestProductStoreRepository:
    """Tests para las operaciones del repositorio de relaciones producto-tienda"""
    
    def test_add_product_store(self, db_session):
        """Test añadir una relación producto-tienda"""
        # Crear producto y tienda
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        store = store_repository.create_store(db_session, 1)
        db_session.commit()
        
        # Añadir relación
        product_store = product_store_repository.add_product_store(
            db_session, product.product_id, store.store_id
        )
        
        assert product_store.product_id == 1
        assert product_store.store_id == 1
    
    def test_get_product_stores(self, db_session):
        """Test obtener todas las tiendas de un producto"""
        # Crear producto y tiendas
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        store1 = store_repository.create_store(db_session, 1)
        store2 = store_repository.create_store(db_session, 2)
        store3 = store_repository.create_store(db_session, 3)
        db_session.commit()
        
        # Añadir relaciones
        product_store_repository.add_product_store(db_session, 1, 1)
        product_store_repository.add_product_store(db_session, 1, 2)
        product_store_repository.add_product_store(db_session, 1, 3)
        
        # Obtener relaciones
        product_stores = product_store_repository.get_product_stores(db_session, 1)
        
        assert len(product_stores) == 3
        store_ids = {ps.store_id for ps in product_stores}
        assert store_ids == {1, 2, 3}
    
    def test_get_product_stores_empty(self, db_session):
        """Test obtener tiendas de un producto sin tiendas"""
        # Crear producto sin tiendas
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        db_session.commit()
        
        # Obtener relaciones
        product_stores = product_store_repository.get_product_stores(db_session, 1)
        assert product_stores == []
    
    def test_get_product_store_existing(self, db_session):
        """Test obtener una relación específica existente"""
        # Crear producto y tienda
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        store = store_repository.create_store(db_session, 1)
        db_session.commit()
        
        # Añadir relación
        product_store_repository.add_product_store(db_session, 1, 1)
        
        # Obtener relación específica
        product_store = product_store_repository.get_product_store(db_session, 1, 1)
        assert product_store is not None
        assert product_store.product_id == 1
        assert product_store.store_id == 1
    
    def test_get_product_store_non_existing(self, db_session):
        """Test obtener una relación que no existe"""
        product_store = product_store_repository.get_product_store(db_session, 999, 999)
        assert product_store is None
    
    def test_delete_product_store(self, db_session):
        """Test eliminar una relación producto-tienda"""
        # Crear producto y tienda
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        store = store_repository.create_store(db_session, 1)
        db_session.commit()
        
        # Añadir relación
        product_store = product_store_repository.add_product_store(db_session, 1, 1)
        db_session.commit()
        
        # Verificar que existe
        assert product_store_repository.get_product_store(db_session, 1, 1) is not None
        
        # Eliminar relación
        product_store_repository.delete_product_store(db_session, product_store)
        db_session.commit()
        
        # Verificar que ya no existe
        assert product_store_repository.get_product_store(db_session, 1, 1) is None
    
    def test_delete_product_store_by_ids(self, db_session):
        """Test eliminar una relación producto-tienda por IDs"""
        # Crear producto y tienda
        product = product_repository.create_product(db_session, 1, "Test", 10.0)
        store = store_repository.create_store(db_session, 1)
        db_session.commit()
        
        # Añadir relación
        product_store_repository.add_product_store(db_session, 1, 1)
        db_session.commit()
        
        # Verificar que existe
        assert product_store_repository.get_product_store(db_session, 1, 1) is not None
        
        # Eliminar por IDs
        product_store_repository.delete_product_store_by_ids(db_session, 1, 1)
        db_session.commit()
        
        # Verificar que ya no existe
        assert product_store_repository.get_product_store(db_session, 1, 1) is None
    
    def test_delete_product_store_by_ids_non_existing(self, db_session):
        """Test eliminar una relación que no existe no causa error"""
        # No debe causar error
        product_store_repository.delete_product_store_by_ids(db_session, 999, 999)
        db_session.commit()
