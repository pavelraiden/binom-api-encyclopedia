#!/usr/bin/env python3
"""
This script automatically finds and tests all code examples (Python and cURL)
within the markdown documentation.
"""

import os
import re
import subprocess
from pathlib import Path


def find_md_files():
    """Finds all markdown files in the docs/endpoints directory."""
    docs_path = Path("/home/ubuntu/binom-api-encyclopedia/docs/endpoints")
    return list(docs_path.rglob("*.md"))

def test_code_examples():
    """Finds, extracts, and tests code examples from markdown files."""
    md_files = find_md_files()
    total_tests = 0
    passed_tests = 0

    print(f"--- Starting Code Example Test Suite for {len(md_files)} files ---\n")

    # Regex to find python and curl code blocks
    code_block_regex = re.compile(r"```(python|curl)\n(.*?)\n```", re.DOTALL)

    for md_file in md_files:
        print(f"--- Testing file: {md_file.name} ---")
        try:
            content = md_file.read_text(encoding="utf-8")
            code_blocks = code_block_regex.findall(content)

            if not code_blocks:
                print("    No runnable code examples found.")
                continue

            for lang, code in code_blocks:
                total_tests += 1
                print(f"  - Found {lang} example. Running test...")
                
                # Replace placeholder API key if present
                code = code.replace("os.getenv('binomPublic')", f'"{os.getenv("binomPublic")}"')

                success = False
                output = ""

                try:
                    if lang == "python":
                        # Execute Python code
                        result = subprocess.run(
                            ["python3", "-c", code],
                            capture_output=True, text=True, timeout=30
                        )
                    elif lang == "curl":
                        # Execute cURL command
                        # Add -s -S for silent but show errors
                        if "api-key" not in code:
                            code = code.replace("curl", 'curl -H "api-key: ' + os.getenv("binomPublic") + '"')
                        result = subprocess.run(
                            code, shell=True, capture_output=True, text=True, timeout=30
                        )

                    if result.returncode == 0:
                        success = True
                        passed_tests += 1
                        output = result.stdout.strip()
                        if not output:
                            output = "(No output, but exited successfully)"
                    else:
                        output = result.stderr.strip()

                except subprocess.TimeoutExpired:
                    output = "Test timed out after 30 seconds."
                except Exception as e:
                    output = f"An unexpected error occurred: {e}"

                if success:
                    print(f"    ✅ PASS: {output[:150]}")
                else:
                    print(f"    ❌ FAIL: {output[:150]}")

        except Exception as e:
            print(f"  Error processing file {md_file}: {e}")
        print("\n")

    print("--- Code Example Test Suite Finished ---")
    print(f"Summary: {passed_tests} / {total_tests} tests passed.")

if __name__ == "__main__":
    if not os.getenv("binomPublic"):
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
    else:
        test_code_examples()

