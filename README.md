# YaCut

Сервис - укоротитель ссылок. Позволяет сгенерировать короткую ссылку на основе пользовательской длинной ссылки на ресурс.

# Технологии

* Python
* Flask
* SQLAlchemy

#  Локальный запуск проекта

* Клонируем репозиторий на локальный компьютер ```git clone https://github.com/nmutovkin/yacut.git```

* Переходим в папку репозитория ```cd yacut```

* Cоздаем и активируем виртуальное окружение:
    ```
    python3 -m venv venv
    ```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

* Устанавливаем зависимости из файла requirements.txt:

    ```
    python3 -m pip install --upgrade pip
    ```
    
    ```
    pip install -r requirements.txt
    ```

Сервис будет доступен по ссылке ```http://127.0.0.1:5000/```

# Автор

Никита Мутовкин
