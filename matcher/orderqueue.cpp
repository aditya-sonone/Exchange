#include "orderqueue.hpp"

void OrderQueue::push(const Order& order)
{
    {
        std::lock_guard<std::mutex> lock(
            m_mutex
        );

        m_queue.push(order);
    }

    m_cv.notify_one();
}

Order OrderQueue::pop()
{
    std::unique_lock<std::mutex> lock(
        m_mutex
    );

    m_cv.wait(
        lock,
        [this]
        {
            return !m_queue.empty();
        }
    );

    Order order = m_queue.front();

    m_queue.pop();

    return order;
}