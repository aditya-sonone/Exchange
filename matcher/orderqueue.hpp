#pragma once

#include <condition_variable>
#include <mutex>
#include <queue>

#include "../generated/cpp/order.hpp"

class OrderQueue
{
public:

    void push(const Order& order);

    Order pop();

private:

    std::queue<Order> m_queue;

    std::mutex m_mutex;

    std::condition_variable m_cv;
};