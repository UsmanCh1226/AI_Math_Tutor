"""
stats_solver.py
---------------
Handles statistics problems like mean, median, mode, and standard deviation.
"""

import statistics


def solve_statistics(parsed):
    """
    Solves basic statistics problems.

    Parameters:
        parsed (dict): Contains 'expression' and 'step_by_step' flags.

    Returns:
        str: Answer or step-by-step explanation.
    """

    expr = parsed["expression"]
    step_mode = parsed.get("step_by_step", False)
    steps = []

    # Extract numbers from the expression
    nums = [float(n) for n in expr.replace(",", " ").split() if n.replace('.', '', 1).isdigit()]

    if len(nums) == 0:
        return "Please provide a set of numbers."

    expr_lower = expr.lower()

    if "mean" in expr_lower or "average" in expr_lower:
        mean_val = statistics.mean(nums)
        if not step_mode:
            return f"Mean: {mean_val:.2f}"
        steps.append(f"Numbers: {nums}")
        steps.append(f"Formula: Mean = sum(numbers) / count(numbers)")
        steps.append(f"Calculation: {sum(nums)} / {len(nums)} = {mean_val:.2f}")
        return "\n".join(steps)

    elif "median" in expr_lower:
        median_val = statistics.median(nums)
        if not step_mode:
            return f"Median: {median_val}"
        steps.append(f"Numbers: {nums}")
        steps.append("Median is the middle number when sorted.")
        steps.append(f"Sorted list: {sorted(nums)}")
        steps.append(f"Median = {median_val}")
        return "\n".join(steps)

    elif "mode" in expr_lower:
        try:
            mode_val = statistics.mode(nums)
        except statistics.StatisticsError:
            return "No unique mode found."
        if not step_mode:
            return f"Mode: {mode_val}"
        steps.append(f"Numbers: {nums}")
        steps.append("Mode is the most frequent number.")
        steps.append(f"Mode = {mode_val}")
        return "\n".join(steps)

    elif "standard deviation" in expr_lower:
        stdev_val = statistics.stdev(nums)
        if not step_mode:
            return f"Standard Deviation: {stdev_val:.2f}"
        steps.append(f"Numbers: {nums}")
        steps.append("Formula: sqrt(sum((x - mean)²) / (n-1))")
        steps.append(f"Standard Deviation = {stdev_val:.2f}")
        return "\n".join(steps)

    return "Sorry, I can't solve that statistics problem yet."
