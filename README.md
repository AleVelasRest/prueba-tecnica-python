# Prueba Técnica: Backend Developer (Python & Architecture)

## Contexto de negocio

Usted trabaja para "Logística Tech". Se le ha encargado construir un **Microservicio de Ingesta de Pedidos**. Este servicio actúa como una puerta de entrada que recibe pedidos de clientes externos, valida las reglas de negocio y los despacha hacia un sistema ERP central.

**Nota Importante:** Aunque la empresa usa un ERP específico, el diseño de su solución debe ser agnóstico a la tecnología de destino, permitiendo cambiar el ERP en el futuro sin reescribir la lógica de negocio.
Los entregables de este proyecto deben subirse a su repositorio de GitHub. Trate de hacer buen manejo de las ramas, commits, PR y las carpetas dentro del repositorio. Para la parte teórica, responda las siguientes preguntas en un archivo `teoria.md` dentro del repositorio.

---

## Parte 1: Fundamentos de Ingeniería

1. **SOLID:**
    * Dé un ejemplo concreto en Python (pseudocódigo o código) de cómo aplicaría el principio de Inversión de Dependencias (DIP) al conectar una base de datos o una API externa.

2. **Odoo ORM:**
    * En el contexto de Odoo, explique la diferencia entre `_inherit` y `_inherits`. ¿En qué caso usaría cada uno para extender la funcionalidad de un modelo existente como `sale.order`?

3. **Gestión de Dependencias y Git:**
    * Sabemos que la forma de manejar los paquetes y las dependencias de los proyectos de Python es con un `requirements.txt`, ¿Qué opciones de mejora sugiere para el manejo de paquetes y por qué?
    * Describa brevemente su flujo de trabajo ideal en Git (Branching model) y qué considera una "buena práctica" al escribir un mensaje de commit.

4. **Tipado y Genéricos:**
    * Explique la utilidad de usar `Generic[T]` y `TypeVar` en Python. Dé un ejemplo breve de una función o clase donde el uso de genéricos mejore la seguridad del tipo y la reutilización del código.

5. **Arquitectura:**
   * ¿Por qué es importante que la capa de `services` (Lógica de Negocio) no importe nada de la capa de `routers` (Infraestructura Web)?

---

## Parte 2: Desafío Práctico - API de Ingesta

Debe construir una API REST usando FastAPI (preferible) o Flask.

### Requerimientos Funcionales

#### Ingesta de Pedidos (`POST /orders`)

Crear un endpoint POST que reciba un pedido, valide reglas de negocio y lo guarde en una base de datos `SQLite`

##### JSON de Entrada

```json
{
    "external_id": "AMZ-999",
    "customer": {
        "email": "client@test.com",
        "name": "Juan Perez",
        "client_id": "123456789"
    },
    "items": [
        {
            "sku": "ABC-1",
            "quantity": 2,
            "price_unit": 150.00
        },
        {
            "sku": "ABC-2",
            "quantity": 4,
            "price_unit": 100.00
        }
    ],
    "date": "2025-10-20T14:30:00"
}
```

* Reglas
  * Validar que `quantity > 0` y `price_unit >= 0`
  * El email debe tener formato válido
  * Si el total es mayor a $300, marcar el campo `is_vip` como `True`
  * Para la fecha de llegada (`arrival_date`), se debe calcular así:
    * Si la persona es VIP, se debe sumar 3 días a la fecha `date`
    * Si la persona no es VIP, se debe sumar 5 días a la fecha `date`

#### Reporte de los Pedidos (`GET /orders/report`)

El negocio necesita visualizar el volumen de compras por cliente. Cree un endpoint que devuelva un objeto JSON relacionando el usuario con sus órdenes acumuladas.

Salida esperada (JSON): El endpoint debe retornar una lista de objetos con el resumen acumulado de lo que se ha procesado hasta el momento

##### JSON de Salida

```json
[
  {
    "customer_email": "neron.navarrete@test.com",
    "total_orders": 5,
    "total_amount_spent": 1500.00,
    "is_vip": "True",
    "arrival_date": "2025-10-22T14:30:00"
  },
  {
    "customer_email": "jane.doe@test.com",
    "total_orders": 2,
    "total_amount_spent": 280.50,
    "is_vip": "False",
    "arrival_date": "2025-10-26T14:30:00"
  }
]
```

* Reglas
  * `"customer_email":` Corresponde al correo del usuario
  * `"total_orders":` Corresponde a la cantidad total de órdenes
  * `"total_amount_spent":` Corresponde al total gastado en las órdenes
  * `"is_vip":` Corresponde a la validación del total de las órdenes
  * `"arrival_date":` Corresponde a la fecha de llegada de las órdenes

### Requerimientos Técnicos y Estructura

#### Criterios de Implementación

1. **Abstracción y Desacoplamiento**
    * El sistema debe implementar un mecanismo que desacople la lógica de negocio de la capa de acceso a datos.
    * Se espera que el dominio no dependa directamente de implementaciones concretas de infraestructura.

2. **Persistencia y Almacenamiento**
    * Implemente una solución de persistencia utilizando una base de datos relacional ligera (SQLite para facilitar la ejecución local).
    * La elección de herramientas y estrategias de consulta queda a criterio.
    * Asegure una gestión eficiente de los recursos (conexiones, sesiones, cursores).

3. **Manejo de Errores y Resiliencia**
    * El sistema debe ser capaz de diferenciar claramente entre errores de dominio/negocio y errores de infraestructura.
    * La API debe mapear estas excepciones a los códigos de estado HTTP semánticamente correctos.

---

## Parte 3: Conocimiento Específico Odoo

*Esta sección es teórica/conceptual para validar el conocimiento específico de la herramienta, pero separada de la arquitectura limpia de la Parte 2.*

Cree una carpeta llamada `odoo_module_design`. Allí, agregue un archivo Python (`models.py`) como si estuviera desarrollando un módulo dentro de Odoo.

**El requerimiento:** Escriba el código Python (usando la API de Odoo) para definir un modelo que extienda `sale.order`.

* Agregue un campo nuevo llamado `x_order_number`.
* Agregue un campo nuevo llamado `x_external_company` (Selection: 'ecommerce', 'manual', 'Amazon').
* Agregue un campo computado `x_is_big_order` que sea `True` si el `amount_total` es mayor a 500.
* Incluya el método `_compute_x_is_big_order`.
* Incluya una restricción la cual valide que `x_order_number` sea mayor o igual que 10.

*Nota: Este código no necesita ser ejecutado, solo se evaluará la sintaxis correcta del ORM de Odoo y las decoraciones.*

---

## Parte 4: Extra (Opcional)

**Docker:** Incluya un Dockerfile para levantar su aplicación con un solo comando.

---

## Criterios de Evaluación

* Arquitectura Limpia
* Calidad Pythonica
* Extensibilidad
* Buenas Prácticas

