# Instalación de Dependencias

## Paso 1 => Instalar [poetry](https://python-poetry.org/)
```python
pip install poetry
```
## Paso 2 => Politica de Ejecución de Scripts
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
## Paso 3 => Crear Virtual Environment Recomendado (Optional) 
```python
virtualenv venv_app
```
### Paso 3.1 => Activar Virtual Environment 
```powershell
& c:/<nominaApp>/<venv_app>/Scripts/Activate.ps1
``````
## Paso 4 Instalar Dependencies
```python
poetry install --no-root
```

# Uso

## Ejecuta:
```python
python manage.py runserver
```