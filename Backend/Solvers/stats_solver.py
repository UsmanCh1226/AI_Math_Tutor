"""
stats_solver.py
---------------
Handles basic statistics problems like mean, median, variance, and probability.
"""

import statistics as stats


def solve_statistics(parsed):
    """
    Solves statistics problems based on the parsed input.

    Parameters:
        parsed (dict):
            {
                "expression": "mean of 2,4,6,8",
                "step_by_step": True/False
            }

    Returns:
        str: Answer string (with explanation if step_by_step=True)
    """
    expr = parsed.get("expression", "").lower()
    step_mode = parsed.get("step_by_step", False)
    steps = []

    try:
        # Extract numbers
        if "of" in expr:
            numbers_str = expr.split("of")[1]
        else:
            numbers_str = expr
        numbers = [float(x) for x in numbers_str.replace(",", " ").split() if x.strip()]

        # Mean
        if "mean" in expr:
            mean_val = stats.mean(numbers)
            if not step_mode:
                return f"Mean: {mean_val:.2f}"
            steps.append("We are calculating the mean (average).")
            steps.append(f"Numbers: {numbers}")
            steps.append(f"Formula: Mean = sum(numbers) / count")
            steps.append(f"Calculation: {sum(numbers)} / {len(numbers)} = {mean_val:.2f}")
            return "\n".join(steps)

        # Median
        elif "median" in expr:
            median_val = stats.median(numbers)
            if not step_mode:
                return f"Median: {median_val:.2f}"
            steps.append("We are calculating the median (middle value).")
            steps.append(f"Numbers: {numbers}")
            steps.append("Sort the numbers, pick the middle (or average of two middle values).")
            steps.append(f"Result: {median_val:.2f}")
            return "\n".join(steps)

        # Variance
        elif "variance" in expr:
            variance_val = stats.variance(numbers)
            if not step_mode:
                return f"Variance: {variance_val:.2f}"
            steps.append("We are calculating the variance.")
            steps.append(f"Numbers: {numbers}")
            steps.append("Formula: Variance = average of squared differences from the mean.")
            steps.append(f"Result: {variance_val:.2f}")
            return "\n".join(steps)

        else:
            return "Supported stats operations: mean, median, variance."

    except Exception as e:
        return f"Error processing statistics: {e}"
