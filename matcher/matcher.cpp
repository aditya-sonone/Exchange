#include "matcher.hpp"

#include <iostream>

Matcher::Matcher(OrderQueue& queue)
    : m_queue(queue)
{
}

Matcher::~Matcher()
{
    stop();
}

void Matcher::start()
{
    m_running = true;

    m_thread = std::thread(
        &Matcher::run,
        this
    );
}

void Matcher::stop()
{
    m_running = false;

    if (m_thread.joinable())
    {
        m_thread.join();
    }
}

void Matcher::run()
{
    while (m_running)
    {
        Order order = m_queue.pop();
        m_orderBook.addOrder(order);

        std::cout
            << "\n[MATCHER] Processing Order\n";

        std::cout
            << "Order ID: "
            << order.getOrderId()
            << std::endl;

        std::cout
            << "Price: "
            << order.getPrice()
            << std::endl;
    }
}