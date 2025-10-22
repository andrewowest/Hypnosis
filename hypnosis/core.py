from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union


PRIORITY_LEVELS = {
    "critical": 0.99,
    "high": 0.95,
    "medium": 0.85,
    "low": 0.75,
}


@dataclass
class HypnotizedFact:
    """A fact injected via hypnosis with guaranteed persistence."""
    
    id: str
    fact: str
    priority: float
    category: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "fact": self.fact,
            "priority": self.priority,
            "category": self.category,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> HypnotizedFact:
        return cls(
            id=data["id"],
            fact=data["fact"],
            priority=data["priority"],
            category=data.get("category"),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", datetime.utcnow().isoformat() + "Z"),
        )


class MemoryStore(ABC):
    """Abstract interface for memory backends."""
    
    @abstractmethod
    def write(self, fact: HypnotizedFact) -> None:
        """Persist a hypnotized fact."""
        pass
    
    @abstractmethod
    def read_all(self) -> List[HypnotizedFact]:
        """Retrieve all hypnotized facts."""
        pass
    
    @abstractmethod
    def delete(self, fact_id: str) -> bool:
        """Remove a hypnotized fact by ID."""
        pass


class Hypnotizer:
    """Direct memory injection for AI agents."""
    
    def __init__(
        self,
        memory_store: MemoryStore,
        default_priority: float = 0.95,
    ) -> None:
        """Initialize hypnotizer.
        
        Args:
            memory_store: Backend for persisting hypnotized facts
            default_priority: Default importance score (0.0-1.0)
        """
        self.memory_store = memory_store
        self.default_priority = default_priority
    
    def inject(
        self,
        fact: str,
        priority: Union[str, float] = "high",
        category: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> HypnotizedFact:
        """Inject a fact directly into long-term memory.
        
        Args:
            fact: The information to remember
            priority: Importance level ("critical", "high", "medium", "low") or float (0.0-1.0)
            category: Optional category for organization
            metadata: Additional context
            
        Returns:
            The hypnotized fact object
        """
        if isinstance(priority, str):
            priority_value = PRIORITY_LEVELS.get(priority.lower(), self.default_priority)
        else:
            priority_value = max(0.0, min(1.0, float(priority)))
        
        hypnotized = HypnotizedFact(
            id=str(uuid.uuid4()),
            fact=fact.strip(),
            priority=priority_value,
            category=category,
            metadata=metadata or {},
        )
        
        self.memory_store.write(hypnotized)
        return hypnotized
    
    def recall(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_priority: float = 0.0,
    ) -> List[HypnotizedFact]:
        """Retrieve hypnotized facts.
        
        Args:
            query: Optional text filter (substring match)
            category: Optional category filter
            min_priority: Minimum priority threshold
            
        Returns:
            List of matching hypnotized facts, sorted by priority (descending)
        """
        facts = self.memory_store.read_all()
        
        # Apply filters
        if category is not None:
            facts = [f for f in facts if f.category == category]
        
        if min_priority > 0.0:
            facts = [f for f in facts if f.priority >= min_priority]
        
        if query is not None:
            query_lower = query.lower()
            facts = [f for f in facts if query_lower in f.fact.lower()]
        
        # Sort by priority (highest first)
        facts.sort(key=lambda f: f.priority, reverse=True)
        return facts
    
    def forget(self, fact_id: str) -> bool:
        """Remove a hypnotized fact.
        
        Args:
            fact_id: ID of the fact to remove
            
        Returns:
            True if fact was removed, False if not found
        """
        return self.memory_store.delete(fact_id)
    
    def list_categories(self) -> List[str]:
        """Get all unique categories."""
        facts = self.memory_store.read_all()
        categories = {f.category for f in facts if f.category is not None}
        return sorted(categories)
