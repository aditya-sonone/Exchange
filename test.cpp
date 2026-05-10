#include <fstream>
#include <iostream>

#include "generated/order.hpp"
#include "generated/packetdispatcher.hpp"


int main()
{
    Order order(
        69,
        Side::Sell
    );

    std::ofstream out(
        "order.bin",
        std::ios::binary
    );

    order.serializePacket(out);

    out.close();

    std::ifstream in(
        "order.bin",
        std::ios::binary
    );

    PacketDispatcher::dispatch(in);

    in.close();

    return 0;
}