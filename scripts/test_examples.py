#!/usr/bin/env python3
"""
This script automatically finds and tests all code examples (Python and cURL)
within the markdown documentation.
"""

import os
import re
import tempfile
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
                
                code = code.replace("os.getenv('binomPublic')", f'"{os.getenv("binomPublic")}"')

                success = False
                output = ""
                temp_file_path = None

                try:
                    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=f".{lang}") as temp_file:
                        if lang == "curl":
                            if "api-key" not in code:
                                code = code.replace("curl", 'curl -H "api-key: ' + os.getenv("binomPublic") + '"')
                        temp_file.write(code)
                        temp_file_path = temp_file.name

                    if lang == "python":
                        result = subprocess.run(
                            ["python3", temp_file_path],
                            capture_output=True, 
                            text=True, 
                            timeout=30, 
                            check=False,
                            cwd=os.path.dirname(temp_file_path)
                        )
                    elif lang == "curl":
                        result = subprocess.run(
                            ["bash", temp_file_path],
                            capture_output=True, 
                            text=True, 
                            timeout=30, 
                            check=False,
                            cwd=os.path.dirname(temp_file_path)
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
                    logger.warning(f"Test timed out for {lang} example in {md_file.name}")
                except subprocess.CalledProcessError as e:
                    output = f"Process failed with return code {e.returncode}: {e.stderr}"
                    logger.error(f"Process failed for {lang} example in {md_file.name}: {e}")
                except Exception as e:
                    output = f"An unexpected error occurred: {e}"
                    logger.error(f"Unexpected error for {lang} example in {md_file.name}: {e}")
                finally:
                    if temp_file_path and os.path.exists(temp_file_path):
                        try:
                            os.remove(temp_file_path)
                        except OSError as e:
                            logger.warning(f"Failed to remove temporary file {temp_file_path}: {e}")

                if success:
                    print(f"    ✅ PASS: {output[:150]}")
                    logger.info(f"Test passed for {lang} example in {md_file.name}")
                else:
                    print(f"    ❌ FAIL: {output[:150]}")
                    logger.warning(f"Test failed for {lang} example in {md_file.name}: {output[:150]}")

        except Exception as e:
            print(f"  Error processing file {md_file}: {e}")
            logger.error(f"Error processing file {md_file}: {e}")
        print("\n")

    print("--- Code Example Test Suite Finished ---")
    print(f"Summary: {passed_tests} / {total_tests} tests passed.")
    logger.info(f"Test suite completed: {passed_tests}/{total_tests} tests passed")

if __name__ == "__main__":
    if not os.getenv("binomPublic"):
        print("CRITICAL ERROR: `binomPublic` environment variable not set.")
        logger.critical("binomPublic environment variable not set")
    else:
        test_code_examples()
