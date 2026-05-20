#include "server.hpp"

#include <arpa/inet.h>
#include <unistd.h>

#include <cstring>
#include <iostream>
#include <sstream>
#include <vector>

#include "../generated/packetdispatcher.hpp"
#include "../generated/packetheader.hpp"

Server::Server(int port)
    : m_port(port)
{
}

void Server::start()
{
    int serverFd = socket(AF_INET, SOCK_STREAM, 0);

    if (serverFd < 0)
    {
        std::cerr << "Failed to create socket\n";
        return;
    }

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(m_port);

    if (bind(serverFd, (sockaddr*)&address, sizeof(address)) < 0)
    {
        std::cerr << "Bind failed\n";
        return;
    }

    if (listen(serverFd, 5) < 0)
    {
        std::cerr << "Listen failed\n";
        return;
    }

    std::cout << "Gateway listening on port "
              << m_port
              << std::endl;

    while (true)
    {
        int clientFd = accept(serverFd, nullptr, nullptr);

        if (clientFd < 0)
        {
            std::cerr << "Accept failed\n";
            continue;
        }

        std::cout << "Client connected\n";

        while (true)
        {
            PacketHeader header;

            ssize_t headerBytes =
                recv(clientFd,
                     &header,
                     sizeof(PacketHeader),
                     MSG_WAITALL);

            if (headerBytes <= 0)
            {
                std::cout << "Client disconnected\n";
                close(clientFd);
                break;
            }

            std::vector<char> payload(header.getPayloadSize());

            ssize_t payloadBytes =
                recv(clientFd,
                     payload.data(),
                     header.getPayloadSize(),
                     MSG_WAITALL);

            if (payloadBytes <= 0)
            {
                std::cout << "Payload read failed\n";
                close(clientFd);
                break;
            }

            std::stringstream stream;

            header.serialize(stream);

            stream.write(payload.data(), payload.size());

            PacketDispatcher::dispatch(stream);
        }
    }
}