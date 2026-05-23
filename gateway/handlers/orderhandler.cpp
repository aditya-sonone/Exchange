#include "orderhandler.hpp"

#include <iostream>

void OrderHandler::initialize(
    OrderQueue* queue)
{
    s_queue = queue;
}

void OrderHandler::handle(
    const Order& order)
{
    if (!s_queue)
    {
        std::cerr
            << "Order queue not initialized\n";

        return;
    }

    std::cout
        << "[GATEWAY] Received Order "
        << order.getOrderId()
        << std::endl;

    s_queue->push(order);
}