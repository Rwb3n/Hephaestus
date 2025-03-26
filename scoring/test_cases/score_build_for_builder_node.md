def score_build(self, code_output, passed_line_test, registry):
    score = 0

    # 1. Line count efficiency (ideal: use ≤ 90% of 200 lines)
    lines = code_output.strip().splitlines()
    line_count = len(lines)
    line_efficiency = max(0, 1 - line_count / 200)
    score += int(line_efficiency * 40)  # up to 40 points

    # 2. Inclusion of main() block
    if "def main(" in code_output or "if __name__ == '__main__'" in code_output:
        score += 15

    # 3. Reuse of prior imports (check overlap with recent build)
    recent_imports = set()
    for build in reversed(registry["builds"][-5:]):  # look at last 5 builds
        try:
            with open(build["file_path"], "r") as f:
                for line in f:
                    if line.strip().startswith("import ") or line.strip().startswith("from "):
                        recent_imports.add(line.strip())
        except:
            continue

    current_imports = {l.strip() for l in lines if l.strip().startswith("import ") or l.strip().startswith("from ")}
    overlap = len(current_imports & recent_imports)
    score += min(overlap * 2, 15)  # up to 15 points

    # 4. Registry ancestry depth bonus
    score += min(len(registry["builds"]), 30)  # up to 30 points for momentum

    # 5. Line test pass/fail penalty
    if not passed_line_test:
        score -= 25

    return max(score, 0)
