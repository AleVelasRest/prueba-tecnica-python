1.  **SOLID:**
    - Dé un ejemplo concreto en Python (pseudocódigo o código) de cómo aplicaría el principio de Inversión de Dependencias (DIP) al conectar una base de datos o una API externa.

> Se declara la interface DSConnector.  
> Se crean 2 clases hijas una para Postgres y otra para un API (PostgresDS y APIDS).  
> Se crea una función (search_order) para obtener los datos usando las clases hijas.  
> Se hace el llamado con ambas.

**Creación de interface:**

```python
# base.py
# Libreria de classes y methodos abstractos
from abc import ABC, abstractmethod					 

class DSConnector(ABC):
    @abstractmethod
    def get_order_data(self, order_id: int):
        pass
```

**Para Postgres:**

```python
# postgres_ds.py
import psycopg
from psycopg.rows import dict_row
from .base import DSConnector # base.py estando en el mismo directorio

class PostgresDS(DSConnector):
    def __init__(self, dsn: str):
        self.dsn = dsn

    def get_order_data(self, order_id: int):
        """
        Obtiene los datos de una orden desde PostgreSQL.
        Parámetros:
            order_id (int): ID de la orden que se desea consultar.
        Devuelve:
            dict | None: Diccionario con los datos de la orden,
            o None si no existe.
        """		
        try:
            with psycopg.connect(self.dsn) as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(
                        "SELECT * FROM orders WHERE id = %s",
                        (order_id,)
                    )
                    order = cur.fetchone()
                    return order

        except psycopg.Error as e:
            print(f"Error de PostgreSQL al consultar la orden {order_id}: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado al consultar la orden {order_id}: {e}")
            return None
```

**Para API:**

```python
# api_ds.py
import httpx
from .base import DSConnector # base.py estando en el mismo directorio

class APIDS(DSConnector):
    def __init__(self, base_url: str, api_key: str | None = None):
        """
        base_url: URL base de la API externa (ej: https://api.summa.com)
        api_key: Token o llave
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def get_order_data(self, order_id: int):
        """
        Obtiene datos de una orden desde una API externa.
        Parámetros:
            order_id (int): ID de la orden a consultar.
        Devuelve:
            dict | None: Datos de la orden o None si ocurre un error.
        """
        url = f"{self.base_url}/orders/{order_id}"

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        try:
            response = httpx.get(url, headers=headers, timeout=10)

            # Evalua errores
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            print(
                f"HTTP error al consultar la orden {order_id}: "
                f"{e.response.status_code} {e.response.text}"
            )
            return None

        except httpx.RequestError as e:
            print(f"Error de conexión con la API al consultar la orden {order_id}: {e}")
            return None

        except ValueError as e:
            print(f"Respuesta JSON inválida al consultar la orden {order_id}: {e}")
            return None

        except Exception as e:
            print(f"Error inesperado al consultar la orden {order_id}: {e}")
            return None
```

**Llamado**

```python
# main.py
from base import DSConnector
from postgres_ds import PostgresDS
from api_ds import APIDS

def search_order(order_id: int, datasource: DSConnector):
    order = datasource.get_order_data(order_id)

    if order is None:
        return f"No se pudo obtener la orden {order_id}"

    return f"Orden recibida: {order}"

# Para Postgres
ds = PostgresDS("postgres://user:pass@pg.summa.com:5432/db")
print("Desde postgres: ", process_order(10, ds))
# Para API
ds = APIDS("https://api.summa.com", api_key="SuperKlabe")
print("Desde API: ", process_order(10, ds))
```

2.  **Odoo ORM:**
    - En el contexto de Odoo, explique la diferencia entre `_inherit` y `_inherits`. ¿En qué caso usaría cada uno para extender la funcionalidad de un modelo existente como `sale.order`?

> Ambas extienden el modelo base pero afectan la base de datos de diferente manera

| Diferencia | \_inherit | \_inherits |
| --- | --- | --- |
| ***En base de datos:*** | Crea columnas partiendo de nuevos atributos en la misma tabla | Crea una nueva tabla relacionada para los nuevos atributos |
| ***En uso:*** | Cuando los nuevos atributos son requeridos o se guardan con frecuencia | Para el caso de sales.order o de los modelos de los módulos base de Odoo sirve usar \_inherits si las ordenes de venta no llevan con frecuencia los nuevos atributos. |

3.  **Gestión de Dependencias y Git:**
    
    - Sabemos que la forma de manejar los paquetes y las dependencias de los proyectos de Python es con un `requirements.txt`, ¿Qué opciones de mejora sugiere para el manejo de paquetes y por qué?
    
    > El uso de del gestor de proyectos de python UV, se está convirtiendo en el favorito de los desarrolladores por estable y práctico, una vez que se inicia un proyecto con UV ya se tiene el repositorio local de git, cada que se agrega un paquete, UV lo registra y se conserva su integridad.
    
    - Describa brevemente su flujo de trabajo ideal en Git (Branching model) y qué considera una "buena práctica" al escribir un mensaje de commit.
    
    > El uso de una plantilla asi:
    > 
    > &lt;tipo&gt;(ámbito): resumen
    > 
    > Detalle si es necesario
    > 
    >   
    > **Tipos**  
    > feat: característica
    > 
    > fix: arreglo
    > 
    > docs: documentación
    > 
    > gui: interfaz (de usuario)
    > 
    > **Ejem:  
    > **
    > 
    > feat(login): Nueva opción de logueo con llave al correo con OTP  
    > Se tenía solo acceso con usuario y contraseña ya se puede usar un OTP, queda pendiente la integración con Google, Meta y MS.  
    
4.  **Tipado y Genéricos:**
    
    - Explique la utilidad de usar `Generic[T]` y `TypeVar` en Python. Dé un ejemplo breve de una función o clase donde el uso de genéricos mejore la seguridad del tipo y la reutilización del código.
  > Los genéricos permiten controlar la susceptibilidad del código a errores que tengan que ver con tipos de objetos, un caso común es la consulta en tablas donde la llave primaria puede ser un int, str o un uuid.
> 
```python
from typing import Generic, TypeVar

T = TypeVar("T")  # El tipo de tabla como sales_orden, products, etc
ID = TypeVar("ID")  # El tipo del ID (int, str, uuid)

class Repository(Generic[T, ID]):
    def get(self, id: ID) -> T:
        raise error # manejo de errores
```

```python
class ReadOrder(Repository[Order, int]):
    def get(self, id: int) -> Order:
        try:
			order = ...query o llamado a api
            return Dict[order] # Devuelve el la orden en un diccionario
        except KeyError:
            raise ValueError(f"La orden con id {id} no existe")
```

```python
repo = ReadOrder()

order = repo.get(1)
print(order)  
```
	  
5.  **Arquitectura:**
    
    - ¿Por qué es importante que la capa de `services` (Lógica de Negocio) no importe nada de la capa de `routers` (Infraestructura Web)?
	  > Porque invalidaría la separación de responsabilidades, la intención de llevar la lógica del negocio a la abstracción es que no dependa de si hay una db relacional, noSQL, API, etc.
	   > La capa de services encapsula el negocio.
	   > La capa de routers expone los datos.
