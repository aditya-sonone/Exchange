# Exchange Engineering Log

## Protocol & Serialization Layer

### Achievements
- Built custom schema parser for packet definitions.
- Added support for:
  - structs
  - enums
  - packet annotations
- Implemented automatic C++ code generation.
- Generated:
  - packet structs
  - enum headers
  - serialization/deserialization methods
  - packet dispatcher
- Added binary packet serialization.
- Added packet framing using `PacketHeader`.

### Key Lessons
- In-memory C++ object layout is NOT safe for network protocols.
- Explicit serialization is required for deterministic wire format.
- Never use raw object memory for socket transmission.

### Problems Solved
#### Wire Format vs Memory Layout Bug
Issue:
- `recv()` was reading directly into `PacketHeader` object.
- Compiler padding caused header corruption.

Fix:
- Read exact protocol bytes into buffer.
- Deserialize explicitly using stream.

Result:
- Correct packet parsing.
- Stable binary protocol.

---

## Gateway Layer

### Achievements
- Built TCP gateway server.
- Added socket lifecycle management.
- Added packet receive loop.
- Added payload reconstruction.
- Added dispatcher integration.

### Runtime Flow
Client
→ TCP Gateway
→ PacketDispatcher
→ OrderHandler

### Problems Solved
#### Payload Corruption
Issue:
- Payload values became zero/garbage.

Root Cause:
- Header framing mismatch.

Fix:
- Explicit 6-byte header read.
- Manual deserialization.

---

## Dispatcher Architecture

### Achievements
- Auto-generated `PacketDispatcher`.
- Added packet ID routing.
- Added handler invocation.

### Architectural Improvement
- Dispatcher generation moved into generator pipeline.
- Generated folder can now be fully recreated automatically.

---

## Matcher Architecture

### Achievements
- Introduced dedicated matcher thread.
- Added asynchronous order processing.
- Added thread-safe queue.
- Decoupled networking from business logic.

### Current Runtime Architecture
Client
→ Gateway Thread
→ PacketDispatcher
→ OrderHandler
→ Thread-safe Queue
→ Matcher Thread

### Design Patterns Introduced
- Producer-Consumer Pattern
- Event-Driven Architecture
- Thread-safe Queue Pattern
- Asynchronous Processing
- Thread Ownership Separation

---

## Build System Evolution

### Initial State
- Manual g++ compilation.
- Manual protocol generation.
- No dependency graph.

### Current State
- Modular CMake build.
- Matcher static library.
- Gateway executable.
- Automated protocol generation.
- Automatic rebuild on schema changes.

### CMake Improvements
#### Added Matcher Module
- Created `matcher` static library.
- Linked gateway against matcher.

#### Added Root Build Graph
- Root CMake now orchestrates:
  - matcher
  - gateway
  - test

#### Added Protocol Codegen Pipeline
Implemented:
- `add_custom_command()`
- `add_custom_target(protocol_codegen)`
- Python generator integration
- Stamp-file based dependency tracking

### Current Build Flow
schema change
→ protocol generation
→ generated headers updated
→ matcher rebuild
→ gateway rebuild

### Problems Solved
#### Undefined Linker References
Issue:
- `OrderQueue::push()` unresolved.

Fix:
- Proper matcher library linkage.
- Centralized root build graph.

#### Separate Build Trees
Issue:
- matcher and gateway were built independently.

Fix:
- Single root-level CMake build.

---

## Testing Infrastructure

### Achievements
- Added binary packet generation test.
- Added dispatcher replay test.
- Added TCP packet sender using Python.

### Problems Solved
#### Relative Path Inconsistency
Issue:
- `order.bin` generated in build directory.
- Python client searched root directory.

Fix:
- Standardized packet generation path.

---

## Current Design Patterns Used

### Factory-Style Code Generation
Generator creates protocol classes automatically.

### Dispatcher Pattern
Packet IDs route packets to correct handlers.

