import requests
import constants
from bs4 import BeautifulSoup


def get_value(element, param):
    if param is None:
        return element.text
    else:
        if param == 'href':
            return constants.DEFAULT_URL + element[param]
        else:
            return element[param]


def get_updated_text(src, title, tag_type, tag_class, object_xml, param):
    if object_xml.find(tag_type, tag_class) is None:
        return ''

    if not tag_class is None:
        value = get_value(object_xml.find(tag_type, tag_class), param)
    else:
        value = get_value(object_xml.find(tag_type), param)

    return src + title + ': ' + value + '\n'


def get_skin(object_xml):
    skin = {'image': object_xml.find('img')['src'], 'text': ''}
    skin['text'] = get_updated_text(skin['text'], '💬 Название', 'div', 'ItemPreview-itemName', object_xml, None)
    skin['text'] = get_updated_text(skin['text'], '📋 Тип', 'div', 'ItemPreview-itemTitle', object_xml, None)
    skin['text'] = get_updated_text(skin['text'], '📖 Описание', 'div', 'ItemPreview-itemText', object_xml, None)
    skin['text'] = get_updated_text(skin['text'], '⚙ Состояние', 'div', 'WearBar-value', object_xml, None)
    skin['text'] = skin['text'] + '\n'
    skin['text'] = get_updated_text(skin['text'], '✅ Скидка', 'span', None, object_xml, None)
    skin['text'] = get_updated_text(skin['text'], '💰 Итоговая цена', 'div', 'Tooltip-link', object_xml, None)
    skin['text'] = get_updated_text(skin['text'], '📌 Ссылка', 'a', 'ItemPreview-href', object_xml, 'href')
    skin['text'] = skin['text'] + '\n'
    return skin


def get_all_skins():
    skins = []
    r = requests.get(constants.URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    objects_xml = soup.find_all('div', class_='ItemPreview ItemPreview--grid ItemPreview--id-730')
    for object_xml in objects_xml:
        skins.append(get_skin(object_xml))
    return skins
