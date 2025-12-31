#   rpc GetAllSignals (Empty) returns (SignalPool) {}
import grpc
from proto import elecont_pb2, elecont_pb2_grpc




def get_all_signals(ip_address_and_port):
    # Создаем соединение с сервером
    channel = grpc.insecure_channel(ip_address_and_port)
    
    # Создаем прокси-класс для обращения к службе Elecont
    stub = elecont_pb2_grpc.ElecontStub(channel)
    
    # Передаем пустой объект Empty в качестве аргумента
    empty_request = elecont_pb2.Empty()
    
    # Вызываем метод GetAllSignals
    response = stub.GetAllSignals(empty_request)
    
    # Выводим полученный ответ
    print(response)


ip_user_channel_client = '127.0.0.1:29041'

# Запускаем получение сигналов
get_all_signals(ip_user_channel_client)
   