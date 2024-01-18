# parseGeoData
Parsing data.gov.spb.ru getting geo data and analyze data with yandex geocoder
-----------------------------
Программа парсинга наборов данных с получением координат организаций с последующем анализом метаданных полученных с Яндекс ГеоКодера по этим координатам.

## Задание:
* Выбрать 10 наборов данных с сайта https://classif.gov.spb.ru/, в которых присутствует поле с координатами, из них 7 наборов должны содержать не менее 100 записей (строк)
* Написать код на Python для анализа координат. Входные данные: файл с набором данных из п. 1 и название столбца с координатами. Выходные данные: таблица со столбцами "название набора данных", "ссылка на набор данных", "количество записей в наборе", "название столбца с координатами", "количество координат, расположенных на территории РФ", "количество координат, расположенных на территории Ленинградской области или СПб", "количество координат, расположенных в пределах СПб"

* Для проверки соответствия координат географическому региону следует использовать геокодер, например, геокодер Яндекса (до 1000 запросов в сутки).

* Результаты работы программы будут приведены в таблицах Excel файлов, а именно, полученные координыты - coordinates.xlsx, анализ данных - finishTable.xlsx
