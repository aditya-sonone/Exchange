#include <fstream>
#include <iostream>

#include "generated/order.hpp"
#include "generated/packetdispatcher.hpp"


int main()
{
    Order order;

    order.setOrderId(123);
    order.setSide(Side::Buy);
    order.setPrice(1000);

    std::ofstream out(
        "order.bin",
        std::ios::binary
    );
    std::cout << order.getOrderId() << std::endl;
std::cout << static_cast<int>(order.getSide()) << std::endl;
std::cout << order.getPrice() << std::endl;
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