# <p align="center">WiFi_Access 🔐

<p align="center">Простой и в то же время полезный инструмент для получения списка всех имён сетей WiFi и их пароля, к которым когда-либо был подключён Ваш ПК!
<p align="center">Работает отлично как на Linux, так и на Windows! Но это ещё не всё, данный инструмент также работает и на Android!

## ⚡️ Установка

### Для Linux и Termux:
```python
pip3 install WiFi_Access
```

### Для Windows:
```python
pip install WiFi_Access
```
<br>

## 🌀 Использование

### Код на Python:
```python
from WiFi_Access import WiFi

# Вызов функции получения всех имён wifi и их паролей
wifi = WiFi.start()

# Вывод списка всей информации
print(wifi)
```
### Результат:
```python
>>> [{'name': 'Network 1', 'password': 'Password'}, {'name': 'TestNet', 'password': 'qwerty12'}, {'name': 'Free WiFi', 'password': None}]
```

### Другие примеры на Python:
```python
from WiFi_Access import WiFi

# Вызов функции получения всех имён wifi и их паролей исключительно на Windows
Windows = WiFi()
Windows.windows(prints=True)

# Вызов функции получения всех имён wifi и их паролей исключительно на Linux
Linux = WiFi()
Linux.linux(prints=True)

# Вызов функции получения всех имён wifi и их паролей исключительно на Android
Android = WiFi()
Android.android(prints=True) # Права суперпользователя обязательны (ROOT)!

# С аргументом 'prints' равному True, будет производиться вывод в терминале
```
<br>

## 💎 Связь
 - **[Telegram](https://t.me/MY_INSIDE_DREAM)**