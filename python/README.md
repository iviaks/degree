# Для установки всех зависимостей
```bash
pip install -r requirements.txt
```

# Получить Serial порты
```bash
python -m serial.tools.list_ports
```

# Запустить приложение
```bash
python charts.py
```

# Прочая информация

В файле input.txt хранится общий вид получаемых данных. Чтобы выключить режим считывания с файла, нужно:
    * изменить константу READING_MODE на 0;
    * получить порт, к которому подключено Arduino и изменить константу AVAILABLE_SERIAL_PORT на этот порт.
