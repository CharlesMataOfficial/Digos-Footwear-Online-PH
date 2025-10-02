
# Digos-Footwear-Online-PH
###  Django-based e-commerce platform for Digos Footwear.
---
## Getting Started
### 1. Activate Virtual Environment
```bash
venv\Scripts\activate
cd DFOPH_project
```
### 2. To remove existing pycache and migration files (Only optional when to drop all data in database.
### Delete migration files (except __init__.py), all __pycache__ folders, and .pyc files
```bash
Get-ChildItem -Path . -Recurse -Include *.py -Exclude __init__.py | Where-Object { $_.DirectoryName -match "migrations" } | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Include *.pyc | Remove-Item -Force
```
### 3. To install requirements
```bash
pip install -r requirements.txt
```
### 4. To run automigrate (instead of manually migrate apps ['DFOPH_accounts', 'DFOPH_sellers', 'DFOPH_buyers']):
```python 
python manage.py automigrate
```

### 5. To create a admin user for authentication
```python
python manage.py createsuperuser
```

## Installation notes 
### 1. To check the existing requirements.txt 
```cmd
type requirements.txt
```
### 2.To change ports configuration the same field as xammp
```cmd
xammp my.ini=port=3306
```
### settings.py
```cmd
'HOST': '127.0.0.1',
'PORT': '3306',
```
### phpMyAdmin config
### xampp\phpMyAdmin\config.inc.php
```php
$cfg['Servers'][$i]['host'] = '127.0.0.1';
$cfg['Servers'][$i]['port'] = '3306';
```
