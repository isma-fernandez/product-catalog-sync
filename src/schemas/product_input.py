from pydantic import BaseModel, Field, PositiveInt, PositiveFloat

class ProductInput(BaseModel):
    product_id: PositiveInt = Field(..., description="Identificador del producto")
    # REGEX: Detecta una cadena de dígitos separados por '|', por ejemplo: "1|2|3"
    # o simplemente un dígito "1"
    store_id: str = Field(..., pattern=r"^\d+(?:\|\d+)*$", description="Identificador de la tienda")
    title: str = Field(..., description="Título del producto", min_length=1)
    price: PositiveFloat = Field(..., description="Precio del producto")