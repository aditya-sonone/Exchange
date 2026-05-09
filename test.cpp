#include <fstream>
#include <iostream>

#include "generated/order.hpp"

int main()
{
    Order order(
        1,
        350.5,
        10,
        "BSE"
    );

    std::ofstream out(
        "order.bin",
        std::ios::binary
    );

    order.serialize(out);

    out.close();

    Order loadedOrder(
        0,
        0,
        0,
        ""
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