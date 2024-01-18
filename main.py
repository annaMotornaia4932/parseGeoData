
import requests
import json
import pandas as pd

MY_KEY = '9b8461cf-238f-4401-a367-02d76cf1fe21'
# 8271080c-47b9-4e73-b532-3aec88150bab  22e11d40-2b73-41b0-9b17-62235ce82ab6 дополнительный
listIn = [] # список в который будут записываться координаты
nameCoordJason = "" # в каждом наборе данных наименование атрибуту
def get_geoData(url, url1, url2, countItems):
    headers = {'user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                             'Version/16.3 Safari/605.1.15',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
               }
    resp = requests.get(url=url, headers=headers)
    current_page: int = 1

    while resp.status_code == 200:
        url = url1 + str(current_page) + url2
        resp = requests.get(url=url, headers=headers)
        print(current_page, resp.status_code)
        current_page = current_page + 1
        jsonData = json.loads(resp.text)
        global nameCoordJason

        for item in jsonData["results"]:
            if ("coord" in item["row"].keys()):
                listIn.append(item["row"]["coord"])
                countItems = countItems + 1
                nameCoordJason = "coord"
            if ("longitude" in item["row"].keys()):
                listIn.append(item["row"]["longitude"])
                countItems = countItems + 1
                nameCoordJason = "longitude"
            if ("longitude_latitude" in item["row"].keys()):
                listIn.append(item["row"]["longitude_latitude"])
                countItems = countItems + 1
                nameCoordJason = "longitude_latitude"
            if ("coordinates" in item["row"].keys()):
                listIn.append(item["row"]["coordinates"])
                countItems = countItems + 1
                nameCoordJason = "coordinates"
            if ("coordinates_direct_track" in item["row"].keys()):
                listIn.append(item["row"]["coordinates_direct_track"])
                countItems = countItems + 1
                nameCoordJason = "coordinates_direct_track"

        url = url1 + str(current_page) + url2
        resp = requests.get(url=url, headers=headers)

    df = pd.DataFrame(listIn)
    df.to_excel('./coordinates.xlsx')
    return countItems

def countCoordFunction(countCoord):
    strCoord = ""
    count1 = 0
    count2 = 0
    count3 = 0

    for item in listIn:
        strCoord = str(item)
        print(strCoord)
        strCoord = strCoord.replace("[", "")
        strCoord = strCoord.replace("]", "")
        URL = ('https://geocode-maps.yandex.ru/1.x/?apikey=' + MY_KEY +
               '&geocode=' + strCoord + '&sco=latlong&format=json')
        resp = requests.get(URL)
        jsonData = json.loads(resp.text)
        jsonData1 = jsonData.get("response").get("GeoObjectCollection").get("featureMember")

        if (jsonData1[1].get("GeoObject").get("metaDataProperty").get("GeocoderMetaData").
                get("Address").get("country_code") == "RU"):
            count1 += 1

        jsonData2 = jsonData1[1].get("GeoObject").get("metaDataProperty").get("GeocoderMetaData").get("Address").get("Components")
        #print(jsonData2)

        if (jsonData2[2].get("name") == "Ленинградская область" or jsonData2[2].get("name") == "Санкт-Петербург"):
            count2 += 1

        if (jsonData2[2].get("name") == "Санкт-Петербург"):
            count3 += 1

    countCoord = [count1, count2, count3]
    return countCoord
