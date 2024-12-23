# Конфигурационное управление домашнее задание номер 4
# Скляр Матвей ИКБО-62-23

# Описание

Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее. Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.
Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.
Форматом для файла-лога и файла-результата является csv.
Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу.


Загрузка константы

![image](https://github.com/user-attachments/assets/4eeed1c1-1778-430b-8dde-3a4ece8de5d9)


Размер команды: 5 байт. Операнд: поле B. Результат: регистр-аккумулятор.
Тест (A=111, B=195): 0xEF, 0x61, 0x00, 0x00, 0x00


Чтение значения из памяти

![image](https://github.com/user-attachments/assets/9adf17d6-06a4-4975-8065-a3af8e6a9e7d)


Размер команды: 5 байт. Операнд: значение в памяти по адресу, которым является поле B. Результат: регистр-аккумулятор.
Тест (A=46, B=218): 0x2E, 0x6D, 0x00, 0x00, 0x00


Запись значения в память

![image](https://github.com/user-attachments/assets/a6855a97-5aa6-4285-9e49-27987d2b6481)


Размер команды: 5 байт. Операнд: регистр-аккумулятор. Результат: значение в памяти по адресу, которым является поле B.
Тест (A=116, B=303): 0xF4, 0x97, 0x00, 0x00, 0x00


Бинарная операция: "!="

![image](https://github.com/user-attachments/assets/d5316c0d-57c4-4277-a82a-a95893c2ddc5)


Размер команды: 5 байт. Первый операнд: регистр-аккумулятор. Второй операнд: значение в памяти по адресу, которым является поле B. Результат: регистр-аккумулятор.
Тест (A=42, B=930): 0x2A, 0xD1, 0x01, 0x00, 0x00

# Установка
```
git clone https://github.com/Sttalkerr/homeworks/tree/main/4DZ.git
```
# Запуск
```
python assembler.py input.asm output_program.bin result.csv
python interpreter.py output_program.bin result.csv 0 350
```