### Producer-Consumer Pattern
Gateway produces orders.
Matcher consumes orders.

### Event-Driven Architecture
Packets become asynchronous events.

### Modular Build Architecture
Independent modules linked through dependency graph.

---

## Current Project Architecture

Exchange
├── generator/
│   ├── parser
│   ├── code generator
│   └── dispatcher generation
│
├── generated/
│   ├── protocol structs
│   ├── enums
│   ├── serializers
│   └── dispatcher
│
├── gateway/
│   ├── TCP server
│   ├── packet ingestion
│   └── handlers
│
├── matcher/
│   ├── matcher thread
│   └── thread-safe queue
│
└── test/
    ├── packet generation
    └── replay testing

---

## Current Status

### Working Features
- TCP packet ingestion
- Binary serialization
- Automatic protocol generation
- Packet dispatching
- Thread-safe asynchronous queue
- Dedicated matcher thread
- Modular CMake build
- Automatic protocol rebuilds

---

## Additional Architecture Evolution

### Dependency Injection / Inversion of Control

#### Problem
Generated protocol layer depended directly on business logic handlers.

#### Solution
Introduced callback registration / handler injection architecture.

#### Architectural Benefit
- Generated code became reusable.
- Business logic separated from transport/protocol layer.
- Generated artifacts became disposable.

---

## TCP Framing Lessons

### Problem
TCP does not preserve packet boundaries.

### Symptoms
- Packet IDs became corrupted.
- Payload fields became zero.
- Dispatcher showed `Unknown packet`.

### Root Cause
Assumed `recv()` returns complete logical packet.

### Solution
Introduced explicit packet framing:
- `PacketHeader`
- payload size field
- exact byte reads
- stream reconstruction

### Architectural Lesson
TCP is a byte stream, not a message protocol.
Applications must define framing themselves.

---

## Disposable Generated Artifacts

### Improvement
Moved all dispatcher logic into generator.

### Result
Entire `generated/` directory can now be deleted and recreated safely.

### Architectural Lesson
Generated code should never contain handwritten business logic.
Generated artifacts must be reproducible.

---

## Advanced Design Patterns Added

### RAII (Resource Acquisition Is Initialization)

#### Used In
- `std::ofstream`
- `std::vector`
- `std::stringstream`
- socket/file ownership

#### Problem Solved
- automatic cleanup
- prevents leaks
- exception-safe resource management

---

### Single Responsibility Principle

#### Current Responsibilities
Parser
- parses schema

Generator
- generates C++ protocol code

FileWriter
- writes generated files

Dispatcher
- routes packets

Server
- handles TCP networking

OrderHandler
- processes business events

#### Architectural Lesson
One component should have one reason to change.

---

## Build System Automation

### Major Improvement
Integrated protocol generator directly into CMake.

### Added
- `add_custom_command()`
- `add_custom_target(protocol_codegen)`
- stamp-file dependency tracking
- automatic schema rebuilds

### Current Build Flow
schema change
→ generator reruns
→ generated headers recreated
→ matcher rebuilds
→ gateway rebuilds

### Architectural Lesson
Build systems should depend on generation process, not exact generated files.

---

## Current Runtime Architecture (Updated)

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
 ↓
thread-safe queue
 ↓
matcher thread
 ↓
future order book

---

## Future Architectural Patterns Planned

### Upcoming Patterns
- Reactor Pattern
- Observer Pattern
- Publish / Subscribe
- Lock-Free Ring Buffer
- State Machine
- Command Pattern

### Planned Components
- OrderBook
- Matching Engine
- Replay Engine
- Risk Engine
- Market Data Publisher

---

## Next Planned Steps

### Immediate
- Build OrderBook
- Add bids/asks storage
- Add order insertion logic
- Print live order book state

### Future
- Matching engine
- Trade execution
- Market data events
- Persistence/replay logs
- Multiple client support
- ASIO networking
- Lock-free queues
- Performance optimization

