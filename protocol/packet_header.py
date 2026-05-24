import struct


class PacketHeader:

    SIZE = 6

    def __init__(self):

        self.packet_id = 0
        self.payload_size = 0

    def serialize(self):

        return struct.pack(
            "<HI",
            self.packet_id,
            self.payload_size
        )

    @staticmethod
    def deserialize(data: bytes):

        packet_id, payload_size = struct.unpack(
            "<HI",
            data
        )

        obj = PacketHeader()

        obj.packet_id = packet_id
        obj.payload_size = payload_size

        return obj