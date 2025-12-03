# Yarn

Yarn is a lightweight text editor built with Python and the PySide6 framework. It is designed for note-taking and text editing with a focus on customization, clean interface, and open-source development.

Yarn — это лёгкий текстовый редактор, созданный на Python с использованием фреймворка PySide6. Он предназначен для ведения заметок и редактирования текста с акцентом на кастомизацию, чистый интерфейс и открытую разработку.



> [!NOTE]
> **Acknowledgements | Благодарности**
>
> This project is made possible thanks to the incredible work of the [Python](https://www.python.org/) and [Qt for Python (PySide6)](https://wiki.qt.io/Qt_for_Python) development communities.
>
> Проект стал возможным благодаря невероятной работе сообществ [Python](https://www.python.org/) и [Qt for Python (PySide6)](https://wiki.qt.io/Qt_for_Python).



> [!TIP]
> **Technologies | Технологии**
>
> - **Python 3.7+**
> - **PySide6**



> [!IMPORTANT]
> **Author | Автор**
>
> [otkruchenyy](https://github.com/otkruchenyy)
> 
> [tg_channel](https://t.me/+BTSVg57miuhiNDQy)



> [!IMPORTANT]
> Requires Python 3.7+ (compatible with PySide6). | Требуется Python 3.7+ (совместимо с PySide6).

> [!WARNING]
> Before installation, review the [**license agreement**](LICENSE.txt).
> Перед установкой ознакомьтесь с [**лицензионным соглашением**](LICENSE.txt).

## Installation | Установка
```bash
git clone https://github.com/otkruchenyy/Yarn.git
cd Yarn
python -m venv venv
pip install -r requirements.txt
```

## Running the Application | Запуск приложения
**Linux/Mac:**
```bash
source venv/bin/activate
python src/main.py
```

**Windows:**
```bash
venv\Scripts\activate
python src/main.py
```



> [!NOTE]
> ## Fonts | Шрифты
>
> This project uses the following font families, which are licensed under the [SIL Open Font License (OFL) Version 1.1](https://openfontlicense.org/):
>
> Данный проект использует следующие семейства шрифтов, лицензированные по [SIL Open Font License (OFL) Версия 1.1](https://openfontlicense.org/):
> 
> *   **Open Sans** – [Copyright 2020 The Open Sans Project Authors](https://github.com/googlefonts/opensans)
> *   **Unbounded** – [Copyright 2022 The Unbounded Project Authors](https://github.com/googlefonts/unbounded)
> 
> **Location of font-specific license files:**
> Each font's individual copyright notice and license information can be found in its respective directory:
> *   Open Sans: [`fonts/opensans/`](./resources/fonts/Open_Sans/)
> *   Unbounded: [`fonts/unbounded/`](./resources/fonts/Unbounded/)
> 
> **Расположение файлов с лицензиями для конкретных шрифтов:**
> Уведомления об авторских правах и информация о лицензии для каждого шрифта находятся в соответствующих директориях:
> *   Open Sans: [`fonts/opensans/`](./resources/fonts/Open_Sans/)
> *   Unbounded: [`fonts/unbounded/`](./resources/fonts/Unbounded/)
> 
> Each directory contains a `OFL.txt` or similar file with the specific attribution required by the license.
>
> Каждая директория содержит файл `OFL.txt` или аналогичный, с указанием конкретной информации об авторских правах, требуемой лицензией.



> [!WARNING]
> ## Future Font Management & Legal Disclaimer | Управление шрифтами и юридическое уведомление
>
> The application is designed to support user-provided font files in future updates. While this functionality empowers customization, please be advised:
>
> Приложение спроектировано с возможностью поддержки пользовательских файлов шрифтов в будущих обновлениях. Эта функция дает возможности для кастомизации, однако обратите внимание:
>
>
> **User Responsibility for Licensing | Ответственность пользователя за лицензирование**
>
> The addition and use of third-party fonts within the application is the sole responsibility of the user. You must ensure that any font you install and use is appropriately licensed for such embedding, distribution, and/or modification, as dictated by its specific license (e.g., OFL, Apache 2.0, commercial license). Any legal consequences arising from the use of improperly licensed fonts shall be borne solely by the user.
>
> Ответственность пользователя за лицензирование: Добавление и использование сторонних шрифтов в приложении является исключительной ответственностью пользователя. Вы обязаны убедиться, что любой устанавливаемый и используемый вами шрифт имеет соответствующую лицензию для такого внедрения, распространения и/или модификации, как того требует его конкретная лицензия (например, OFL, Apache 2.0, коммерческая лицензия). Все правовые последствия, возникшие в результате использования шрифтов с ненадлежащей лицензией, несет исключительно пользователь.
>
>
> **No Liability for User Content | Отказ от ответственности за пользовательский контент**
>
> The authors and maintainers of this project expressly disclaim any liability for user-provided content, including font files. We are not responsible for verifying font licenses, and we cannot be held liable for any copyright infringement or licensing violations that may occur from a user's actions.
>
> Отказ от ответственности за пользовательский контент: Авторы и сопровождающие данного проекта прямо отказываются от любой ответственности за контент, предоставленный пользователями, включая файлы шрифтов. Мы не отвечаем за проверку лицензий шрифтов и не можем нести ответственность за любое нарушение авторских прав или условий лицензирования, которое может произойти в результате действий пользователя.
>
>
> **Intended Use | Предполагаемое использование**
>
> This tool is intended for use with properly licensed, freely distributable fonts (such as those under OFL). Using fonts in violation of their license terms is a breach of this project's intended purpose and may constitute copyright infringement.
>
> Предполагаемое использование: Данный инструмент предназначен для работы с правомерно лицензированными, свободно распространяемыми шрифтами (например, распространяемыми по лицензии OFL). Использование шрифтов с нарушением условий их лицензии противоречит предполагаемому назначению проекта и может являться нарушением авторских прав.