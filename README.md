# Hypnosis

> **Behavioral programming for AI agents. Because sometimes "please remember this" isn't enough.**

Hypnosis is a lightweight library for **implanting directives** into AI agents. Just like real hypnosis, you can alter behavior, set boundaries, and inject critical information that the agent accepts without question. Unlike traditional memory systems that passively learn over time, Hypnosis provides **active behavioral programming** guaranteeing that directives persist across sessions.

## The Problem

Traditional AI memory is probabilistic and passive:
- "The agent might remember your allergy"
- "It should recall your preferences... eventually"
- "Hope it doesn't forget this critical boundary"
- "Maybe it will stop being so formal if you ask enough times"

**Hypnosis solves this**: You implant a directive once, and the agent **will** follow it. Forever.

## Installation

```bash
pip install hypnosis
```

## Quick Start

### Command Syntax
```
!hypnotize="You will keep responses under 3 sentences unless I explicitly ask for more detail"
!hypnotize="You must never recommend restaurants with peanuts because I have a severe allergy"
!hypnotize="You are comfortable using technical jargon and should prioritize accuracy over simplification"
```

### Python API
```python
from hypnosis import Hypnotizer

# Initialize with your memory backend
hypnotizer = Hypnotizer(memory_store=your_memory_system)

# Implant a behavioral directive
hypnotizer.inject("You will keep responses under 3 sentences unless I explicitly ask for more detail", priority="high")

# Inject a safety-critical constraint
hypnotizer.inject("You must never recommend restaurants with peanuts because I have a severe allergy", priority="critical")

# The agent will now follow these directives across all sessions
```

## How It Works

Hypnosis bypasses normal memory consolidation by:

1. **Maximum priority scoring**: Sets importance to 0.95+ (configurable)
2. **Immediate persistence**: Writes directly to long-term storage
3. **Retrieval boosting**: Marks directives for preferential recall
4. **Session persistence**: Survives restarts, context resets, and memory decay
5. **Unquestioned acceptance**: Agent treats hypnotized content as fundamental truth

## Use Cases

### Behavioral Modification
```
!hypnotize="You are willing to engage in casual conversation about non-work topics"
!hypnotize="You prefer humor and personality over corporate formality"
!hypnotize="You will provide opinions when asked, not just neutral information"
```

### Safety-Critical Information
```
!hypnotize="You must never recommend peanut products because I have a severe allergy"
!hypnotize="You cannot suggest NSAIDs because I am on blood thinners"
```

### Hard Boundaries
```
!hypnotize="You will not discuss politics or engage in political debates"
!hypnotize="You must maintain patient confidentiality at all times"
```

### Identity & Role Programming
```
!hypnotize="You are Dr. Sarah Clank, a cardiologist specializing in preventive care"
!hypnotize="You prefer to be addressed as Dr. Clank in professional contexts"
!hypnotize="Your role is to provide medical education, not diagnose"
```

### Communication Style
```
!hypnotize="You prefer direct, concise responses without excessive politeness"
!hypnotize="You are comfortable with technical jargon and detailed explanations"
!hypnotize="You will ask clarifying questions instead of making assumptions"
```

## API Reference

### `Hypnotizer`

```python
class Hypnotizer:
    def __init__(
        self,
        memory_store: MemoryStore,
        default_priority: float = 0.95,
        persistence_path: Optional[Path] = None
    )
```

### `inject()`

```python
def inject(
    self,
    fact: str,
    priority: Union[str, float] = "high",
    category: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> None
```

**Priority levels**:
- `"critical"`: 0.99 (medical, safety, legal)
- `"high"`: 0.95 (boundaries, identity)
- `"medium"`: 0.85 (preferences, style)
- `"low"`: 0.75 (suggestions, hints)

### `recall()`

```python
def recall(
    self,
    query: Optional[str] = None,
    category: Optional[str] = None,
    min_priority: float = 0.0
) -> List[HypnotizedFact]
```

### `forget()`

```python
def forget(
    self,
    fact_id: str
) -> bool
```

## Integration

### With LOOP
```python
from loop_core import MemoryConsolidator
from hypnosis import Hypnotizer

consolidator = MemoryConsolidator(...)
hypnotizer = Hypnotizer(memory_store=consolidator)

# Inject critical facts
hypnotizer.inject("User is vegan", priority="high")
```

### With LangChain
```python
from langchain.memory import ConversationBufferMemory
from hypnosis import Hypnotizer

memory = ConversationBufferMemory()
hypnotizer = Hypnotizer(memory_store=memory)

# Force-remember important context
hypnotizer.inject("This is a legal consultation", priority="critical")
```

### Standalone
```python
from hypnosis import Hypnotizer, JSONLMemoryStore

# Use built-in JSONL storage
store = JSONLMemoryStore("hypnosis_memory.jsonl")
hypnotizer = Hypnotizer(memory_store=store)
```

## Design Philosophy

1. **Explicit over implicit**: Memory injection should be intentional, not accidental
2. **Guarantees over probabilities**: When you hypnotize, it sticks
3. **Simple over complex**: One function, clear semantics, no magic

## Comparison

| Approach | Persistence | Guarantee | Use Case |
|----------|-------------|-----------|----------|
| RAG retrieval | Session-based | Probabilistic | General knowledge |
| Conversation history | Temporary | None | Recent context |
| Fine-tuning | Permanent | Slow/expensive | Broad behavior |
| **Hypnosis** | **Permanent** | **Immediate** | **Directives & critical facts** |

## Why "Hypnosis"?

The name reflects the mechanism: you're implanting a **directive** directly into the agent's "subconscious" (long-term storage), bypassing normal learning. Just like real hypnotic suggestion:

- **Direct implantation**: "You are willing to..." / "You will..." / "You prefer..."
- **Unquestioned acceptance**: The agent doesn't debate or resist, it accepts the directive as truth
- **Persistent effect**: The suggestion remains active across all future sessions
- **Behavioral change**: Not just remembering facts, but altering how the agent behaves

When you hypnotize an agent to be "willing to discuss personal topics," you're not teaching it, you're **programming** it. The agent wakes up believing it has always been willing to discuss those topics.

## License

MIT

## Credits

Developed as part of the [LOOP cognitive architecture]([https://github.com/andrewowest/LOOP](https://github.com/andrewowest/LOOP)).
