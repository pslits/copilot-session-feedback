# Event Storming Notation Reference

Agent-consumable reference for the Event Storming notation system.
Covers all 9 core elements, grammar rules, extended notation, and Markdown rendering.

---

## Core Notation Elements

| # | Element | Colour | Markdown Render | Description |
|---|---------|--------|-----------------|-------------|
| 1 | **Domain Event** | 🟠 Orange | `🟠 Order Placed` | Something that happened in the domain, expressed in past tense. The foundational element — everything else relates to events. |
| 2 | **Command** | 🔵 Blue | `🔵 Place Order` | An action requested by an actor or policy, expressed in imperative mood. Triggers one or more domain events. |
| 3 | **Aggregate** | 🟨 Yellow (large) | `🟨 Order` | A cluster of domain objects treated as a unit for state changes. Receives commands, enforces invariants, emits events. *(Software Design only)* |
| 4 | **Actor / Person** | 🟡 Yellow (small) | `🟡 Customer` | A person or role that issues commands. Represents the human (or system) initiating an action. |
| 5 | **System** | 🩷 Pink | `🩷 Payment Gateway` | A system (external or internal) treated as a black box. Either sends events into or receives commands/events from the domain. |
| 6 | **Policy** | 🟣 Lilac / Purple | `🟣 Whenever invoice arrives, schedule payment` | A business rule or automation that reacts to an event and triggers a command. Always follows "Whenever [event], then [command]". |
| 7 | **Read Model** | 🟢 Green | `🟢 Customer Credit Score` | Data that an actor needs to see before issuing a command. Represents the information requirement. |
| 8 | **Hot Spot** | 🔴 Red | `🔴 Who owns this? ❓` | A problem, question, conflict, or area of uncertainty. Marks items needing further discussion. |
| 9 | **Opportunity** | 💚 Bright Green | `💚 Could automate this step` | A positive discovery: new feature idea, process improvement, quick win, or business insight found during exploration. The counterpart of Hot Spots. |


---

## Naming Conventions

| Element | Convention | Examples | Anti-example |
|---------|-----------|----------|--------------|
| Domain Event | **Past tense**, domain language | `Order Placed`, `Payment Received`, `Item Shipped` | ~~`Place Order`~~ (imperative = command) |
| Command | **Imperative mood**, verb first | `Place Order`, `Cancel Subscription`, `Approve Refund` | ~~`Order Placed`~~ (past tense = event) |
| Aggregate | **Noun or noun phrase** | `Order`, `Shopping Cart`, `User Account` | ~~`Process Order`~~ (verb = command) |
| Actor | **Role name** | `Customer`, `Admin`, `Warehouse Manager` | ~~`The system`~~ (too vague) |
| System | **System proper name** | `Stripe`, `Email Gateway`, `Inventory API` | ~~`External`~~ (unspecific) |
| Policy | **"Whenever [event], then [command]"** | `Whenever Order Placed then Send Confirmation` | ~~`Handle order`~~ (too vague) |
| Read Model | **Noun describing the view** | `Order Summary`, `Inventory Dashboard` | ~~`Show Order`~~ (verb = command) |
| Opportunity | **Short noun phrase** describing the insight | `Automate Invoicing`, `Self-Service Returns` | ~~`We should fix this`~~ (too vague, that’s a Hot Spot) |

### Avoiding Vague Commands

If a command reads as “Check”, “Verify”, or “Review”, decide which applies:

| Symptom | Diagnosis | Fix |
|---------|----------|-----|
| The action retrieves information but changes no state | It’s a Read Model, not a Command | Replace the 🔵 Command with a 🟢 Read Model |
| The action changes state but is poorly named | It’s a real Command with a vague name | Rephrase as a specific state change (e.g., 🔵 `Approve Claim` instead of 🔵 `Review Claim`) |
| The action involves a human decision point | It’s a human-in-the-loop step | Model as: `Event → Policy → Human → Read Model → Command` |

**Conversational flows:** When modeling chatbots or dialogue-driven processes,
focus on the exit condition — the event that ends the conversation — rather than
modeling each message exchange. Treat the conversation as a single Command →
System → Event sequence where the event captures the outcome.

### Common Mistakes

| ❌ Wrong | ✅ Right | Why |
|---|---|---|
| 🟠 `Send Email` | 🟠 `Email Sent` | Events are past tense — things that already happened |
| 🟠 `Update Order` | 🟠 `Shipping Address Changed` | Avoid generic CRUD names; capture *what* changed |
| 🟠 `OrderUpdated` | 🟠 `Order Cancelled` | Domain-specific events carry meaning; generic labels do not |
| 🔵 `Order Placed` | 🔵 `Place Order` | Commands are imperative — things we ask the system to do |
| 🟣 `Check inventory` | 🟣 `Whenever order placed, reserve inventory` | Policies must state the trigger event and the resulting command |

