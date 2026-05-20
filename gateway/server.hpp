#pragma once

class Server
{
public:
    explicit Server(int port);

    void start();

private:
    int m_port;
};