#include "orderbook.hpp"

#include <iostream>

void OrderBook::addOrder(const Order& order)
{
    if (order.getSide() == Side::Buy)
    {
        m_bids.push_back(order);
    }
    else
    {
        m_asks.push_back(order);
    }

    print();
}

void OrderBook::print() const
{
    std::cout << "\n===== ORDER BOOK =====\n";

    std::cout << "\nBIDS\n";

    for (const auto& order : m_bids)
    {
        std::cout
            << order.getQuantity()
            << " @ "
            << order.getPrice()
            << std::endl;
    }

    std::cout << "\nASKS\n";

    for (const auto& order : m_asks)
    {
        std::cout
            << order.getQuantity()
            << " @ "
            << order.getPrice()
            << std::endl;
    }

    std::cout << "======================\n";
}