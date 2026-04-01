# Output Templates — Event Storming

Reference document for the `event-storming` skill. Defines the structured output
formats that agents must produce at the end of each Event Storming phase.

Agents: use the template for the current phase and fill in every table. Do not
omit sections — if a section has no entries, write "None identified" in the
first row.

---

## Big Picture Output Template

### Domain Event Timeline

| # | Event | Cluster | Triggering Command | Actor | Notes |
|---|-------|---------|--------------------|-------|-------|
| 1 | 🟠 `Order Placed` | Order Lifecycle | 🔵 `Place Order` | 🟡 Customer | Pivotal event |
| 2 | … | … | … | … | … |

### External Systems

| System | Interaction Type | Events Affected | Notes |
|--------|-----------------|-----------------|-------|
| 🩷 Payment Gateway | Outbound API call | 🟠 `Payment Processed` | … |

### Hot Spots

| # | Hot Spot | Reason | Related Events | Severity |
|---|----------|--------|----------------|----------|
| 1 | 🔴 Pricing logic unclear | Multiple discount rules conflict | 🟠 `Order Priced` | High |

### Opportunities

| # | Opportunity | Related Events | Impact | Source |
|---|-------------|----------------|--------|--------|
| 1 | 💚 Automate invoice generation | 🟠 `Order Confirmed` | Eliminates manual step | Process gap discovered during timeline |

### Bounded Context Candidates

| # | Candidate Context | Key Events | Distinguishing Vocabulary |
|---|-------------------|------------|---------------------------|
| 1 | Order Management | 🟠 `Order Placed`, 🟠 `Order Confirmed` | order, line item, cart |

### Open Questions

| # | Question | Context | Suggested Resolution |
|---|----------|---------|---------------------|
| 1 | Who owns returns after 30 days? | Mentioned in refund flow | Clarify with domain expert |

### Goal Metrics

| Metric | Count |
|--------|-------|
| Domain events | _N_ |
| Commands | _N_ |
| Actors | _N_ |
| External systems | _N_ |
| Hot spots | _N_ |
| Opportunities | _N_ |
| Bounded context candidates | _N_ |
| Open questions | _N_ |

---

## Process Modeling Output Template

### Process List

| Process | Start Event | End Event | Event Count |
|---------|-------------|-----------|-------------|
| Order Fulfillment | 🟠 `Order Placed` | 🟠 `Order Shipped` | 8 |

### Process Flow (repeat per process)

> **Process:** _[Name]_

#### ✅ Happy Path

Use chain notation. Apply the PM grammar at every link: `Actor → Command → System → Event`.
Policies are embedded **inline** where they occur — there is no separate Policy Flows section.
Use `→ 🟣 Policy Name: "Whenever…"` to show automatic reactions inline in the chain.
Use 🩷 System (pink) for the executor — Aggregates (🟨) only appear in Software Design.

```
🟡 Customer
  → 🔵 `Place Order`
    → 🩷 Order Service
      → 🟠 `Order Placed`
        → 🟣 Order Fulfilment Policy: "Whenever an order is placed, reserve inventory"
          → 🔵 `Reserve Inventory`
            → 🩷 Warehouse System
              → 🟠 `Inventory Reserved`
```

#### ⚠️ Alternative Paths

One named chain per variation, branching from the exact command or event where the
divergence occurs. Use the same `→` chain notation as the happy path.

**⑴ Variation name**
```
🔵 `Command where divergence occurs`
  → 🩷 System
    → *(condition that triggers this path)*
      → 🔵 `Next Command`
        → 🩷 System
          → 🟠 `Resulting Event`
```

#### Read Models

| Read Model | Serves Command | Data Source | Notes |
|------------|---------------|-------------|-------|
| 🟢 Order Summary View | 🔵 `Review Order` | 🩷 Order Service | Displayed before confirmation |

### Cross-Reference Coverage

| Big Picture Event | Covered By Process | Gap? |
|-------------------|--------------------|------|
| 🟠 `Order Placed` | Order Fulfillment | No |
| 🟠 `Inventory Reserved` | — | **Yes** |

### Goal Metrics

