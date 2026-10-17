# Versions

Both versions split `AmbarAssistant` into small classes with one responsibility each.
They differ on purpose.

## Version A: layered architecture with ports

- Four layers: interface, application, domain, infrastructure. Dependencies point toward the domain.
- Ports (`SensorFeed`, `ReadingRepository`, `LanguageModel`, `ActuatorPort`) are interfaces; MQTT, SQLite
  and the local model implement them.
- `AssistantService` orchestrates a turn; `IntentRouter` replaces the `if/elif` chain with a rule table.
- Best at: readability, a linear flow that is easy to follow, and unit tests with fake ports.
- Trade-off: speaking and acting at the same time needs explicit threading.

## Version B: event bus and skills

- An `EventBus` decouples adapters (MQTT, console, voice) from skills (`ClimateSkill`, `MotorSkill`,
  `ConversationSkill`).
- `ToolRegistry` exposes device actions to the language model, so a spoken order becomes a
  `CommandRequested` event handled without blocking the conversation.
- Best at: growing the device network (a new sensor or actuator is a new adapter or skill, with no
  change to the core) and concurrent handling.
- Trade-off: the flow is implicit in events, so it is harder to trace and debug.

## Responsibility map

| Original responsibility | Version A | Version B |
| --- | --- | --- |
| MQTT connection | `MqttSensorFeed` | `MqttAdapter` |
| JSON messages | `Reading.from_mqtt` | `Reading.from_mqtt` via `MqttAdapter` |
| Persistence | `SqliteRepository` | `SqliteEventStore` |
| Threshold rules | `RuleEngine` | `ClimateSkill` |
| Prompt context | `ContextBuilder` | `ConversationSkill` |
| LLM inference | `OllamaLlm` | `LocalLlmAdapter` |
| Intents | `IntentRouter` | event types and `ToolRegistry` |
| Motor control | `MqttActuator` | `MotorSkill` and `MqttActuator` |
| Console I/O | `ConsoleInterface` | `ConsoleAdapter` |
| Configuration | `Settings` | environment variables in `main` |
