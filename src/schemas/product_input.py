from pydantic import BaseModel, Field, PositiveInt, PositiveFloat, field_validator, conint
import re

class ProductInput(BaseModel):
    product_id: int = Field(..., description="Identificador del producto", ge=0)
    # REGEX: Detecta una cadena de dígitos separados por '|', por ejemplo: "1|2|3"
    # o simplemente un dígito "1"
    store_id: set[int] = Field(..., description="Identificador de la tienda")
    title: str = Field(..., description="Título del producto", min_length=1)
    price: PositiveFloat = Field(..., description="Precio del producto")


    @field_validator("title")
    def title_must_not_be_empty(cls, value: str) -> str:
        """
        Comprobación de que no este en blanco el título, min_length cuenta los espacios
        """
        if not value.strip():
            raise ValueError("El título no debe estar vacío")
        return value
    
    @field_validator("store_id", mode="before")
    def parse_store_id(cls, value: str) -> set[int]:
        """
        Parsea la cadena de store_id en un set de enteros positivos
        """
        pattern=r"^\d+(?:\|\d+)*$"
        if re.match(pattern, value):
            return {int(x) for x in value.split("|")}
        else:
            raise ValueError(f"store_id debe ser una cadena de dígitos separados por '|', valor recibido: {value}")
        
    def __str__(self) -> str:
        return f"{self.title} ({self.product_id}), tienda/s={self.store_id}, precio={self.price})"