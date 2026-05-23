# Exchange Project — Design Patterns & Problems Solved

This document tracks:

- Design patterns used
- Why they were introduced
- Problems they solved
- Architectural lessons learned

---

# 1. Code Generation Pattern

## Where

```text
schemas/ -> generator/ -> generated/
```

## Purpose

Generate repetitive protocol code automatically from schemas.

## Example

Schema:

```text
@packet(1)
struct Order {
    uint64 orderId;
}
```

Generated:

```cpp
class Order {
    void serialize(...);
    void deserialize(...);
};
```

## Problem Solved

Without generation:

- repetitive boilerplate
- manual serialization bugs
- packet inconsistency
- harder protocol evolution

## Architectural Lesson

Generated artifacts should never be source-of-truth.

Source-of-truth is:

```text
schemas/
generator/
```

NOT:

```text
generated/
```

---

# 2. Dispatcher Pattern

## Where

```text
PacketDispatcher
```

## Purpose

Route incoming packets to appropriate handlers.

## Example

```cpp
switch(packetId)
{
    case Order::PACKET_ID:
}
```

## Problem Solved

Without dispatcher:

- networking layer becomes packet-aware
- packet parsing duplicated everywhere
- protocol handling becomes messy

## Architectural Lesson

Transport layer should not contain business logic.

---

# 3. Callback / Inversion Of Control (IoC)

## Where

```cpp
registerOrderHandler(...)
```

## Purpose

Allow application code to inject behavior into dispatcher.

## Example

```cpp
PacketDispatcher::registerOrderHandler(
    OrderHandler::handle
);
```

## Problem Solved

Previously:

```text
generated dispatcher -> gateway handlers
```

Generated protocol code depended on business logic.

This created:

- tight coupling
- non-reusable generated code
- impossible regeneration workflow

After IoC:

```text
gateway registers handlers -> dispatcher
```

Now generated code is protocol-only.

## Architectural Lesson

Infrastructure layers should not depend on business layers.

---

# 4. Separation Of Concerns

## Current Separation

```text
Protocol Layer
Transport Layer
Business Logic Layer
```

## Purpose

Keep each system component focused on one responsibility.

## Problem Solved

Without separation:

- networking code becomes mixed with matching logic
- protocol changes break business logic
- difficult testing
- poor scalability

## Architectural Lesson

Large distributed systems survive through strict boundaries.

---

# 5. Layered Architecture

## Current Layers

```text
Schema Layer
    ↓
Generated Protocol Layer
    ↓
Transport Layer
    ↓
Business Logic Layer
```

## Purpose

Organize system into clean dependency hierarchy.

## Problem Solved

Prevents:

- circular dependencies
- spaghetti architecture
- hidden coupling

## Architectural Lesson

Dependencies should flow downward only.

---

# 6. Serialization Pattern

## Where

```cpp
serialize()
deserialize()
```

## Purpose

Convert objects into binary wire format.

## Problem Solved

Allows:

- network transport
- persistence
- replay
- interoperability

## Architectural Lesson

Serialization is the foundation of distributed systems.

---

# 7. Packet Framing Pattern

## Where

```text
PacketHeader
```

## Packet Layout

```text
[packetId][payloadSize][payload]
```

## Purpose

TCP is stream-oriented.

Framing reconstructs message boundaries.

## Problem Solved

Without framing:

- partial packets
- merged packets
- ambiguous reads

## Architectural Lesson

TCP provides byte streams, not messages.

Applications must define framing.

---

# 8. DSL (Domain Specific Language)

## Where

```text
schemas/order.txt
```

## Purpose

Create a protocol-definition language.

## Example

```text
@packet(1)
struct Order
```

## Problem Solved

Without DSL:

- protocol definitions spread across C++
- harder protocol evolution
- duplicated metadata

## Architectural Lesson

DSLs centralize system definitions.

---

# 9. Static Registration Pattern

## Where

```cpp
registerOrderHandler(...)
```

## Purpose

Configure system behavior during startup.

## Problem Solved

Allows runtime composition of systems.

Dispatcher no longer hardcodes application behavior.

## Architectural Lesson

Registration-based systems are extensible.

---

# 10. Transport / Protocol Decoupling

## Current Design

Protocol layer does not know about TCP.

## Purpose

Allow packets to travel over:

- TCP
- UDP
- shared memory
- replay files

without changing packet classes.

## Problem Solved

Prevents transport-specific protocol implementations.

## Architectural Lesson

Protocols should remain transport-agnostic.

---

# 11. RAII (Resource Acquisition Is Initialization)

## Where

```cpp
std::ofstream
std::vector
std::stringstream
```

## Purpose

Automatic resource cleanup.

## Problem Solved

Avoids:

- memory leaks
- file descriptor leaks
- manual cleanup bugs

## Architectural Lesson

Resource ownership should be explicit and automatic.

---

# 12. Single Responsibility Principle

## Current Responsibilities

### Parser
Parses schema.

### Generator
Generates C++.

### FileWriter
Writes files.

### Dispatcher
Routes packets.

### Server
Handles TCP.

### OrderHandler
Processes orders.

## Problem Solved

Prevents giant multipurpose classes.

## Architectural Lesson

One component -> one reason to change.

---

# Problems Resolved So Far

## Problem: Generated code depended on business logic

### Solution

Introduced callback registration / IoC.

---

## Problem: Packet boundaries lost over TCP

### Solution

Introduced PacketHeader framing.

---

## Problem: Manual protocol boilerplate

### Solution

Built schema-driven code generation.

---

## Problem: Hardcoded packet processing

### Solution

Introduced PacketDispatcher.

---

## Problem: Non-reproducible generated files

### Solution

Moved all dispatcher logic into generator.

Generated files became disposable artifacts.

---

# Current Architecture Summary

```text
schemas/
    ↓
generator/
    ↓
generated protocol layer
    ↓
TCP gateway
    ↓
dispatcher
    ↓
handlers
```

---

# Next Planned Patterns

Upcoming patterns likely include:

- Producer / Consumer
- Thread-safe Queue
- Event-Driven Architecture
- Reactor Pattern
- Observer Pattern
- Pub/Sub
- Lock-Free Ring Buffer
- State Machine
- Command Pattern

These will appear when building:

- matcher
- market data
- order books
- replay engine
- risk engine

