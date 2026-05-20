#pragma once

#include "../../generated/order.hpp"

class OrderHandler
{
public:
    static void handle(const Order& order);
};