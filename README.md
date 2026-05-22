# Sistema de Gestión de Servicios de Calibración (SIMAC)

Aplicación híbrida móvil y web desarrollada para la gestión de órdenes de servicio en un laboratorio de calibración acreditado.

El proyecto integra:

- Backend en Flask (Python)
- API REST
- Aplicación móvil híbrida con Ionic + Angular
- Base de datos MySQL
- Integración móvil Android mediante Capacitor

---

# Características

--> Inicio de sesión  
--> Gestión de órdenes de servicio  
--> Visualización de detalles  
--> Creación de órdenes  
--> Edición de órdenes  
--> Eliminación de órdenes  
--> Navegación mediante SideMenu  
--> Consumo de API REST  
--> Aplicación móvil híbrida Android  
--> Conexión a base de datos MySQL  

---

# Tecnologías Utilizadas

## Backend

- Python
- Flask
- Flask SQLAlchemy
- Flask CORS
- MySQL
- SQLAlchemy

## Frontend Móvil

- Ionic
- Angular
- TypeScript
- Capacitor

## Base de Datos

- MySQL

---

# Estructura del Proyecto

```bash
Api Mobil/
│
├── Gestioserviciosflask/     # Backend Flask
├── calibracionApp/           # Aplicación Ionic
├── database/                 # Base de datos SQL
└── README.md
```

---

# Instalación del Backend Flask

## 1. Crear entorno virtual

```bash
python -m venv venv
```

---

## 2. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
pip install flask flask_sqlalchemy flask_cors pymysql pandas werkzeug
```

---

## 4. Ejecutar servidor Flask

```bash
python main.py
```

Servidor:

```bash
http://127.0.0.1:5000
```

---

# Configuración Base de Datos

Importar el archivo:

```bash
database/laboratorio_calibracion.sql
```

en MySQL Workbench.

---

# Instalación Aplicación Ionic

## 1. Entrar al proyecto

```bash
cd calibracionApp
```

---

## 2. Instalar dependencias

```bash
npm install
```

---

## 3. Ejecutar aplicación web

```bash
ionic serve
```

---

## 4. Ejecutar en Android

```bash
ionic capacitor run android
```

---

# API REST

## Obtener órdenes

```http
GET /api/ordenes
```

---

## Obtener detalle de orden

```http
GET /api/orden/{id}/detalle
```

---

## Crear orden

```http
POST /api/orden
```

---

## Editar orden

```http
PUT /api/orden/{id}
```

---

## Eliminar orden

```http
PUT /api/orden/{id}/eliminar
```

---

# Pantallas Implementadas

- Login
- Home
- Lista de órdenes
- Detalle de orden
- Crear orden
- Editar orden

---

# Autor

Jesus Delgado

Maestría en Sistemas Computacionales

---

# Evidencias

La aplicación fue probada en:

- Navegador Web

---

# Licencia

Proyecto académico y educativo.
