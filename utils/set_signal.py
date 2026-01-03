"""
Модуль "set_signal.py" для демонстрации запроса к gRPC-серверу с целью отправки сигнала.
Используется протокол буферов Protobuf и библиотека gRPC.
"""

# Импортируем библиотеку gRPC для осуществления коммуникаций с удалённым сервером
import grpc

# Импортируем сгенерированные файлы на основе протокола буферов (ProtoBuf)
from proto import elecont_pb2, elecont_pb2_grpc

# Стандартная библиотека Python для работы со временем
import time


def set_signal(ip_address_and_port, guid, value):
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
    
    # Получаем текущее время в миллисекундах
    timestamp_ms = int(time.time() * 1000)
    
    try:
        # Устанавливаем соединение с удалённым сервером по указанному адресу и порту
        channel = grpc.insecure_channel(ip_address_and_port)
        stub = elecont_pb2_grpc.ElecontStub(channel)
        
        # Создаём объект Signal и заполняем его необходимыми данными
        request_signal = elecont_pb2.Signal()
        request_signal.guid = guid              # Идентификатор сигнала
        request_signal.quality = 0        # Показатель качества (В текущей реализации всегда 0 - Good)
        request_signal.time = timestamp_ms         # Временная метка в миллисекундах
        request_signal.type.value = elecont_pb2.ElecontSignalType.INT16        # Тип сигнала (В текущей реализации всегда int16)
        request_signal.value = value            # Значение сигнала
        request_signal.str_quality = "GOOD" # Строковое описание качества (В текущей реализации всегда Good)
        
        # Выполняем запрос на сервер, вызывая метод SetSignal
        stub.SetSignal(request_signal)
        
        # Получаем сигнал по GUID и сравниваем значение
        response_get_signal_by_guid = stub.GetSignalByGuid(elecont_pb2.Guid(guid=guid))
        
        # Проверяем совпадение значения сигнала
        if value == response_get_signal_by_guid.value:
            # Сообщаем об успешной отправке
            print(f"Сигнал с GUID={guid} успешно обновлён.")
        else:
            # Если отправленное значение не совпадает со значением в приложение вызываем ошибку
            raise Exception("Произошла ошибка, значения сигнала не совпадают!")  
        
    # Обработка ошибок
    except grpc.RpcError as e:
        print(f'gRPC ошибка: {e.details()}')
