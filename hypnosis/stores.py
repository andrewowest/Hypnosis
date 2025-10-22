from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .core import HypnotizedFact, MemoryStore


class JSONLMemoryStore(MemoryStore):
    """JSONL-based memory store for hypnotized facts."""
    
    def __init__(self, storage_path: Path | str) -> None:
        """Initialize JSONL store.
        
        Args:
            storage_path: Path to JSONL file
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.storage_path.exists():
            self.storage_path.write_text("", encoding="utf-8")
    
    def write(self, fact: HypnotizedFact) -> None:
        """Append fact to JSONL file."""
        with self.storage_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(fact.to_dict(), ensure_ascii=False) + "\n")
    
    def read_all(self) -> List[HypnotizedFact]:
        """Read all facts from JSONL file."""
        if not self.storage_path.exists():
            return []
        
        facts: List[HypnotizedFact] = []
        lines = self.storage_path.read_text(encoding="utf-8").splitlines()
        
        for line in lines:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                facts.append(HypnotizedFact.from_dict(data))
            except (json.JSONDecodeError, KeyError):
                continue
        
        return facts
    
    def delete(self, fact_id: str) -> bool:
        """Remove fact by rewriting file without the target ID."""
        facts = self.read_all()
        original_count = len(facts)
        
        facts = [f for f in facts if f.id != fact_id]
        
        if len(facts) == original_count:
            return False
        
        # Rewrite file
        with self.storage_path.open("w", encoding="utf-8") as f:
            for fact in facts:
                f.write(json.dumps(fact.to_dict(), ensure_ascii=False) + "\n")
        
        return True
