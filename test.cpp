#include <fstream>
#include <iostream>

#include "generated/order.hpp"
#include "generated/packetdispatcher.hpp"


int main()
{
    Order order;

    order.setOrderId(623);
    order.setSide(Side::Buy);
    order.setPrice(5400);
    order.setPan("A2377");

    std::ofstream out("../order.bin", std::ios::binary);

    order.serializePacket(out);

    out.close();

    std::ifstream in("../order.bin", std::ios::binary);

    PacketDispatcher::dispatch(in);

    in.close();

    return 0;
}