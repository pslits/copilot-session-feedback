# Requirements Intake Guide — Forward Event Storming

Reference document for the `event-storming` skill. Provides heuristics for
extracting Event Storming notation elements from requirements documents.

Use this reference when the direction is **forward** (requirements → Event
Storming).

---

## Supported Input Formats

| Format | Description | Best For |
|--------|------------|----------|
| User stories | "As a [role], I want to [action] so that [outcome]" | Commands, Actors, Events |
| Acceptance criteria | "Given…When…Then" or checklist items | Policies, Domain Events |
| PRD / product brief | Prose describing features, goals, and workflows | Big Picture events, External Systems |
| Free-text requirements | Unstructured description of desired behaviour | All elements (lower confidence) |
| Process descriptions | Step-by-step workflow narratives | Process flows, Policies, Read Models |
| Domain glossary | List of domain terms and definitions | Aggregates, Ubiquitous Language |

---

## Heuristic Mapping Table

Each row maps an ES notation element to the requirements patterns that signal it.

| ES Element | Requirements Signal | What to Look For | Example |
|------------|-------------------|-------------------|---------|
| **Domain Event** | Outcome / result clause | "so that [outcome]" in user stories, "Then [state change]" in acceptance criteria, past-tense results in prose ("the order is confirmed") | "Then the payment is captured" → `Payment Captured` |
| **Domain Event** | Business milestone | Key state transitions mentioned in PRDs: "approved", "shipped", "completed", "cancelled", "expired" | "Once approved, the request moves to fulfillment" → `Request Approved` |
| **Command** | Actor intention | "I want to [action]" in user stories, imperative verbs in requirements ("submit", "cancel", "approve", "assign") | "I want to submit my application" → `Submit Application` |
| **Command** | System action | Automated actions mentioned in process descriptions: "the system sends", "automatically generates", "triggers a notification" | "The system sends a confirmation email" → `Send Confirmation Email` |
| **Aggregate** | Core business noun | Nouns that have a lifecycle (created, modified, archived) and appear repeatedly across multiple user stories or acceptance criteria | "Order" appearing in place, confirm, ship, cancel stories → `Order` aggregate |
| **Aggregate** | Entity in domain glossary | Glossary entries that describe things with state, rules, and ownership | "Policy: a set of coverage terms owned by a policyholder" → `Policy` aggregate |
| **Actor** | Role / persona | "As a [role]" in user stories, named personas in PRDs, role descriptions in requirements | "As a warehouse operator" → Actor: Warehouse Operator |
| **Actor** | System / timer actor | "The system automatically…", "Every night at midnight…", "On schedule…" | "Every day at 2 AM, the system archives old records" → Actor: Scheduler |
| **External System** | Integration mention | "integrates with", "sends data to", "receives from", third-party service names, API references, "via [service name]" | "Payment processed via Stripe" → External System: Stripe |
| **External System** | Data import/export | "Import data from…", "Export report to…", "Sync with…" | "Sync inventory with warehouse management system" → External System: WMS |
| **Policy** | Business rule | "Must", "shall", "only if", "whenever", "automatically when", conditional logic in acceptance criteria | "Orders over $500 require manager approval" → Policy: Large Order Approval |
| **Policy** | Constraint / validation | "Cannot", "must not", "valid only when", "unless", required fields, format rules | "Cannot cancel an order after shipment" → Policy: Post-Ship Cancellation Block |
| **Read Model** | Information display | "User sees…", "Dashboard shows…", "Display the…", "Summary of…", reporting requirements | "The manager sees a list of pending approvals" → Read Model: Pending Approvals View |
| **Read Model** | Decision-supporting data | Information explicitly needed before an actor can issue a command | "Before approving, the manager reviews the order total and history" → Read Model: Order Review |
| **Hot Spot** | Ambiguity | Vague language ("appropriate", "as needed", "TBD"), contradictory requirements, missing acceptance criteria, unresolved questions | "Handle edge cases appropriately" → Hot Spot: Undefined edge case handling |
| **Hot Spot** | Complexity flag | Requirements that mention exceptions, fallbacks, special cases, or multiple branching paths without clear resolution | "If payment fails, retry up to 3 times, then escalate or cancel depending on order type" → Hot Spot: Payment failure strategy |
| **Timeline Arrow** | Temporal sequence | "After…", "then…", "once…is complete", "before…", "first…then…", numbered steps in process descriptions | "After the order is placed, payment is processed" → Timeline: `Order Placed` → `Payment Processed` |

---

## Intake Contract

When processing requirements, the agent must:

1. **Declare the input format** — identify which of the supported formats above the
   input matches (may be a mix).
2. **Extract verbatim quotes** — for each ES element identified, record the exact
   text from the requirements that supports it.
3. **Assign confidence** — High (explicit and unambiguous), Medium (implied but
   reasonable), Low (inferred from context, needs human confirmation).
4. **Flag gaps** — elements expected but not found in the requirements (e.g., no
   actors mentioned, no external systems, no policies).
5. **Present extraction summary** — before proceeding to Big Picture generation,
   show the human a table of extracted elements with confidence levels and
   supporting quotes.

### Extraction Summary Format

| ES Element | Name | Confidence | Supporting Quote | Source Location |
|------------|------|-----------|-----------------|----------------|
| Domain Event | `Order Placed` | High | "so that the order is placed" | Story #3 |
| Policy | Large Order Approval | Medium | "orders over $500 require approval" | AC §2.1 |
| Hot Spot | Returns window | Low | "handle returns appropriately" | PRD p.4 |

---

## Handling Ambiguity

| Situation | Agent Action |
|-----------|-------------|
| Requirements use present tense for everything | Convert outcomes to past tense for events, keep imperative for commands |
| No actors specified | Default to "User" for interactive commands; flag as Hot Spot for human to assign specific roles |
| Contradictory requirements | Create a Hot Spot for each contradiction; include both versions in the extraction summary |
| Missing acceptance criteria | Flag affected user stories as Hot Spots; extract events from the "so that" clause only |
| Domain jargon without definitions | Add terms to extraction summary with Low confidence; flag for domain expert review |
| Very high-level requirements (epic-level) | Extract only Big Picture events; note that Process Modeling will need more detailed requirements |
