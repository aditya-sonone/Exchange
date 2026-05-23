#pragma once

#include "../../generated/order.hpp"
#include "../../matcher/orderqueue.hpp"

class OrderHandler
{
public:

    static void initialize(OrderQueue* queue);

    static void handle(const Order& order);

private:

    inline static OrderQueue* s_queue = nullptr;
};