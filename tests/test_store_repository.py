"""
Tests para store_repository
"""
import pytest
from src.repositories import store_repository


@pytest.mark.unit
class TestStoreRepository:
    """Tests para las operaciones del repositorio de tiendas"""
    
    def test_create_store(self, db_session):
        """Test crear una tienda en la base de datos"""
        store = store_repository.create_store(db_session, store_id=1)
        
        assert store.store_id == 1
        
        # Verificar que se puede recuperar de la DB
        db_store = store_repository.get_store(db_session, 1)
        assert db_store is not None
        assert db_store.store_id == 1
    
    def test_get_store_existing(self, db_session):
        """Test obtener una tienda existente"""
        # Crear tienda
        store_repository.create_store(db_session, store_id=1)
        
        # Recuperar tienda
        store = store_repository.get_store(db_session, 1)
        assert store is not None
        assert store.store_id == 1
    
    def test_get_store_non_existing(self, db_session):
        """Test obtener una tienda que no existe"""
        store = store_repository.get_store(db_session, 999)
        assert store is None
    
    def test_get_or_create_store_new(self, db_session):
        """Test get_or_create con una tienda nueva"""
        # Verificar que no existe
        assert store_repository.get_store(db_session, 1) is None
        
        # Crear usando get_or_create
        store = store_repository.get_or_create_store(db_session, 1)
        assert store is not None
        assert store.store_id == 1
        
        # Verificar que se creó
        db_store = store_repository.get_store(db_session, 1)
        assert db_store is not None
    
    def test_get_or_create_store_existing(self, db_session):
        """Test get_or_create con una tienda existente"""
        # Crear tienda primero
        original_store = store_repository.create_store(db_session, store_id=1)
        db_session.commit()
        
        # Obtener usando get_or_create
        store = store_repository.get_or_create_store(db_session, 1)
        
        # Verificar que devuelve la misma tienda
        assert store.store_id == original_store.store_id
        
        # Verificar que no se duplicó
        db_session.commit()
        all_stores = db_session.query(store_repository.Store).all()
        assert len(all_stores) == 1
