    # Run the line-limit test
    passed = test_line_limit(out_path, max_lines=self.max_lines)

    # NEW: Compute score
    score = self.score_build(code_output, passed, shared["registry"])

    # Capture metadata
    build_record = {
        "id": new_id,
        "task": prep_res[0],
        "file_path": out_path,
        "timestamp": datetime.utcnow().isoformat(),
        "passed_line_test": passed,
        "score": score
    }
    registry["builds"].append(build_record)

    # Write registry
    with open(self.registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    # NEW: Provide feedback with score
    shared["feedback"] = {
        "build_id": new_id,
        "passed_line_test": passed,
        "score": score,
        "remarks": "Build passed." if passed else "Build failed line limit."
    }
