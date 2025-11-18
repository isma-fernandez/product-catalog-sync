from src.models.base import init_db

def main():
    print("Inicializando la base de datos...")
    init_db()
    print("Base de datos inicializada.")

if __name__ == "__main__":
    main()