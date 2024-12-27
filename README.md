Стаханов v. 0.2 выходит на мировые рынки с новым веб-интерфейсом. Тот же самый (ну, почти) исходный код сканера в новом виде.

Запуск, как обычно, по http://127.0.0.1:8000/

Результаты сканирования теперь попадают напрямую в базу Django, а все страницы со статистикой считаются на основе данных базы.
Вот какие страницы есть:
- Главная. Там можно указать путь для сканирования, посмотреть дату последнего скана и общий объем файлов, а также очистить базу (чтобы посканировать что-то еще, например).
- Статистика файлов по расширениям
- Топ самых больших файлов по размеру
- Топ самых больших изображений по произведению ширина x высота
- Топ PDF-документов по количеству страниц в них

Все URL внутренних страниц построены по принципу http://127.0.0.1:8000/stknapp/top/X/bydimensions/, где X можно варьировать прямо в адресе. Прикручены сниппеты и CSS-стили из Bootstrap. Есть какая-никакая обработка ошибок и фидбек пользователю о происходящем.

А еще теперь есть три модуля тестирования и HTML-документация в http://127.0.0.1:8000/docs/build/html/index.html.