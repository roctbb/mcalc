import json

example_calc = {
    "title": "Международный прогностический индекс лимфомы Ходжкина для поздних стадий",
    "info": [
        {
            "title": "Описание",
            "text": """О модели: Эта модель была разработана на основе подробных индивидуальных данных пациентов из объединенной когорты из 4027 пациентов, получавших лечение в восьми оригинальных международных клинических исследованиях классической лимфомы Ходжкина на поздней стадии, проведенных в 1996-2019 годах. Эффективность модели была подтверждена в когорте из 1431 пациента из четырех крупных проспективных когорт и регистров классической лимфомы Ходжкина."""
        },
        {
            "title": "Ссылки",
            "text": """Родди, Энджи Мэй. Парсонс, Сьюзан К. Апшоу, Дженика Н. Фридберг, Джонатан В. Галламини, Андреа. Хоукс, Элиза. Ходжсон, Дэвид. Джонсон, Питер. Линк, Брайан К. Привет, Эрик. Сэвидж, Керри Дж. Зинзани, Пьер Луиджи. Маурер, Мэтью. Ивенс, Эндрю М.

Международный прогностический индекс лимфомы Ходжкина на поздней стадии: Разработка и валидация модели клинического прогнозирования от Консорциума HoLISTIC.
Журнал клинической онкологии. 2022, 10 декабря. doi: 10.1200/JCO.22.02473. PMID: 36495588."""
        }
    ],
    "fields": [
        {
            "title": "Возраст",
            "description": "18 - 65 лет",
            "is_required": True,
            "code": "age",
            "limits": [
                {
                    "type": "min",
                    "value": 18
                },
                {
                    "type": "max",
                    "value": 65
                }
            ],
            "type": "int",
            "unit": "лет"
        },
        {
            "title": "Альбумин",
            "description": "От 10 до 60",
            "is_required": True,
            "code": "albumin",
            "limits": [
                {
                    "type": "min",
                    "value": 10
                },
                {
                    "type": "max",
                    "value": 60
                }
            ],
            "type": "int",
            "unit": "г/л"
        },
        {
            "title": "Массивный объем опухоли (больше 7 см)",
            "is_required": True,
            "type": "radio",
            "code": "bulk",
            "options": [
                {
                    "title": "Да",
                    "value": 1
                },
                {
                    "title": "Нет",
                    "value": 0
                }
            ]
        },
        {
            "title": "Пол",
            "is_required": True,
            "code": "female",
            "type": "radio",
            "options": [
                {
                    "title": "Женский",
                    "value": 1
                },
                {
                    "title": "Мужской",
                    "value": 0
                }
            ]
        },
        {
            "title": "Гемоглобин",
            "description": "От 50 до 165",
            "is_required": True,
            "code": "hemoglobin",
            "limits": [
                {
                    "type": "min",
                    "value": 50
                },
                {
                    "type": "max",
                    "value": 165
                }
            ],
            "type": "int",
            "unit": "г/л"
        },
        {
            "title": "Лимфоциты",
            "description": "От 0.1 до 5.0",
            "is_required": True,
            "code": "lymphocyte",
            "limits": [
                {
                    "type": "min",
                    "value": 0.1
                },
                {
                    "type": "max",
                    "value": 5.0
                }
            ],
            "type": "float",
            "unit": "10^9/л"
        },
        {
            "title": "Стадия",
            "is_required": True,
            "code": "stage",
            "type": "radio",
            "options": [
                {
                    "title": "Стадия IV",
                    "value": 4
                },
                {
                    "title": "Стадия III",
                    "value": 3
                },
                {
                    "title": "Стадия IIB",
                    "value": 2
                }
            ]
        }
    ],
    "results": [
        {
            "title": "Общая выживаемость через 5 лет",
            "code": "os",
            "unit": "%",
            "round": 2,
            "script": """
def calculate(data):
    from math import exp
    
    data['albumin'] = data['albumin'] / 10
    data['hemoglobin'] = data['hemoglobin'] / 10
    
    stage4 = data['stage'] == 4
    So5 = 0.9372773
    Sbx = -0.23395617 * data['female'] \
          + 0.26580226 * stage4 \
          + 0.2903614 * data['bulk'] \
          - 0.02039509 * data['age'] \
          + 0.06586394 * (max(data['age'], 30) - 30) \
          - 0.46322696 * data['lymphocyte'] \
          + 0.83241075 * (max(data['lymphocyte'], 2) - 2) \
          - 0.11580102 * data['hemoglobin'] \
          - 0.37859857 * data['albumin']

    Sbx0 = -3.515723

    return So5 ** exp(Sbx - Sbx0)      
"""
        },
        {
            "title": "Выживание без прогрессии через 5 лет",
            "code": "pfs",
            "unit": "%",
            "round": 2,
            "script": """
def calculate(data):
    from math import exp
    
    data['albumin'] = data['albumin'] / 10
    data['hemoglobin'] = data['hemoglobin'] / 10
    
    stage4 = data['stage'] == 4
    stage3 = data['stage'] == 3
    So5 = 0.778205
    Sbx = - 0.0235349 * data['age'] \
          + 0.03754181 * (max(data['age'], 30) - 30) \
          - 0.25541601 * data['lymphocyte'] \
          + 0.42244199 * (max(data['lymphocyte'], 2) - 2) \
          - 0.27362557 * data['albumin'] \
          + 0.18418918 * stage3 \
          + 0.37651968 * stage4

    Sbx0 = -1.689394

    return So5 ** exp(Sbx - Sbx0)          
"""
        }
    ]

}

if __name__ == "__main__":
    print(json.dumps(example_calc))