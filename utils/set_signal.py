"""
Модуль для демонстрации запроса к gRPC-серверу с целью отправки сигнала.
Используется протокол буферов Protobuf и библиотека gRPC.
"""

# Импортируем библиотеку gRPC для осуществления коммуникаций с удалённым сервером
import grpc

# Импортируем сгенерированные файлы на основе протокола буферов (ProtoBuf)
from proto import elecont_pb2, elecont_pb2_grpc

# Стандартная библиотека Python для работы со временем
import time


def set_signal(ip_address_and_port, guid, quality, timestamp, type_valye, value, str_quality):
    """Отправляет сигнал на удалённый сервер с указанными параметрами.

    Параметры:
        ip_address_and_port (str): Адрес и порт сервера (пример: '127.0.0.1:29041').
        guid (str): Уникальный идентификатор сигнала.
        quality (int): Показатель качества сигнала.
        timestamp (int): Временная отметка в миллисекундах.
        type_valye (int or enum): Тип сигнала (используя значения перечисления ElecontSignalType).
        value (str): Текущее значение сигнала.
        str_quality (str): Строковое представление качества сигнала.
    """
    try:
        # Устанавливаем соединение с удалённым сервером по указанному адресу и порту
        channel = grpc.insecure_channel(ip_address_and_port)
        stub = elecont_pb2_grpc.ElecontStub(channel)
        
        # Создаём объект Signal и заполняем его необходимыми данными
        request_signal = elecont_pb2.Signal()
        request_signal.guid = guid              # Идентификатор сигнала
        request_signal.quality = quality        # Показатель качества
        request_signal.time = timestamp         # Временная метка в миллисекундах
        request_signal.type.value = type_valye        # Тип сигнала (перечисление ElecontSignalType)
        request_signal.value = value            # Значение сигнала
        request_signal.str_quality = str_quality # Строковое описание качества
        
        # Выполняем запрос на сервер, вызывая метод SetSignal
        stub.SetSignal(request_signal)
        
        # Получаем сигнал по GUID и сравниваем значение
        response_get_signal_by_guid = stub.GetSignalByGuid(elecont_pb2.Guid(guid=guid))
        
        # Проверяем совпадение значения сигнала
        if value == response_get_signal_by_guid.value:
            # Сообщаем об успешной отправке
            print('Сигнал отправлен успешно.')
        else:
            # Если отправленное значение не совпадает со значением в приложение вызываем ошибку
            raise Exception("Значения сигнала не совпадают!")  
        
    # Обрабатываем любые ошибки gRPC
    except grpc.RpcError as e:
        print(f'gRPC ошибка: {e.details()}')


# Адрес и порт нашего локального сервера
ip_user_channel_client = '127.0.0.1:29041'

# Получаем текущее время в миллисекундах
timestamp_ms = int(time.time() * 1000)

# Создаём словарь с информацией о сигнале
signal = {
    'guid': 'b6ae1b69-faae-4464-b93b-5a961f485287',     # GUID сигнала
    'quality': 0,                                        # Качество сигнала
    'time': timestamp_ms,                                 # Текущая временная метка
    'type_valye': elecont_pb2.ElecontSignalType.INT16,   # Тип сигнала (используем перечисление)
    'value': '555',                                       # Значение сигнала
    'str_quality': "GOOD"                                # Строковое описание качества
}

# Вызываем функцию отправки сигнала с соответствующими параметрами
set_signal(ip_user_channel_client, signal['guid'], signal['quality'], signal['time'], signal['type_valye'], signal['value'], signal['str_quality'])
