# Code Analysis Heuristics — Reverse Event Storming

Reference document for the `event-storming` skill. Provides heuristics for
extracting Event Storming notation elements from existing source code.

Use this reference when the direction is **reverse** (code → Event Storming).

---

## Heuristic Table

Each row maps an ES notation element to the code patterns that suggest it.

| ES Element | Code Signal | What to Look For | Confidence |
|------------|------------|-------------------|------------|
| **Domain Event** | State change | Assignments to persisted fields, ORM save/update calls, event emissions (`emit`, `publish`, `dispatch`, `raise`), side effects (logging state transitions, audit writes) | High |
| **Domain Event** | Callback / hook | `on_save`, `post_commit`, `after_create`, lifecycle hooks, observer pattern subscribers | Medium |
| **Command** | Public method / endpoint | Controller actions, API route handlers, CLI entry points, message consumers, public methods that mutate state | High |
| **Command** | Service method call | Application-service or use-case methods called from controllers or handlers | High |
| **Aggregate** | Class with state + behaviour | Classes that hold fields **and** enforce invariants (validation in setters, guard clauses, state machine transitions). Not pure data containers. | High |
| **Aggregate** | ORM entity / document | Classes decorated with `@Entity`, `@Document`, mapped in `models.py`, schema definitions with both fields and methods | Medium |
| **Actor** | User-facing entry point | Controllers, REST endpoints, GraphQL resolvers, CLI commands, UI event handlers — the caller represents an actor | High |
| **Actor** | Scheduled job / cron | Time-based triggers (`@Scheduled`, cron expressions, Celery beat tasks) — the scheduler is a system actor | Medium |
| **External System** | Outbound integration | HTTP client calls, SDK imports, message queue producers, SMTP sends, file uploads to external storage, third-party API wrappers | High |
| **External System** | Inbound webhook | Webhook receivers, callback URLs, event subscriptions from external services | High |
| **Policy** | Conditional business logic | `if`/`else` branches that encode business rules (not infrastructure checks), validation decorators, state machine guard conditions, specification pattern implementations | Medium |
| **Policy** | Reactive handler | Event handlers that trigger a new command without human intervention: sagas, process managers, policy objects, `when_event_then_command` patterns | High |
| **Read Model** | Query / projection | Read-only repository methods, view models, DTOs, GraphQL query resolvers, dashboard data providers, CQRS read-side projections | High |
| **Read Model** | Computed property | Derived/calculated fields exposed to the UI or other commands | Medium |
| **Hot Spot** | Complexity indicator | High cyclomatic complexity, deeply nested conditions, TODO/FIXME/HACK comments, broad exception catches, shared mutable state, feature flags, commented-out code | Medium |
| **Hot Spot** | Error-heavy path | Multiple exception types, retry logic, fallback chains, circuit breakers — signals uncertain or contested domain logic | Medium |
| **Temporal Sequence** | Temporal ordering | Method call chains, sequential steps in a service method, event handler ordering, saga step sequences | Medium |

---

## Language-Specific Hints

### Python

| Signal | Pattern Examples |
|--------|-----------------|
| Domain Event | `signal.send()`, Django signals (`post_save`, `pre_delete`), custom `EventBus.publish()`, dataclass with `occurred_at` field |
| Command | Flask/FastAPI route functions, Django view methods, Click CLI commands, Celery task definitions |
| Aggregate | Django `Model` subclass with `clean()` or property validators, SQLAlchemy model with `@validates` |
| External System | `requests.post()`, `httpx`, `boto3` client calls, `smtplib`, Celery `send_task()` to a different service |
| Policy | Decorators like `@validate`, `@require_permission`, custom validator classes, `if order.total > threshold` |

### TypeScript / JavaScript

| Signal | Pattern Examples |
|--------|-----------------|
| Domain Event | `EventEmitter.emit()`, `subject.next()` (RxJS), custom `DomainEvent` classes, Redux actions |
| Command | Express/Fastify route handlers, NestJS `@Post()` / `@Put()` methods, GraphQL mutations |
| Aggregate | Classes in `domain/` or `model/` with private fields + public methods that validate before mutating |
| External System | `fetch()`, `axios`, AWS SDK calls, `amqplib` publish, WebSocket sends to external services |
| Policy | Middleware functions, NestJS guards, Zod/Yup schema validations, `if (user.role === ...)` |

### C# / .NET

| Signal | Pattern Examples |
|--------|-----------------|
| Domain Event | `INotification` (MediatR), `IDomainEvent`, `EventStore.AppendToStreamAsync()` |
| Command | `IRequest<T>` (MediatR), ASP.NET controller actions (`[HttpPost]`), `ICommandHandler<T>` |
| Aggregate | Classes inheriting `AggregateRoot` or `Entity`, EF Core entities with `DbSet<T>` + domain methods |
| External System | `HttpClient` calls, gRPC client stubs, `IMessagePublisher`, Azure SDK clients |
| Policy | FluentValidation validators, domain service methods with `if/throw`, specification pattern classes |

### Java / Kotlin

| Signal | Pattern Examples |
|--------|-----------------|
| Domain Event | `ApplicationEvent`, Spring `@EventListener`, Axon `@EventSourcingHandler`, custom event classes |
| Command | `@RestController` methods, `@CommandHandler` (Axon/CQRS), Spring MVC `@PostMapping` |
| Aggregate | `@Aggregate` (Axon), JPA `@Entity` with business methods, classes with `@Version` optimistic locking |
| External System | `RestTemplate`, `WebClient`, Kafka producer, Feign client interfaces |
| Policy | `@Valid` + constraint annotations, Spring `Validator` implementations, domain service guard clauses |

---

## Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Non-OO code (scripts, functional) | Aggregates hard to identify — no class with state + behaviour | Look for data structures + functions that operate on them; treat the pair as a candidate aggregate |
| Microservices / distributed systems | Events cross service boundaries; single-repo analysis misses half the picture | Flag inter-service calls as External Systems; note that the full event flow requires multi-repo analysis |
| Event-sourced systems | Domain events are already explicit — heuristics may produce duplicates | Use the existing event definitions directly instead of re-discovering; validate against the event store schema |
| CRUD-only code | Few meaningful domain events — mostly mechanical state changes | Report that the domain may be a "CRUD context" with low event-storming value; flag as a Hot Spot for the human to decide |
| Generated code / boilerplate | Frameworks generate controllers/DTOs that look like commands/read models | Skip files in generated directories (`gen/`, `generated/`, `migrations/`); focus on hand-written domain code |
| Legacy / poorly structured code | Business rules buried in UI or database layer | Search broadly (views, stored procedures, frontend components); flag finding locations as Hot Spots |
