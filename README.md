# GA4RoboTrailer

## Описание проекта

Этот проект посвящен использованию генетических алгоритмов для управления мобильным роботом с прицепом в среде с препятствиями. Основная цель — найти оптимальную траекторию движения робота от начальной точки до конечной, избегая столкновений с препятствиями.

## Структура репозитория

- `data/`: Содержит JSON-файлы с результатами экспериментов.
- `src/`: Содержит исходный код проекта.
  - `optimize.py`: Основной скрипт для запуска генетического алгоритма.
  - `plotting.py`: Скрипт для визуализации траекторий.
  - `ga_results_analyzer.py`: Скрипт для анализа результатов экспериментов.
- `images/`: Содержит изображения для `README.md`.
  - `images_235/`: Изображения для запуска с параметрами 235.
  - `images_255/`: Изображения для запуска с параметрами 255.
  - `images_310/`: Изображения для запуска с параметрами 310.

## Установка и запуск

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/ваш-username/GeneticRoboNav.git
   cd GA4RoboTrailer

2. Установите необходимые зависимости:
    ```sh
    pip install -r requirements.txt

3. Запустите основной скрипт:
    ```sh
    python src/optimize.py

## Примеры работы:

<p align="center">
  <img src="https://github.com/Belladonna03/telebot-currency-rates/blob/master/data/first_best.png" width="30%" />
  <img src="https://github.com/Belladonna03/telebot-currency-rates/blob/master/data/second_best.png" width="30%" />
  <img src="https://github.com/Belladonna03/telebot-currency-rates/blob/master/data/third_best.png" width="30%" />
</p>