| Metric | Count |
|--------|-------|
| Processes modeled | _N_ |
| Commands | _N_ |
| Events | _N_ |
| Policies | _N_ |
| Read models | _N_ |
| Variations | _N_ |
| Hot spots | _N_ |
| Opportunities | _N_ |

---

## Software Design Output Template

### Aggregate Cards (repeat per aggregate)

> **Aggregate:** 🟨 _[Name]_

| Lifecycle | Details |
|-----------|---------|
| **Create** | _How is this aggregate created? Which 🔵 command?_ |
| **Update** | _What 🔵 commands change its state?_ |
| **Delete** | _When/how is it deleted or archived?_ |
| **Query** | _What 🟢 read models expose its state?_ |

| Commands Handled | Events Produced |
|-----------------|----------------|
| 🔵 `Place Order` | 🟠 `Order Placed` |
| 🔵 `Confirm Order` | 🟠 `Order Confirmed` |

| Invariants |
|------------|
| Order total must be positive |
| Cannot confirm a cancelled order |

### Bounded Context Map

| Context | Aggregates | Owner / Team | Key Vocabulary |
|---------|-----------|-------------|----------------|
| Ordering | 🟨 Order, 🟨 Order Line | Order Team | order, line item, cart |
| Shipping | 🟨 Shipment, 🟨 Tracking | Logistics Team | shipment, carrier, tracking |

### Integration Contracts

| Publisher | Consumer | Data / Event | Pattern | Notes |
|-----------|----------|-------------|---------|-------|
| Ordering | Shipping | 🟠 `Order Confirmed` | Event-based (async) | Triggers shipment creation |

### Aggregate Validation Report

| Aggregate | Commands | Events | Lifecycle Complete? | Bounded Context | Issues |
|-----------|----------|--------|--------------------:|----------------|--------|
| 🟨 Order | 3 | 4 | Yes | Ordering | None |
| 🟨 Tracking | 1 | 1 | No — missing Delete | Shipping | Clarify archival policy |

### Goal Metrics

| Metric | Count |
|--------|-------|
| Aggregates | _N_ |
| Bounded contexts | _N_ |
| Integration contracts | _N_ |
| User stories generated | _N_ |

---

## Five Views Template

Compiled from all three phases at the end of the Software Design phase.

### View 1 — Next Actions

| # | Action | Priority | Source Phase | Related Aggregate / Event |
|---|--------|----------|-------------|--------------------------|
| 1 | Resolve 🔴 pricing logic unclear | High | Big Picture | 🟠 `Order Priced` |
| 2 | Define archival policy for 🟨 Tracking | Medium | Software Design | 🟨 Tracking |

### View 2 — Domain Definitions (Ubiquitous Language)

| Term | Definition | Bounded Context | First Appeared |
|------|-----------|----------------|----------------|
| Order | A customer's intent to purchase one or more items | Ordering | Big Picture |
| Shipment | A physical delivery unit tracked by a carrier | Shipping | Process Model |

### View 3 — Context Map

```
┌─────────────┐   🟠 Order Confirmed      ┌─────────────┐
│  Ordering    │ ──────────────────────▶  │  Shipping    │
│              │                           │              │
│  🟨 Order    │   🟠 Shipment Created     │  🟨 Shipment │
│  🟨 Order Line│ ◀────────────────────── │  🟨 Tracking │
└─────────────┘                           └─────────────┘
```

_Replace the ASCII diagram with the actual bounded contexts and their
integration events._

### View 4 — User Stories

| # | Story | Source |
|---|-------|--------|
| 1 | As a 🟡 **Customer**, I want to 🔵 **Place Order** so that 🟠 `Order Placed` starts the fulfillment process. | PM: Order Fulfillment, Step 1 |
| 2 | As a 🟡 **Warehouse Operator**, I want to 🔵 **Pick Items** so that 🟠 `Items Picked` triggers packing. | PM: Order Fulfillment, Step 4 |

### View 5 — Integration Contracts

_Same table as Software Design Integration Contracts above. Reproduced here for
standalone readability._

| Publisher | Consumer | Data / Event | Pattern | Notes |
|-----------|----------|-------------|---------|-------|
| Ordering | Shipping | 🟠 `Order Confirmed` | Event-based | … |
