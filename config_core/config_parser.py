import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

path_settings = 'settings.ini'


def get_config(path: str) -> configparser.ConfigParser:
    """
    :param path: Путь к файлу конфигурации
    :return: Возращает объект с конфигурацией
    """
    config = configparser.ConfigParser()
    if not os.path.exists(path):    # Если нет файла с конфигурацией, то создать новый
        config = create_config(path)
    config.read(path, encoding='UTF-8')
    return config


def create_config(path: str) -> configparser.ConfigParser:
    """
    :param path: Путь к файлу конфигурации
    :return: Возращает новый объект с конфигурацией
    """
    config = configparser.ConfigParser()
    config.add_section('Server')
    config.set('Server', 'login', '')
    config.set('Server', 'password', '')
    config.set('Server', 'smtp_server', 'mail.nic.ru')
    config.set('Server', 'smtp_port', '587')
    config.add_section('Global')
    config.set('Global', 'interval', '10')
    config.set('Global', 'file_csv', 'basis.csv')
    config.set('Global', 'subject_mail', 'Предложение для компании {{company}} {{full_name}}')
    config.set('Global', 'template_mail', 'template.html')
    with open(path, 'w', encoding='UTF-8') as config_file:
        config.write(config_file)
    return config


def update_config(config: configparser.ConfigParser):
    with open(path_settings, 'w', encoding='UTF-8') as config_file:
        config.write(config_file)
