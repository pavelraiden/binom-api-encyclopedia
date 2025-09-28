from checklists.checklist_system import ChecklistManager

manager = ChecklistManager()

# Create the 10/10 quality checklist
quality_checklist = manager.create_10_10_quality_checklist()
print("Created 10/10 quality checklist")

# Save it
filepath = manager.save_checklist(quality_checklist)
print(f"Saved checklist to: {filepath}")

# Generate report
report = manager.generate_checklist_report(quality_checklist)

# Save report to a file
with open("10_10_quality_plan.md", "w", encoding="utf-8") as f:
    f.write(report)

print("\nGenerated report and saved to 10_10_quality_plan.md")

