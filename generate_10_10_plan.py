from checklists.checklist_system import Checklist, ChecklistItem, ChecklistManager

def create_10_10_quality_checklist() -> Checklist:
    """Create checklist for achieving 10/10 repository quality"""
    checklist = Checklist(
        "10_10_quality",
        "Comprehensive plan to achieve 10/10 repository quality, based on Claude AI recommendations"
    )
    
    quality_items = [
        # 1. Documentation Quality
        ("doc_style_guide", "Create a unified style guide for documentation", "", True),
        ("doc_linting", "Implement automatic documentation quality checks (vale, markdownlint)", "", True),
        ("doc_structure", "Structure documentation by complexity (Quick Start, Core Concepts, Advanced, API Reference)", "", True),
        ("doc_interactive_examples", "Add interactive examples (e.g., CodeSandbox)", "", False),
        ("doc_versioning", "Implement documentation versioning", "", True),

        # 2. Technical Quality
        ("ci_cd_pipeline", "Configure a full CI/CD pipeline (lint, test, security, build, deploy)", "", True),
        ("api_doc_generation", "Add automatic generation of API documentation from code/specs", "", True),
        ("code_typing", "Enforce 100% type hinting coverage in all Python code", "", True),
        ("dependabot", "Configure Dependabot for automatic dependency updates", "", True),

        # 3. AI/User Experience
        ("ai_agent_section", "Create a dedicated section for AI agents (/ai/prompts, /ai/examples, etc.)", "", True),
        ("structured_metadata", "Add structured metadata in JSON for AI consumption", "", True),
        ("ai_content_index", "Create an AI-friendly content index", "", True),
        ("ai_specific_examples", "Develop API interaction examples specifically for AI agents", "", True),

        # 4. Automation
        ("openapi_validation", "Set up automatic validation of OpenAPI specifications", "", True),
        ("example_updater", "Implement a system to automatically update code examples", "", True),
        ("doc_freshness_check", "Create a system to check for outdated documentation", "", True),
        ("changelog_generation", "Automate changelog generation from commit messages", "", True),

        # 5. Testing
        ("unit_tests", "Implement unit tests for all components (pytest)", "", True),
        ("integration_tests", "Add integration tests for API examples", "", True),
        ("e2e_tests", "Create end-to-end tests for documentation and user workflows", "", False),
        ("multi_env_testing", "Set up testing in multiple environments (e.g., different Python versions)", "", True),
        ("test_coverage_90", "Achieve >90% code test coverage", "", True),

        # 6. Quality Monitoring
        ("sonarqube", "Integrate SonarQube for continuous code quality analysis", "", False),
        ("doc_quality_metrics", "Define and monitor documentation quality metrics (readability, completeness, etc.)", "", True),
        ("quality_dashboard", "Create a dashboard with key quality metrics", "", False),
        ("quality_reporting", "Set up automated quality reports", "", False),
    ]
    
    for item_id, title, description, required in quality_items:
        checklist.add_item(ChecklistItem(item_id, title, description, required))
        
    return checklist

if __name__ == "__main__":
    manager = ChecklistManager()
    quality_checklist = create_10_10_quality_checklist()
    filepath = manager.save_checklist(quality_checklist)
    print(f"Saved checklist to: {filepath}")
    report = manager.generate_checklist_report(quality_checklist)
    with open("10_10_quality_plan.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("Generated report and saved to 10_10_quality_plan.md")