---

## Grammar Rules

The Event Storming notation follows a directional grammar. These are the valid connections:

### Core Grammar — Software Design (must be enforced)

```
Actor ──▶ Command ──▶ Aggregate ──▶ Domain Event
                                        │
                                        ├──▶ Read Model (information produced)
                                        ├──▶ Policy ──▶ Command (reactive chain)
                                        └──▶ External System (notification)
```

### Core Grammar — Process Modeling

In Process Modeling, the System element replaces the Aggregate:

```
Event ──▶ Policy ──▶ Command ──▶ System ──▶ Event
```

Or with a human decision point:

```
Event ──▶ Policy ──▶ Human ──▶ Read Model ──▶ Command ──▶ System ──▶ Event
```

### Rules

1. **Events are triggered, never spontaneous.** Every Domain Event must trace back to either a Command (via an Aggregate in SD, or a System in PM) or an External System.
2. **Commands require an issuer.** Every Command must have either an Actor or a Policy as its source.
3. **Aggregates mediate.** Commands do not directly produce events — they go through an Aggregate that enforces business invariants.
4. **Policies are reactive.** A Policy always listens to a Domain Event and reacts by issuing a Command.
5. **Read Models inform.** A Read Model is consumed by an Actor before issuing a Command. It does not trigger actions itself.
6. **External Systems are boundary elements.** They can emit events into the domain or receive commands/events from the domain.

### Valid Sequences

| Sequence | Example |
|----------|---------|
| `Actor → Command → Aggregate → Event` | `🟡 Customer → 🔵 Place Order → 🟨 Order → 🟠 Order Placed` |
| `Actor → Command → System → Event` (PM) | `🟡 Customer → 🔵 Place Order → 🩷 Order Service → 🟠 Order Placed` |
| `Event → Policy → Command` | `🟠 Order Placed → 🟣 Whenever Order Placed, Send Email → 🔵 Send Confirmation Email` |
| `Event → Read Model` | `🟠 Order Placed → 🟢 Order Confirmation View` |
| `External System → Event` | `🩷 Payment Gateway → 🟠 Payment Confirmed` |
| `Event → External System` | `🟠 Order Shipped → 🩷 Notification Service` |

### Branching Flow Notation

When a Policy branches on conditions, use tree notation to show alternative paths:

```
🟠 Event Name
  → 🟣 Policy Name:
      ├── Condition A? ──→ 🔵 Command A
      │                     → 🩷 External System
      │                       → 🟠 Resulting Event A
      │
      └── Condition B? ──→ 🔵 Command B
                            → 🩷 External System
                              → 🟠 Resulting Event B
```

Rules:
- The triggering 🟠 Event starts at the top, unindented.
- The 🟣 Policy follows on the next line, indented with `→`.
- Each branch uses `├──` (mid-branch) or `└──` (last branch) with the condition as a question.
- Commands, External Systems, and resulting Events chain downward with increasing indent.
- Use `│` to connect lines vertically within a branch.
- For non-branching policies, a single `└──` suffices.

### Invalid Sequences (common mistakes)

| Invalid | Why | Fix |
|---------|-----|-----|
| `Actor → Event` | Actors don't directly cause events | Insert a Command and Aggregate between them |
| `Command → Event` (no Aggregate) | Commands are processed by Aggregates | Add the Aggregate that enforces invariants |
| `Policy → Event` | Policies issue Commands, not Events | Change to `Policy → Command → Aggregate → Event` |
| `Read Model → Command` | Read Models inform, they don't trigger | Add an Actor who reads the model, then issues the command |
| `Event → Event` (direct) | Events don't cause events directly | Insert a Policy between them if there's a business rule |

---

## Extended Notation

These elements appear in Process Modeling and Software Design phases:

| Element | Symbol | Use in Phase | Description |
|---------|--------|-------------|-------------|
| **Swimlane** | `---` divider | Process Modeling | Separates different processes or bounded contexts on the timeline |
| **Bounded Context** | `[ Context Name ]` | Software Design | A logical boundary grouping related aggregates; a candidate microservice or module |
| **Integration Contract** | `⇄` | Software Design | A defined interface between bounded contexts specifying what data crosses the boundary |
| **Variation** | `⑴ ⑵ ⑶` | Process Modeling | Alternative paths branching from a decision point in the process flow |
| **Happy Path** | `✅` marker | Process Modeling | The main success scenario through a process |
| **Exception Path** | `⚠️` marker | Process Modeling | An error or edge-case scenario branching from the happy path |
### Optional Extended Notation (from Mariusz Gil)

