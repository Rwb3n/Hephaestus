import os
import json
import logging
from datetime import datetime

############################
# Assume these exist:
#  1) "call_llm(prompt)" function
#  2) "test_line_limit(file_path, max_lines)" function
############################

class FlowBuilderNode:
    """
    A Node-like object that:
      1) Reads a 'build_task' from shared store
      2) Calls LLM to produce a .py file
      3) Saves file
      4) Runs line-count test (or any other test)
      5) Updates registry with pass/fail, logs feedback
    """

    def __init__(self, max_lines=200, builds_dir="heph/builds/", registry_path="heph/engine/registry.json"):
        self.max_lines = max_lines
        self.builds_dir = builds_dir
        self.registry_path = registry_path

    def prep(self, shared):
        # The 'prep' step extracts the build task and directive from shared data
        build_task = shared.get("build_task", "No task specified")
        directive = shared.get("directive", {})
        return (build_task, directive)

    def exec(self, inputs):
        # The 'exec' step calls the LLM to generate code
        build_task, directive = inputs
        directive_str = json.dumps(directive, indent=2) if directive else "No directive found"

        prompt = f"""
You are Hephaestus. Prime Directive:
{directive_str}

Create a Python module that implements the following build task in under {self.max_lines} lines.
Task: {build_task}

Requirements:
- Must not exceed {self.max_lines} lines
- Must be self-contained
- Must have a main() test or usage example
- Must log or print a success message on run
"""
        code_output = call_llm(prompt)
        return code_output

    def post(self, shared, prep_res, code_output):
        # The 'post' step saves the file, runs tests, updates registry, and logs feedback

        # Load or create the registry in shared
        if "registry" not in shared:
            try:
                with open(self.registry_path, "r") as f:
                    shared["registry"] = json.load(f)
            except:
                shared["registry"] = {"builds": [], "lineage": {}, "last_build_id": 0}

        registry = shared["registry"]

        # Determine build ID and output path
        new_id = registry["last_build_id"] + 1
        registry["last_build_id"] = new_id

        out_path = os.path.join(self.builds_dir, f"build_{new_id}.py")
        os.makedirs(self.builds_dir, exist_ok=True)

        # Save the generated code
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code_output)

        # Run the line-limit test
        passed = test_line_limit(out_path, max_lines=self.max_lines)

        # Capture metadata
        build_record = {
            "id": new_id,
            "task": prep_res[0],
            "file_path": out_path,
            "timestamp": datetime.utcnow().isoformat(),
            "passed_line_test": passed
        }
        registry["builds"].append(build_record)

        # Write registry back to disk
        with open(self.registry_path, "w") as f:
            json.dump(registry, f, indent=2)

        # Log results
        if passed:
            logging.info(f"[Build {new_id}] PASSED line-limit test: {out_path}")
            shared["feedback"] = {
                "build_id": new_id,
                "passed_line_test": True,
                "remarks": "Build file is within line limit."
            }
            return "default"  # or "success"
        else:
            logging.warning(f"[Build {new_id}] FAILED line-limit test: {out_path}")
            shared["feedback"] = {
                "build_id": new_id,
                "passed_line_test": False,
                "remarks": "Build file exceeded line limit."
            }
            return "test_failed"
