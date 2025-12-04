# BookStack-API

## 1. Introducción

El presente manual describe el procedimiento de instalación, configuración y ejecución del framework de automatización de pruebas de la API REST de BookStack, específicamente para los módulos **Shelves (Estantes)** y **Books (Libros)**.

Su propósito es orientar a testers, desarrolladores y analistas de calidad en el uso correcto del entorno de pruebas, desde la preparación local hasta la generación de reportes visuales con **Allure Reports**.

El framework fue desarrollado en **Python**, utilizando las siguientes tecnologías:
- **Pytest** como motor de ejecución de pruebas.
- **JSON Schema** para la validación estructural de las respuestas.
- **Allure-Pytest** para la generación de reportes visuales.
- **Logger personalizado** para el registro de las llamadas API (método, headers, payload y respuesta).
- **Fixtures reutilizables** que gestionan la creación y limpieza de datos (shelves/books).

## 2. Requisitos previos

Antes de ejecutar el framework, asegúrese de cumplir con los siguientes requisitos:

| **Requisito**         | **Descripción**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| **Python**            | Versión 3.10 o superior.                                                        |
| **pip**               | Gestor de paquetes incluido con Python.                                          |
| **Git**               | Para clonar el repositorio.                                                     |
| **Allure CLI**        | (Opcional, para generar reportes visuales).                                      |
| **IDE recomendado**   | PyCharm o Visual Studio Code.                                                   |
| **Postman o Insomnia**| (Opcional, para verificar manualmente los endpoints).                           |

## 3. Instalación y Configuración

### Paso 1. Clonar el repositorio

Ejecute en su terminal:

```bash
git clone https://github.com/gualbertoChoque/BookStack-API.git
cd BookStack  
```
## 4. Configurar variables del entorno

En el archivo `config.py` se encuentran las variables base utilizadas por las pruebas:

```python
BASE_URI = 'http://bookstack.test/api'

BASE_INVALID_URI = 'http://bookstack.test/apis'

TOKEN = 'Token vaoa9QNuviHZDpAHu7ym49VtX7XGNTZS:KM8hE4eX2IGVgAPbSKOcVIm4v6zuYmBe'
```
Ajuste estos valores si trabaja en un entorno diferente o de desarrollo local.

---

## 5. Ejecución de pruebas

El framework permite ejecutar todas las pruebas, por módulo o por tipo de marca (mark) según la necesidad.

### Ejecución completa:

```bash
pytest --alluredir=allure-results
```
## Ejecución por tipo de pruebas (marks):

```bash
pytest -m smoke --alluredir=allure-results
pytest -m regression --alluredir=allure-results
pytest -m negative --alluredir=allure-results
pytest -m positive --alluredir=allure-results
```
## Ejecución por archivo o modulos:

```bash
pytest tests/api-qase/shelves/test_US002_Obtener_un_estante.py --alluredir=allure-results
```
## Limpieza de resultados anteirores:

```bash
rmdir /s /q allure-results
```