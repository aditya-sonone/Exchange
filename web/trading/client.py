import socket

from protocol.packet_header import PacketHeader
from generated.python.packet_dispatcher import PacketDispatcher


HOST = "127.0.0.1"
PORT = 9000


def recv_exact(sock, size):

    data = b''

    while len(data) < size:

        chunk = sock.recv(size - len(data))

        if not chunk:
            raise Exception("Connection closed")

        data += chunk

    return data


def send_packet(packet: bytes):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # connect to gateway
        s.connect((HOST, PORT))

        # send binary packet
        s.sendall(packet)

        # receive response header
        header_data = recv_exact(
            s,
            PacketHeader.SIZE
        )

        header = PacketHeader.deserialize(
            header_data
        )

        # receive payload
        payload = recv_exact(
            s,
            header.payload_size
        )

        # deserialize packet
        response_packet = PacketDispatcher.dispatch(
            header.packet_id,
            payload
        )

        return response_packet