def parse_geoData():
    #---------------------------------------------------------------------------------------------------------------
    # countItems = 0
    # countCoord = [0, 0, 0]
    # finishTable = []
    # url = (
    #     'https://data.gov.spb.ru/api/public/version/4593/structure_version/157/?search_all=%D0%B4%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D1%80%D0%B8%D0%BC&page=1&obj_type=&name=&short_name=&name_en=&type=&address_manual=&phone=&www=&email=&description=&description_en=&obj_history=&obj_history_en=&obj_hints=&work_time=&work_time_en=&data_display=&per_page=50'
    # )
    # url1 = ('https://data.gov.spb.ru/api/public/version/4593/structure_version/157/?search_all=%D0%B4%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D1%80%D0%B8%D0%BC&page='
    #         )
    # url2 = (
    #     '&obj_type=&name=&short_name=&name_en=&type=&address_manual=&phone=&www=&email=&description=&description_en=&obj_history=&obj_history_en=&obj_hints=&work_time=&work_time_en=&data_display=&per_page=50'
    # )
    # countItems = get_geoData(url, url1, url2, countItems)
    # countCoord = countCoordFunction(countCoord)
    # result = ({"Название набора данных": 'Достопримечательности',
    #                             "Ссылка на набор данных": str(url),
    #                             "Количество записей в наборе": str(countItems),
    #                             "Название столбца с координатами": str(nameCoordJason),
    #                             "Колич коорд на терр РФ": str(countCoord[0]),
    #                             "Колич коорд в ЛО или СПб": str(countCoord[1]),
    #                             "Колич коорд в пределах СПб": str(countCoord[2])
    #                 })
    # finishTable.append(result)

    # ----------------------------------------------- 1 ----------------------------------------------------------------
    # 26 записей
    countItems = 0
    countCoord = [0, 0, 0]
    finishTable = []
    url = (
        'https://data.gov.spb.ru/api/public/version/4509/structure_version/407/?page=1&number=&district=&name=&chief=&address=&phone=&email=&nearest_subway_station=&data_display=&per_page=50'
    )
    url1 = ('https://data.gov.spb.ru/api/public/version/4509/structure_version/407/?page='
            )
    url2 = (
        '&number=&district=&name=&chief=&address=&phone=&email=&nearest_subway_station=&data_display=&per_page=50'
    )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({"Название набора данных": 'Информация о народных дружинах Санкт-Петербурга',
                                "Ссылка на набор данных": str(url),
                                "Количество записей в наборе": str(countItems),
                                "Название столбца с координатами": str(nameCoordJason),
                                "Колич коорд на терр РФ": str(countCoord[0]),
                                "Колич коорд в ЛО или СПб": str(countCoord[1]),
                                "Колич коорд в пределах СПб": str(countCoord[2])
                    })
    finishTable.append(result)

    # -----------------------------------------------2 ----------------------------------------------------------------
    # 109 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = ('https://data.gov.spb.ru/api/public/version/4858/structure_version/649/?page=1&name=&name_en=&type=&address_manual=&phone=&www=&email=&for_disabled=&ogrn=&inn=&data_display=&per_page=50')
    url1 = ('https://data.gov.spb.ru/api/public/version/4858/structure_version/649/?page=')
    url2 = ('&name=&name_en=&type=&address_manual=&phone=&www=&email=&for_disabled=&ogrn=&inn=&data_display=&per_page=50')
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Театры',   # 109 записей
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
        })
    finishTable.append(result)

    # -----------------------------------------------3 ----------------------------------------------------------------
    # 29 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = ('https://data.gov.spb.ru/api/public/version/3994/structure_version/415/?page=1&name=&the_address=&phone=&link=&logo=&data_display=&per_page=50')
    url1 = ('https://data.gov.spb.ru/api/public/version/3994/structure_version/415/?page=')
    url2 = ('&name=&the_address=&phone=&link=&logo=&data_display=&per_page=50')
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Рестораны-участники проекта «Петербургская кухня»',   # 29 записей
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
        })
    finishTable.append(result)

    # 248 записей
    # countItems = 0
    # countCoord = [0, 0, 0]
    # url = ('https://data.gov.spb.ru/api/public/version/4856/structure_version/569/?page=1&name=&name_en=&type=&country=&address_manual=&district=&phone=&www=&email=&description=&description_en=&work_time=&for_disabled=&ogrn=&inn=&data_display=&per_page=50')
    # url1 = ('https://data.gov.spb.ru/api/public/version/4856/structure_version/569/?page=')
    # url2 = ('&name=&name_en=&type=&country=&address_manual=&district=&phone=&www=&email=&description=&description_en=&work_time=&for_disabled=&ogrn=&inn=&data_display=&per_page=50')
    # countItems = get_geoData(url, url1, url2, countItems)
    # countCoord = countCoordFunction(countCoord)
    # result = ({
    #     "Название набора данных": 'Рестораны-участники проекта «Музеи»',
    #     "Ссылка на набор данных": str(url),
    #     "Количество записей в наборе": str(countItems),
    #     "Название столбца с координатами": nameCoordJason,
    #     "Колич коорд на терр РФ": str(countCoord[0]),
    #     "Колич коорд в ЛО или СПб": str(countCoord[1]),
    #     "Колич коорд в пределах СПб": str(countCoord[2])
    #     })
    # finishTable.append(result)

    #---------------------------------------------- ----------------------------------------------------------------

    # 8 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = ('https://data.gov.spb.ru/api/public/version/5136/structure_version/188/?page=1&name=&abbreviated_name=&address=&district=&nearest_subway_station=&chief=&web_site=&phone=&fax=&inn=&ogrn=&note=&data_display=&per_page=50')
    url1 = ('https://data.gov.spb.ru/api/public/version/5136/structure_version/188/?page=')
    url2 = ('&name=&abbreviated_name=&address=&district=&nearest_subway_station=&chief=&web_site=&phone=&fax=&inn=&ogrn=&note=&data_display=&per_page=50')
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({"Название набора данных": 'Вокзалы',
               "Ссылка на набор данных": str(url),
               "Количество записей в наборе": str(countItems),
               "Название столбца с координатами": nameCoordJason,
               "Колич коорд на терр РФ": str(countCoord[0]),
               "Колич коорд в ЛО или СПб": str(countCoord[1]),
               "Колич коорд в пределах СПб": str(countCoord[2])
                    })
    finishTable.append(result)

    # --------------------------------------------------------------------------------------------------------------
    # 248 записей
    # countItems = 0
    # countCoord = [0, 0, 0]
    # url = ('https://data.gov.spb.ru/api/public/version/5138/structure_version/645/?search_all='
    #        '%D0%BF%D1%80%D0%BE%D0%B5%D0%B7%D0%B4%D0%B0&page=1&route_long_name='
    #        '&route_short_name=&type_communication=&name_streets_roads=&stop_name='
    #        '&direction=&procedure_stops=&cost_day=&cost_evening=&type_transportation_tariff='
    #        '&first_time_out=&last_time_out=&transport_type=&transport_class='
    #        '&environmental_transport=&category_persons_benefits=&name_legal_entity='
    #        '&location_carrier=&carrier_phone=&responsible_department=&tel_responsible_department='
    #        '&coordinates_direct_track=&coordinates_reverse_track=&data_display=&per_page=50')
    # url1 = ('https://data.gov.spb.ru/api/public/version/5138/structure_version/645/?search_all='
    #        '%D0%BF%D1%80%D0%BE%D0%B5%D0%B7%D0%B4%D0%B0&page=')
    # url2 = ('&route_long_name='
    #        '&route_short_name=&type_communication=&name_streets_roads=&stop_name='
    #        '&direction=&procedure_stops=&cost_day=&cost_evening=&type_transportation_tariff='
    #        '&first_time_out=&last_time_out=&transport_type=&transport_class='
    #        '&environmental_transport=&category_persons_benefits=&name_legal_entity='
    #        '&location_carrier=&carrier_phone=&responsible_department=&tel_responsible_department='
    #        '&coordinates_direct_track=&coordinates_reverse_track=&data_display=&per_page=50')
    # countItems = get_geoData(url, url1, url2, countItems)
    # countCoord = countCoordFunction(countCoord)
    # result = ({"Название набора данных": 'Информация о лечебно-профилактических '
    #                                      'учреждениях Санкт-Петербурга (Версия №11 от 28.06.2023)',
    #            "Ссылка на набор данных": str(url),
    #            "Количество записей в наборе": str(countItems),
    #            "Название столбца с координатами": nameCoordJason,
    #            "Колич коорд на терр РФ": str(countCoord[0]),
    #            "Колич коорд в ЛО или СПб": str(countCoord[1]),
    #            "Колич коорд в пределах СПб": str(countCoord[2])
    #                 })
    # finishTable.append(result)

    # ---------------------------------------------------------------------------------------------------------
    # 548 записей
    # countItems = 0
    # countCoord = [0, 0, 0]
    # url = ('https://data.gov.spb.ru/api/public/version/5138/structure_version/645/?search_all='
    #        '%D0%BF%D1%80%D0%BE%D0%B5%D0%B7%D0%B4%D0%B0&page=1&route_long_name=&route_short_name='
    #        '&type_communication=&name_streets_roads=&stop_name=&direction=&procedure_stops='
    #        '&cost_day=&cost_evening=&type_transportation_tariff=&first_time_out=&last_time_out='
    #        '&transport_type=&transport_class=&environmental_transport=&category_persons_benefits='
    #        '&name_legal_entity=&location_carrier=&carrier_phone=&responsible_department='
    #        '&tel_responsible_department=&coordinates_direct_track=&coordinates_reverse_track='
    #        '&data_display=&per_page=50')
    # url1 = ('https://data.gov.spb.ru/api/public/version/5138/structure_version/645/?search_all='
    #        '%D0%BF%D1%80%D0%BE%D0%B5%D0%B7%D0%B4%D0%B0&page=')
    # url2 = ('&route_long_name=&route_short_name='
    #        '&type_communication=&name_streets_roads=&stop_name=&direction=&procedure_stops='
    #        '&cost_day=&cost_evening=&type_transportation_tariff=&first_time_out=&last_time_out='
    #        '&transport_type=&transport_class=&environmental_transport=&category_persons_benefits='
    #        '&name_legal_entity=&location_carrier=&carrier_phone=&responsible_department='
    #        '&tel_responsible_department=&coordinates_direct_track=&coordinates_reverse_track='
    #        '&data_display=&per_page=50')
    # countItems = get_geoData(url, url1, url2, countItems)
    # countCoord = countCoordFunction(countCoord)
    # result = ({"Название набора данных": 'Перечень маршрутов и тарифов проезда в '
    #                                      'общественном транспорте (Версия №23 от 22.08.2023)',
    #            "Ссылка на набор данных": str(url),
    #            "Количество записей в наборе": str(countItems),
    #            "Название столбца с координатами": nameCoordJason,
    #            "Колич коорд на терр РФ": str(countCoord[0]),
    #            "Колич коорд в ЛО или СПб": str(countCoord[1]),
    #            "Колич коорд в пределах СПб": str(countCoord[2])
    #                 })
    # finishTable.append(result)
    # ----------------------------------------------- 5 ----------------------------------------------------------------
    # 110 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = ('https://data.gov.spb.ru/api/public/version/5142/structure_version/619/?search_all='
           '%D0%BD%D0%B0%D0%B7%D0%B5%D0%BC&page=1&name=&type=&address=&district='
           '&nearest_subway_station=&chief=&phone=&fax=&note=&coordinates=&data_display='
           '&per_page=50'
           )
    url1 = ('https://data.gov.spb.ru/api/public/version/5142/structure_version/619/?search_all='
           '%D0%BD%D0%B0%D0%B7%D0%B5%D0%BC&page=')
    url2 = ('&name=&type=&address=&district='
           '&nearest_subway_station=&chief=&phone=&fax=&note=&coordinates=&data_display='
           '&per_page=50'
            )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Точки продаж билетов для проезда на наземном городском'
                                  ' пассажирском транспорте (Версия №27 от 22.08.2023)',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
        })
    finishTable.append(result)
    # ----------------------------------------------- 6 ----------------------------------------------------------------
    # 114 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = (
        'https://data.gov.spb.ru/api/public/version/4365/structure_version/310/?search_all=%D0%BD%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE&page=1&name=&territorial_status=&address=&district=&nearest_subway_station=&chief=&phone=&fax=&e-mail=&data_display=&per_page=50')
    url1 = ('https://data.gov.spb.ru/api/public/version/4365/structure_version/310/?search_all=%D0%BD%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE&page=')
    url2 = (
        '&name=&territorial_status=&address=&district=&nearest_subway_station=&chief=&phone=&fax=&e-mail=&data_display=&per_page=50'
        )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Информация о национально-культурных объединениях, '
                                  'национально-культурных автономиях и казачьих обществах'
                                  ' Санкт-Петербурга (Версия №7 от 19.04.2023)',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
    })
    finishTable.append(result)
    # ----------------------------------------------- 7 ----------------------------------------------------------------
    # 108 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = (
       'https://data.gov.spb.ru/api/public/version/5227/structure_version/387/?search_all=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D1%81&page=1&name=&address_yur=&address_fact=&phone=&email=&site=&data_display=&per_page=50'
    )
    url1 = ('https://data.gov.spb.ru/api/public/version/5227/structure_version/387/?search_all=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D1%81&page=')
    url2 = (
        '&name=&address_yur=&address_fact=&phone=&email=&site=&data_display=&per_page=50'
    )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Перечень ресурсоснабжающих организаций - владельцев'
                                  ' сетей инженерно-технического обеспечения и электрических'
                                  ' сетей в Санкт-Петербурге (Версия №12 от 03.07.2023)',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
    })
    finishTable.append(result)
    # ----------------------------------------------- 8 ----------------------------------------------------------------
    # 10 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = ('https://data.gov.spb.ru/api/public/version/5192/structure_version/401/?page=1&name=&abbreviated_name=&address=&district=&nearest_subway_station=&chief=&phone=&fax=&mode=&email=&web_site=&activity=&data_display=&per_page=50'
           )
    url1 = ('https://data.gov.spb.ru/api/public/version/5192/structure_version/401/?page=')
    url2 = (
        '&name=&abbreviated_name=&address=&district=&nearest_subway_station=&chief=&phone=&fax=&mode=&email=&web_site=&activity=&data_display=&per_page=50'
    )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Информация о государственных казенных учреждениях, подведомственных Архивному комитету Санкт-Петербурга',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
    })
    finishTable.append(result)

    # ----------------------------------------------- 9 ----------------------------------------------------------------
    # 24 записи
    countItems = 0
    countCoord = [0, 0, 0]
    url = (
        'https://data.gov.spb.ru/api/public/version/4854/structure_version/151/?search_all=%D0%B2%D1%8B%D1%81%D1%82%D0%B0%D0%B2%D0%BE%D1%87&page=1&name=&name_en=&type=&address_manual=&phone=&www=&email=&description=&description_en=&for_disabled=&data_display=&per_page=50'
    )
    url1 = ('https://data.gov.spb.ru/api/public/version/4854/structure_version/151/?search_all=%D0%B2%D1%8B%D1%81%D1%82%D0%B0%D0%B2%D0%BE%D1%87&page=')
    url2 = (
        '&name=&name_en=&type=&address_manual=&phone=&www=&email=&description=&description_en=&for_disabled=&data_display=&per_page=50'
    )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Выставочные залы (Версия №10 от 29.06.2023)',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
    })
    finishTable.append(result)
    # ----------------------------------------------- 10 ---------------------------------------------------------
    #77 записей
    countItems = 0
    countCoord = [0, 0, 0]
    url = (
        'https://data.gov.spb.ru/api/public/version/4855/structure_version/159/?search_all=%D0%BA%D0%B8%D0%BD%D0%BE&page=1&name=&type=&address=&district=&phone=&www=&email=&for_disabled=&data_display=&per_page=50'
    )
    url1 = ('https://data.gov.spb.ru/api/public/version/4855/structure_version/159/?search_all=%D0%BA%D0%B8%D0%BD%D0%BE&page=')
    url2 = (
        '&name=&type=&address=&district=&phone=&www=&email=&for_disabled=&data_display=&per_page=50'
    )
    countItems = get_geoData(url, url1, url2, countItems)
    countCoord = countCoordFunction(countCoord)
    result = ({
        "Название набора данных": 'Кинотеатры (Версия №10 от 29.06.2023)',
        "Ссылка на набор данных": str(url),
        "Количество записей в наборе": str(countItems),
        "Название столбца с координатами": nameCoordJason,
        "Колич коорд на терр РФ": str(countCoord[0]),
        "Колич коорд в ЛО или СПб": str(countCoord[1]),
        "Колич коорд в пределах СПб": str(countCoord[2])
    })
    finishTable.append(result)

    dfFinish = pd.DataFrame(finishTable)
    dfFinish.to_excel('./finishtable.xlsx')

if __name__=='__main__':
        parse_geoData()