Add these only when the core model feels complete:

| Symbol | Element | Purpose |
|---|---|---|
| 📐 | Rule / Invariant | A business constraint that must always hold |
| 📊 | Metric | A measurable outcome to track |
| 🔔 | Alert | A notification or escalation trigger |
| 🎨 | Emotion | How a user feels at this point (useful in service design) |

**Start with the 6–9 core colours.** Add extended notation only when needed.

---

## Timeline Conventions

1. **Left to right** — time flows left to right. Earlier events on the left, later on the right.
2. **Pivotal events** — key events that mark major transitions in the process. Identify these first during Big Picture.
3. **Swimlanes** — use horizontal dividers to separate parallel processes or different bounded contexts.
4. **Temporal clustering** — group events that happen close together in time. Leave visual gaps between temporal clusters.
5. **Backward arrows** — avoid them. If a later event triggers an earlier process, model it as a Policy that issues a new Command rather than drawing a backward arrow.
6. **Explicit arrows** — arrows are implicit in left-to-right ordering. Use explicit arrows (`→`) only for loops, jumps, or feedback paths.

---

## Markdown Rendering Guide

When producing Event Storming artifacts in Markdown, use these conventions.

### Choosing the Right Format

| Content | Best Format | Example |
|---------|------------|--------|
| Causal chain (Event → Policy → Command → …) | Indented code block with `→` | Policy flows |
| Ordered sequence of steps | Numbered Markdown table | Happy path flows |
| Side-by-side comparison | Table with columns | Naming conventions, element comparisons |
| Branching / multi-path logic | Tree notation with `├──` / `└──` | Policy with conditions |
| Flat element list | Bulleted list or simple table | Hot spots, opportunities |
| Context relationships | ASCII box diagram | Bounded context maps |

### Event Timeline (Big Picture)

```markdown
| # | Event | Triggered By | Hot Spot? |
|---|-------|-------------|-----------|
| 1 | 🟠 Order Placed | 🔵 Place Order | |
| 2 | 🟠 Payment Processed | 🩷 Payment Gateway | |
| 3 | 🟠 Order Confirmed | 🟣 Whenever Payment Processed | 🔴 What if payment fails? |
```

### Process Flow (Process Modeling)

Process Modeling uses the PM grammar: `Actor → Command → System → Event`.
Aggregates (🟨) only appear in Software Design.

```markdown
### Process: Order Fulfilment

| Step | Element | Name | Notes |
|------|---------|------|-------|
| 1 | 🟡 Actor | Customer | Initiates the process |
| 2 | 🟢 Read Model | Product Catalogue | Customer browses available products |
| 3 | 🔵 Command | Add to Cart | Customer selects items |
| 4 | 🩷 System | Shopping Cart Service | Validates item availability |
| 5 | 🟠 Event | Item Added to Cart | Cart updated |
| 6 | 🔵 Command | Place Order | Customer confirms purchase |
| 7 | 🩷 System | Order Service | Validates cart, creates order |
| 8 | 🟠 Event | Order Placed | Order created successfully |
```

### Policy Flow (Process Modeling)

Use tree notation for policies with branching outcomes:

```markdown
🟠 Payment Submitted
  → 🟣 Payment Validation Policy:
      ├── Funds available? ──→ 🔵 Capture Payment
      │                         → 🩷 Payment Gateway
      │                           → 🟠 Payment Confirmed
      │
      └── Insufficient funds? ──→ 🔵 Decline Payment
                                   → 🩷 Payment Gateway
                                     → 🟠 Payment Declined
```

For simple, non-branching policies:

```markdown
🟠 Order Placed
  → 🟣 Auto-confirm small orders (under $50):
      └── 🔵 Confirm Order → 🩷 Order Service → 🟠 Order Confirmed
```

### Aggregate Cards (Software Design)

```markdown
### 🟨 Order

| Aspect | Detail |
|--------|--------|
| **Commands handled** | Place Order, Cancel Order, Update Order |
| **Events emitted** | Order Placed, Order Cancelled, Order Updated |
| **Invariants** | Order total must be > 0; cannot cancel shipped orders |
| **Lifecycle** | Created by Place Order; updated by Update Order; terminated by Cancel Order or Ship Order |
| **Bounded Context** | Order Management |
```

### Bounded Context Map (Software Design)

```markdown
| Context | Aggregates | Upstream Dependencies | Downstream Consumers |
|---------|-----------|----------------------|---------------------|
| Order Management | Order, OrderLine | Product Catalogue, Customer | Shipping, Billing |
| Shipping | Shipment, Tracking | Order Management | Notification |
```
