#pragma once

#include <atomic>
#include <thread>

#include "orderqueue.hpp"
#include "orderbook.hpp"

class Matcher
{
public:

    Matcher(OrderQueue& queue);

    ~Matcher();

    void start();

    void stop();

private:

    void run();

private:

    OrderQueue& m_queue;
    OrderBook m_orderBook;

    std::thread m_thread;

    std::atomic<bool> m_running {false};
};