#include "orderhandler.hpp"

#include <iostream>

static std::string sideToString(Side side)
{
    switch (side)
    {
        case Side::Buy:
            return "Buy";

        case Side::Sell:
            return "Sell";

        default:
            return "Unknown";
    }
}

void OrderHandler::handle(const Order& order)
{
    std::cout << "\n=== NEW ORDER ===\n";

    std::cout << "Order ID: "
              << order.getOrderId()
              << std::endl;

    std::cout << "Side: "
              << sideToString(order.getSide())
              << std::endl;

    std::cout << "=================\n";
}