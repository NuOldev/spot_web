# Mi Panel de Administración - Restaurante

## Propósito
- Administrar el menú de mi negocio (agregar, editar, eliminar productos)
- Acceso remoto desde cualquier lugar (no solo desde mi laptop)
- Control de acceso con usuario y contraseña (solo yo)

## Estado Actual
- ✅ Menú público funcionando
- ✅ Panel de administración con autenticación
- ✅ Creación de productos
- ⬜ Edición de productos (funciona pero sin verificar propiedad)
- ⬜ Eliminación de productos (funciona pero sin verificar propiedad)
- ⬜ Productos existentes sin `user_id` (necesitan actualización)
- ⬜ En producción en PythonAnywhere

## Estructura de Archivos

- ### Spot_Web 

        spot_web/

            └── ___pycache__/

            └── data/
                |── menu.json

            └── instance/
                |── menu.db

            └── static/

                └── css/
                    |── admin.css
                    |── menu.css
                    |── style.css
                
                └── img/
                    |── menu.css
                    |── style.css
                    
            └── templates/
                ├── index.html
                ├── menu.html
                ├── login.html
                ├── register.html
                ├── logout.html
                ├── admin.html
                ├── admin_new.html
                └── admin_edit.html
            
            └── venv/

            ├── .env (NO subir a GitHub)
            ├── app.py
            ├── extensions.py 
            ├── MANUAL.md (Este archivo)
            ├── models.py 
            ├── requirements.txt 
            ├── seed.py 
            ├── update_products.py 

## Configuración del Entorno

### Variables de Entorno (`.env`)
- `SECRET_KEY`: Clave para firmar las cookies de sesión
- `FLASK_ENV`: `development` o `production`

### Dependencias Principales
- Flask
- Flask-SQLAlchemy (ORM para base de datos)
- Flask-Bcrypt (Encriptación de contraseñas)
- Flask-Login (Manejo de sesiones)
- python-dotenv (Carga de variables de entorno)


## Modelos de Base de Datos

### User
- `id`: Integer, primary_key
- `user_name`: String(50), nullable=False
- `email`: String(50), nullable=False, unique=True
- `password_hash`: String(120), nullable=False, unique=True
- `products`: Relación con Product (solo de ida)

### Product
- `product_id`: Integer, primary_key
- `product_name`: String(100), nullable=False
- `description`: String(100)
- `price`: Numeric(7,2), nullable=False
- `stock`: Integer
- `category`: String(50)
- `add_date`: Date, default=datetime.utcnow
- `user_id`: Integer, ForeignKey('user.id')
- `UniqueConstraint('product_name', 'user_id', name='restriccion')`

### Relaciones
- User → Product: Un usuario puede tener muchos productos (relación de ida)
- Product → User: No tiene relación inversa (por ahora)


## Rutas de la Aplicación

### Rutas Públicas
| Ruta | Método | Función | Descripción |
|------|--------|---------|-------------|
| `/` | GET | `inicio()` | Página de inicio |
| `/menu` | GET | `menu()` | Muestra el menú completo |

### Rutas de Autenticación
| Ruta | Método | Función | Descripción |
|------|--------|---------|-------------|
| `/register` | GET, POST | `register()` | Registro de nuevo usuario |
| `/login` | GET, POST | `login()` | Inicio de sesión |
| `/logout` | GET, POST | `logout()` | Cierre de sesión |

### Rutas de Administración (Protegidas con @login_required)
| Ruta | Método | Función | Descripción |
|------|--------|---------|-------------|
| `/admin` | GET | `admin_office()` | Panel de administración |
| `/admin/new_product` | GET, POST | `new_product()` | Crear nuevo producto |
| `/admin/edit/<int:product_id>` | GET, POST | `edit_product()` | Editar producto |
| `/admin/delete/<int:product_id>` | POST | `delete_product()` | Eliminar producto |


## Decisiones Técnicas

### Por qué NO usamos relación inversa en Product
- Solo yo (un usuario) administraré los productos
- No necesito saber qué admin creó cada producto
- Si en el futuro agrego más admins, se puede agregar fácilmente

### Por qué usamos `db.session.get()` en lugar de `db.get_or_404()`
- `db.session.get()` devuelve None si no encuentra el producto
- `db.get_or_404()` muestra error 404 automáticamente
- Decisión: Usar `db.get_or_404()` para edición (requiere que exista)
- Decisión: Usar `db.session.get()` para eliminación (debemos manejar el error)

### Manejo del `user_id` en productos
- Productos existentes (desde seed.py): necesitan actualización con `update_products.py`
- Productos nuevos: se crean con `user_id=current_user.id`


## Scripts Útiles

### `update_products.py`
**Propósito:** Asignar `user_id` a los productos existentes en la base de datos.

**Cuándo usarlo:** Después de agregar la relación User-Product y antes de subir a producción.

**Cómo ejecutarlo:**
```bash
python update_products.py
```

`seed.py` (Original)

**Propósito:** Cargar productos iniciales desde un archivo JSON.

**Modificación necesaria:** Agregar `user_id=user.id` al crear cada producto.
`create_database.py` (Opcional)

**Propósito:** Crear la base de datos desde cero.


## Despliegue en PythonAnywhere

### Pasos Realizados
1. Crear cuenta en PythonAnywhere
2. Subir el código (via GitHub o manual)
3. Configurar entorno virtual
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar variables de entorno en `.env`
6. Configurar archivo WSGI
7. Recargar la aplicación

### URL del Sitio
`https://spot_web.pythonanywhere.com`

### Archivo WSGI
`/var/www/<mi_usuario>_pythonanywhere_com_wsgi.py`

### Variables de Entorno en Producción
- `SECRET_KEY`: Valor aleatorio generado con `os.urandom(24)`