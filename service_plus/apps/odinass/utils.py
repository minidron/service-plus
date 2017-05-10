import os

from xml.etree import cElementTree as ET


class ImportManager(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.import_all()

    def _get_tree(self):
        if self.tree is not None:
            return self.tree
        if not os.path.exists(self.file_path):
            message = 'File doesn\'t exist: %s' % self.file_path
            raise OSError(message)
        return ET.parse(self.file_path)

    def _parse_groups(self, node):
        """
        Загрузка Групп товаров
        """
        groups = []
        stack = node.findall('Группы/Группа')
        while len(stack):
            item = stack.pop(0)
            if isinstance(item, tuple):
                item, parent = item
            else:
                parent = None

            groups.append({
                'id': item.find('Ид').text,
                'name': item.find('Наименование').text,
                'parent': parent.find('Ид').text if parent else None,
            })

            stack = [(group, item)
                     for group in item.findall('Группы/Группа')] + stack
        return groups

    def _parse_properties(self, node):
        """
        Загрузка Свойств и ВариантыЗначений
        """
        properties = []
        for property_node in node.findall('Свойства/Свойство'):
            value_type = property_node.find('ТипЗначений').text
            property_item = {
                'id': property_node.find('Ид').text,
                'name': property_node.find('Наименование').text,
                'value_type': value_type,
            }

            value_options = []
            for value_option in property_node.findall(
                    'ВариантыЗначений/%s' % value_type):
                value_options.append({
                    'id': value_option.find('ИдЗначения').text,
                    'value': value_option.find('Значение').text,
                })
            property_item['value_options'] = value_options
            properties.append(property_item)
        return properties

    def import_all(self):
        self.import_classifier()

    def import_classifier(self):
        tree = self._get_tree()
        classifier = tree.find('Классификатор')
        if classifier is not None:
            self._parse_groups(classifier)
            self._parse_properties(classifier)
