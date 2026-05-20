#include "server.hpp"

int main()
{
    Server server(9000);

    server.start();

    return 0;
}