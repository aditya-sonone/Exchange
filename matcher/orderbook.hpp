#pragma once

#include <vector>

#include "../generated/order.hpp"

class OrderBook
{
public:

    void addOrder(const Order& order);

    void print() const;

private:

    std::vector<Order> m_bids;

    std::vector<Order> m_asks;
};