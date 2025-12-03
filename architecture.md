Yarn/
├── config/
│   ├── workspaces/                     # простраства и их данные
│   │   ├── other.json
│   │   ├── personal.json
│   │   └── work.json
│   │
│   ├── btn_settings_config.json        # для aside_logic.py, содержит состояние кнопок
│   ├── config.json                     # Конфигурации
│   └── tabs_config.json                # Хранит ссылки и названия вкладок которые вызывает tabs.py
│
├── src/
│   ├── __init__.py
│   ├── main.py                         # Точка входа
│   ├── app/
│   │   ├── __init__.py
│   │   └── main_window.py              # Главное окно
│   │
│   ├── manifests/
│   │   ├── __init__.py
│   │   └── platform_manifests.py       # кроссплатформенные настройки приложения
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_manager.py             # Управление файлами
│   │   └── syntax_highlighter.py       # Подсветка синтаксиса
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── aside_manager.py            # манипуляция состояний кнопок из aside
│   │   ├── color_utils.py              # Манипуляции с цветом (hex)
│   │   ├── helpers.py                  # Вспомогательные функции
│   │   └── terms_manager.py            # Принятие условий пользования
│   │
│   └── widgets/
│       ├── __init__.py
│       ├── aside_panels/
│       │   ├── __init__.py
│       │   ├── plugins.py              # запуск вкладки plugins из aside
│       │   ├── settings.py             # ... settings из aside
│       │   ├── tools.py                # ... tools из aside
│       │   └── workspaces.py           # ... workspaces из aside
│       │
│       ├── aside.py                    # боковая панель
│       ├── header.py       	        # Шапка
│       ├── tabs.py		                # Вкладки
│       ├── text_editor.py              # Кастомный текстовый редактор
│       └── window_resize.py            # Обработчик изменения размера окна
│
├── resources/
│   ├── fonts/
│   │   ├── basic_fonts.json            # Базовые стили для текста
│   │   └── .json                       # Планируеться пользовательские, пока нет
│   │
│   ├── themes/
│   │   ├── dark_theme.json
│   │   ├── light_theme.json
│   │   └── .json                       # Планируеться пользовательские, пока нет
│   │
│   └── icons/     		                # Иконки в ico и png
│
├── tests/
├── requirements.txt
└── README.md