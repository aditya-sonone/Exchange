#include <fstream>
#include <iostream>

#include "generated/cpp/order.hpp"

int main()
{
    std::ofstream out(
        "../order.bin",
        std::ios::binary
    );

    if (!out.is_open())
    {
        std::cerr
            << "Failed to open order.bin"
            << std::endl;

        return 1;
    }

    for (uint64_t i = 1; i <= 10; ++i)
    {
        Order order;
        order.setOrderId(i);
        if (i % 2 == 0)
        {
            order.setSide(Side::Sell);
        }
        else
        {
            order.setSide(Side::Buy);
        }
        order.setPrice(5000 + (i * 10));
        order.setQuantity(100 * i);
        order.serializePacket(out);

        std::cout<< "Generated Order "<< i<< std::endl;
    }

    out.close();

    std::cout
        << "\nGenerated 10 orders successfully."
        << std::endl;

    return 0;
}