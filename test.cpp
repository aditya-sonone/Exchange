#include <fstream>
#include <iostream>

#include "generated/order.hpp"


int main()
{
    Order order(
        1,
        Side::Buy,
        350.5,
        OrderType::IOC
    );

    std::ofstream out(
        "order.bin",
        std::ios::binary
    );

    order.serialize(out);

    out.close();

    Order loadedOrder(
        0,
        Side::Sell,
        0,
        OrderType::FOK
    );

    std::ifstream in(
        "order.bin",
        std::ios::binary
    );

    loadedOrder.deserialize(in);

    in.close();

    std::cout
        << loadedOrder.toString()
        << std::endl;

    return 0;
}