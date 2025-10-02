
# Digos-Footwear-Online-PH
###  Django-based e-commerce platform for Digos Footwear.
---
## Getting Started
### 1. Activate Virtual Environment
```bash
venv\Scripts\activate
cd DFOPH_project
```

### to install requirements
```bash
pip install -r requirements.txt
```

### to run automigrate (instead of manually migrate apps ['DFOPH_accounts', 'DFOPH_sellers', 'DFOPH_buyers']):
```python 
python manage.py automigrate
```

### to create a admin user for authentication
```python
python manage.py createsuperuser
```

## Installation notes 
### to check the existing requirements.txt 
```cmd
type requirements.txt
```
### to change ports configuration the same field as xammp
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
