class DirectiveLoader(Node):
    def exec(self, _):
        import yaml
        with open("heph/engine/prime_directive.yaml") as f:
            directive = yaml.safe_load(f)
        return directive

class FlowBuilderNode(Node):
    def prep(self, shared):
        return shared["build_task"]

    def exec(self, task):
        # Generate flow or node code from task
        prompt = f"""
Prime Directive:
{shared['directive']}

Task:
{task}

Generate a Python class that adheres to the directive, including:
- File under 200 lines
- Uses modular structure
- Includes main() for testing
- Adds logging
"""
        return call_llm(prompt)

    def post(self, shared, prep_res, code_output):
        # Save to file
        path = f"heph/builds/build_{shared['registry']['last_build_id'] + 1}.py"
        with open(path, "w") as f:
            f.write(code_output)

        # Update registry
        shared["registry"]["last_build_id"] += 1
        shared["registry"]["builds"].append({
            "id": shared["registry"]["last_build_id"],
            "task": prep_res,
            "path": path,
            "timestamp": datetime.utcnow().isoformat()
        })

        return "default"