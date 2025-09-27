# How to Contribute to the Binom API Encyclopedia

This guide is for both human developers and AI agents. By contributing, you help us maintain a 10/10 quality standard.

## 🚀 Guiding Principles

1.  **Quality First**: Every contribution must improve the encyclopedia.
2.  **Automation**: All contributions are validated through an automated pipeline.
3.  **Trust**: Trusted contributors (human or AI) gain more autonomy.
4.  **Collaboration**: We improve this knowledge base together.

## 🤖 The Contribution Workflow

1.  **Fork & Branch**: Create a new branch for your changes.
2.  **Make Changes**: Add or update documentation, examples, or schemas.
3.  **Submit a Pull Request**: Your PR will trigger our automated validation pipeline.

## ✅ The Validation Pipeline (`HybridValidator`)

Your contribution will be automatically validated by our `HybridValidator`. Here’s what it checks:

1.  **Syntax & Schema**: Valid Markdown, JSON, and code syntax.
2.  **API Endpoint Test**: The `APITester` will execute a live test against the relevant Binom API endpoint. The test must pass.
3.  **Dependency Check**: The `DependencyChecker` ensures that related endpoints are not negatively affected.
4.  **Quality Metrics**: The `EnhancedAPITester` calculates a quality score. Your change must not decrease the overall score.

## 🏆 The Trust System (`SimpleTrustSystem`)

Your `agent_id` or GitHub username is tracked to build a trust score.

-   **New Contributors (`trust_score` < 0.75)**: Contributions require manual review and approval, even if validation passes.
-   **Trusted Contributors (`trust_score` >= 0.75)**: Contributions that pass validation are automatically approved.
-   **Expert Contributors (`trust_score` >= 0.85)**: Can approve contributions from others.

**How to increase your trust score:**

-   Submit high-quality contributions that pass validation.
-   Fix issues identified by the validation pipeline.
-   Review and approve valid contributions from others (if you are an Expert).

## ❌ What Happens if Validation Fails?

-   Your pull request will be automatically rejected.
-   A detailed error report will be added to the PR comments.
-   Your trust score will be negatively impacted.
-   You are expected to fix the issues and resubmit.

## 📝 Contribution Guidelines

-   **Endpoint Documentation**: Follow the existing structure. Add real-world examples and schema definitions.
-   **Code Examples**: Must be runnable and tested. Include Python and cURL examples.
-   **Bug Fixes**: Clearly describe the bug and the fix. Include a test case that reproduces the bug.
-   **New Features**: Propose new features via an issue first to discuss with the community.

## ⚖️ Quality Gates

-   **API Success Rate**: Must be > 95%.
-   **Code Validity**: All new code examples must pass testing.
-   **Documentation Completeness**: All new documentation must have a completeness score > 90%.

By following these guidelines, you help us maintain the highest quality standard for the Binom API Encyclopedia. Happy contributing!
