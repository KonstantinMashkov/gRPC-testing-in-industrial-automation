"""
Модуль "get_all_signals.py" для демонстрации запроса к gRPC-серверу с целью получения сигнала.
Используется протокол буферов Protobuf и библиотека gRPC.
"""

# Импортируем библиотеку gRPC
import grpc

# Импортируем сгенерированные файлы
from proto import elecont_pb2, elecont_pb2_grpc

# Импортируем библиотеку для преобразования объектов Protobuf в обычные Python-словари формата JSON.
from google.protobuf.json_format import MessageToDict

def get_all_signals(ip_address_and_port):
    """
    Осуществляет подключение к gRPC-серверу и запрашивает список всех сигналов.

    Parameters:
        ip_address_and_port (str): IP-адрес и порт, по которым доступен gRPC-сервер.
    """
    try:
        # Создаем соединение с сервером
        channel = grpc.insecure_channel(ip_address_and_port)
        stub = elecont_pb2_grpc.ElecontStub(channel)
        
        # Передаем пустой объект Empty в качестве аргумента
        empty_request = elecont_pb2.Empty()
        
        # Вызываем метод GetAllSignals
        response = stub.GetAllSignals(empty_request)
        
        # Возвращаем полученные данные       
        return response
    
    # Обработка ошибок
    except grpc.RpcError as e:
        print(f'gRPC ошибка: {e.details()}')
            

# функция для получения все GUID
def get_guids(signals_pool):
    """
    Извлекает все уникальные идентификаторы (GUID) из различных типов сигналов.

    Параметры:
        signals_pool: Объект Protobuf, содержащий различные типы сигналов.

    Возвращаемое значение:
        list: Список уникальных идентификаторов (GUID) всех сигналов, содержащихся в переданном объекте.
    """
    try:
        # Преобразуем объект Protobuf в словарь Python
        signals_data = MessageToDict(signals_pool)
        
        # Список для гуидов
        guides = []

        # Сбор всех GUID проходим по каждому типу сигнала
        for signal_type in signals_data.keys():  # keys() вернут названия ключей ('booleanSignal', 'int16Signal', и т.д "Тетируемое приложение подерживает 13 типов сигналов")
            # Получаем список сигналов для текущего типа
            signals_list = signals_data.get(signal_type)  
            
            # Проходим по каждому сигналу и добавляем GUID в список
            for signal in signals_list:
                guides.append(signal['sigprop']['guid'])

        # Возвращаем все GUID
        return guides
    
    except Exception as ex:
        raise Exception(f"Произошла непредвиденная ошибка: {ex}")
