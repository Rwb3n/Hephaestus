"""
BestOfNBuilder - Generates multiple solution variants and selects the best one.

DEPRECATED: This implementation is being phased out. Please use scoring.best_of_n.BestOfNBuilder instead.
"""

import warnings
import logging

# Show deprecation warning when module is imported
warnings.warn(
    "The engine.best_of_n module is deprecated and will be removed in a future version. "
    "Use scoring.best_of_n.BestOfNBuilder instead.",
    DeprecationWarning, stacklevel=2
)

class BestOfNBuilder:

    def __init__(self, n=3):
        warnings.warn(
            "This BestOfNBuilder implementation is deprecated. Use scoring.best_of_n.BestOfNBuilder instead.",
            DeprecationWarning, stacklevel=2
        )
        self.n = n
        self.builder = FlowBuilderNode()  # uses the builder we built earlier

    def prep(self, shared):
        return shared["build_task"], shared["directive"], shared.get("registry", None)

    def exec(self, inputs):
        def __init__(self, n=3):
            self.n = n
            self.builder = FlowBuilderNode()
            self.mutator = MutationEngine()
        build_task, directive, registry = inputs

        mutated_task, mutated_directive = self.mutator.mutate(build_task, directive)

        candidates = []
        for i in range(self.n):
            shared = {
                "build_task": mutated_task,
                "directive": mutated_directive,
                "registry": registry if registry else {
                    "builds": [], "lineage": {}, "last_build_id": 0
                }
            }
            # Run builder subflow
            prep = self.builder.prep(shared)
            code = self.builder.exec(prep)
            result = self.builder.post(shared, prep, code)

            candidates.append({
                "id": shared["feedback"]["build_id"],
                "score": shared["feedback"]["score"],
                "file": shared["registry"]["builds"][-1]["file_path"],
                "remarks": shared["feedback"]["remarks"],
                "passed": shared["feedback"]["passed_line_test"],
                "code": code
            })

        return candidates

    def post(self, shared, prep_res, candidates):
        # Pick best scoring build
        best = max(candidates, key=lambda x: x["score"])

        shared["feedback"] = {
            "best_id": best["id"],
            "best_score": best["score"],
            "file_path": best["file"],
            "remarks": best["remarks"],
            "passed": best["passed"]
        }

        logging.info(f"[BestOfN] Selected Build {best['id']} with score {best['score']}: {best['file']}")

        return "default"
    
    ###### Example Usage ######

#    best_builder = BestOfNBuilder(n=5)

#    shared = {
#        "build_task": "Build a Node that downloads a file from a URL and saves it to disk",
#        "directive": {
#            "goal": "Extend system capabilities",
#            "constraints": {
#                "max_lines_per_file": 200,
#                "require_registry_logging": True
#            },
#            "reward_criteria": ["efficiency", "reusability", "compliance"]
#        }
#    }

#    inputs = best_builder.prep(shared)
#    candidates = best_builder.exec(inputs)
#    best_builder.post(shared, inputs, candidates)

#    print(json.dumps(shared["feedback"], indent=2))

###### Output Example ######

# Output Example
# If input is:

# "Build a Node that fetches weather data and logs it"

# You might see:

# "Assemble a minimal Node that gathers weather data"

# "Forge a reusable Node that pulls weather data from API"

# "Construct a robust async-compatible Node to harvest weather metrics"

# Same idea. Different language. Different prompt trajectories.