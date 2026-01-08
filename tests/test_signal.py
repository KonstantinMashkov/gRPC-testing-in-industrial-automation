"""
Модуль "test_signal.py" для демонстрации примера авто-теста.
"""

from utils import get_all_signals, set_signal

def test_signals():
    """
    Тестирует работу с сигналами типа данных int16: получает все сигналы сервера, выделяет их GUID и устанавливает новое значение сигнала.

    Эта функция демонстрирует последовательность шагов:
    1. Подключение к серверу и получение всех сигналов.
    2. Извлечение всех GUID из полученных сигналов.
    3. Установку нового значения для каждого сигнала.

    """
    ip_user_channel_client = '127.0.0.1:29041'

    try:
        # Получаем все сигналы с сервера
        all_signals = get_all_signals.get_all_signals(ip_user_channel_client)
        
        # Выделяем все GUID из сигналов
        guides = get_all_signals.get_guids(all_signals)
        
        # Сообщаем о количестве GUID
        print(f"Количество GUID: {len(guides)}")
        
        # Устанавливаем значение для каждого сигнала
        for guid in guides:
            try:
                # Устанавливаем новое значение сигнала
                set_signal.set_signal(ip_user_channel_client, guid, '555')
            except Exception as exc:
                raise Exception(f"Ошибка обновления сигнала с GUID={guid}: {exc}")
                
    except Exception as general_exc:
        raise Exception(f"Возникла общая ошибка: {general_exc}")