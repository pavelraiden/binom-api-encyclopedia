import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class ChecklistStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class ChecklistItem:
    def __init__(self, id: str, title: str, description: str = "", required: bool = True):
        self.id = id
        self.title = title
        self.description = description
        self.required = required
        self.status = ChecklistStatus.PENDING
        self.completed_at = None
        self.notes = ""

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "required": self.required,
            "status": self.status.value,
            "completed_at": self.completed_at,
            "notes": self.notes
        }

class Checklist:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.items: List[ChecklistItem] = []
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def add_item(self, item: ChecklistItem):
        self.items.append(item)

    def get_progress(self) -> Dict:
        total = len(self.items)
        if total == 0:
            return {"total": 0, "completed": 0, "failed": 0, "pending": 0, "progress_percentage": 0}
        completed = len([item for item in self.items if item.status == ChecklistStatus.COMPLETED])
        failed = len([item for item in self.items if item.status == ChecklistStatus.FAILED])
        pending = total - completed - failed
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "progress_percentage": (completed / total * 100)
        }

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "items": [item.to_dict() for item in self.items]
        }

class ChecklistManager:
    def __init__(self, storage_path: str = "/home/ubuntu/binom-api-encyclopedia/checklists/data"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def save_checklist(self, checklist: Checklist) -> str:
        filename = f"{checklist.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.storage_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(checklist.to_dict(), f, indent=2, ensure_ascii=False)
        return filepath

    def generate_checklist_report(self, checklist: Checklist) -> str:
        progress = checklist.get_progress()
        report = f"""# 📋 Checklist Report: {checklist.name}\n
**Description:** {checklist.description}\n**Created:** {checklist.created_at}\n**Progress:** {progress["completed"]}/{progress["total"]} ({progress["progress_percentage"]:.1f}%%)\n\n## 📊 Status Overview\n- ✅ Completed: {progress["completed"]}\n- ❌ Failed: {progress["failed"]}\n- ⏳ Pending: {progress["pending"]}\n- 📝 Total: {progress["total"]}\n\n## 📝 Detailed Items\n\n"""
        for item in checklist.items:
            status_emoji = {
                ChecklistStatus.COMPLETED: "✅",
                ChecklistStatus.FAILED: "❌",
                ChecklistStatus.PENDING: "⏳",
                ChecklistStatus.IN_PROGRESS: "🔄",
                ChecklistStatus.SKIPPED: "⏭️"
            }
            emoji = status_emoji.get(item.status, "❓")
            required_text = " (Required)" if item.required else " (Optional)"
            report += f"### {emoji} {item.title}{required_text}\n"
            report += f"**Description:** {item.description}\n"
            report += f"**Status:** {item.status.value}\n"
            if item.notes:
                report += f"**Notes:** {item.notes}\n"
            if item.completed_at:
                report += f"**Completed:** {item.completed_at}\n"
            report += "\n"
        return report

