#include "server.hpp"

#include "../generated/packetdispatcher.hpp"

#include "handlers/orderhandler.hpp"

int main()
{
    PacketDispatcher::registerOrderHandler(
        OrderHandler::handle
    );

    Server server(9000);

    server.start();

    return 0;
}