# BERNINI API REST PARA APP
___
## Requisitos previos

python  
virtualenv

## Instalación 

*Teniendo instalado python*  
`pip install virtualenv`

*Crear entorno virtual:*  
`python -m virtualenv venv`

*Activar entorno virtual:*  
`.venv/scripts/activate`

*Instalar dependencias:*  
`pip install -r requirements.txt`

## Ejecución

`python manage.py runserver`
___
## URL's del proyecto

Panel admin: http://127.0.0.1:8000/admin/  
Documentación Rest api: http://127.0.0.1:8000/swagger/  
Api root: http://127.0.0.1:8000/api/v1/

## Usuarios

- **Superuser (user_id = 1):** eladmin / asdf1234
- **Usuario 2 (user_id = 2):** comprador / asdf1234$
- **Usuario 3 (user_id = 3):** otro_comprador / asdf1234$

### Tokens
- **Superuser:** 2f69f427e555ec618ff4c41cdb2fefda1a5b943c
- **Usuario 2:** b3ca152f6fd58b0b48cd8faa7c36a2d0eb260d2b
- **Usuario 3:** b75074de71c44c583d982453bdaee3485078b97b

___
# REST API

## `GET /api/v1/products/`
### Petición

`http://127.0.0.1:8000/api/v1/products/`

### Respuesta

Devuelve listado de productos

~~~json
{
    "id": 1,
    "name": "Zapato de tacón de aguja",
    "description": "Zapato de tacón de aguja elegante.",
    "color": "Rojo",
    "cost": "120.00"
}
~~~
___
## `POST /api/v1/create_orders/`
### Petición

`http://127.0.0.1:8000/api/v1/create_orders/`

~~~json
{
  "pedido": {
    "user": 3,
    "address": "Av. Manuel Candela, nº141, pta23",
    "zip_code": "46021",
    "country": "Spain"
    
  },
  "pedido_lineas": [
      {
        "product": 1,
        "quantity": 2,
        "sell_cost": 115.95
      },
      {
        "product": 4,
        "quantity": 2,
        "sell_cost": 120.00
      }
  ]
}
~~~
___
## `GET /api/v1/recover_orders/{id}`
### Petición

`http://127.0.0.1:8000/api/v1/recover_orders/{id}`

**Requiere envío de token en el header**

### Respuesta

Devuelve datos del pedido con sus líneas de pedido

~~~json
{
    "pedido": {
        "id": 4,
        "address": "Bernhardstrasse, 112, 16",
        "zip_code": "46002",
        "country": "Switzerland",
        "order_date": "2023-07-16",
        "shipping_cost": "12.00",
        "user": 3
    },
    "pedido_lineas": [
        {
            "id": 9,
            "quantity": 2,
            "sell_cost": "115.95",
            "order": 4,
            "product": 1
        },
        {
            "id": 10,
            "quantity": 2,
            "sell_cost": "120.00",
            "order": 4,
            "product": 4
        }
    ]
}
~~~
___
## `GET /api/v1/orders/`
### Petición

`http://127.0.0.1:8000/api/v1/orders/`  

`http://127.0.0.1:8000/api/v1/orders/{id}`

**Requiere envío de token en el header**

### Respuesta

Devuelve listado de pedidos según el usuario (Si es superuser devuelve todos)

~~~json
{
    "id": 2,
    "address": "C/ Colón, nº5, pta12",
    "zip_code": "46002",
    "country": "Spain",
    "order_date": "2023-07-16",
    "shipping_cost": "6.00",
    "user": 2
}
~~~
___
## Notas del proyecto
*Se han implementado todos los requisitos y otros puntos valorables a excepción de docker*.