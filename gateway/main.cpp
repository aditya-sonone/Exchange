#include "server.hpp"

#include "../generated/cpp/packetdispatcher.hpp"

#include "handlers/orderhandler.hpp"

#include "../matcher/orderqueue.hpp"
#include "../matcher/matcher.hpp"

int main()
{
    OrderQueue orderQueue;
    Matcher matcher(orderQueue);

    matcher.start();

    OrderHandler::initialize(&orderQueue);
    PacketDispatcher::registerOrderHandler(OrderHandler::handle);

    Server server(9000);
    server.start();

    return 0;
}