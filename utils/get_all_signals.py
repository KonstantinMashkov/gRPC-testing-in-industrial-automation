

"""
Модуль для демонстрации запроса к gRPC-серверу с целью получения сигнала.
Используется протокол буферов Protobuf и библиотека gRPC.
"""

# Импортируем библиотеку gRPC
import grpc

# Импортируем сгенерированные файлы
from proto import elecont_pb2, elecont_pb2_grpc


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
            


# IP-адрес и порт, по которым мы работаем
ip_user_channel_client = '127.0.0.1:29041'

# Запускаем получение сигналов
response_get_all_signals = get_all_signals(ip_user_channel_client)

# Вывод в консоль полученного результата
print(response_get_all_signals)