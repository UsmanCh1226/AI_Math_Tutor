"""
geometry_solver.py
------------------
Handles geometry-related math problems like area, perimeter, and volume.
"""

import math


def solve_geometry(parsed):
    """
    Solves geometry problems based on keywords and numeric values.

    Parameters:
        parsed (dict): Contains 'expression' and 'step_by_step' flags.

    Returns:
        str: Answer or step-by-step explanation.
    """

    expr = parsed["expression"]
    step_mode = parsed.get("step_by_step", False)
    steps = []

    # Lowercase for easier keyword matching
    expr_lower = expr.lower()

    # Extract numbers from the expression
    nums = [float(n) for n in expr_lower.split() if n.replace('.', '', 1).isdigit()]

    # AREA & PERIMETER
    if "circle" in expr_lower and "area" in expr_lower:
        if len(nums) < 1:
            return "Please provide the radius."
        r = nums[0]
        area = math.pi * r**2
        if not step_mode:
            return f"Area of the circle: {area:.2f}"
        steps.append(f"Given radius r = {r}")
        steps.append("Formula: Area = π * r²")
        steps.append(f"Calculation: π * {r}² = {area:.2f}")
        return "\n".join(steps)

    elif "circle" in expr_lower and "perimeter" in expr_lower or "circumference" in expr_lower:
        if len(nums) < 1:
            return "Please provide the radius."
        r = nums[0]
        perimeter = 2 * math.pi * r
        if not step_mode:
            return f"Circumference of the circle: {perimeter:.2f}"
        steps.append(f"Given radius r = {r}")
        steps.append("Formula: Circumference = 2 * π * r")
        steps.append(f"Calculation: 2 * π * {r} = {perimeter:.2f}")
        return "\n".join(steps)

    # VOLUME
    elif "sphere" in expr_lower and "volume" in expr_lower:
        if len(nums) < 1:
            return "Please provide the radius."
        r = nums[0]
        volume = (4/3) * math.pi * r**3
        if not step_mode:
            return f"Volume of the sphere: {volume:.2f}"
        steps.append(f"Given radius r = {r}")
        steps.append("Formula: Volume = 4/3 * π * r³")
        steps.append(f"Calculation: 4/3 * π * {r}³ = {volume:.2f}")
        return "\n".join(steps)

    return "Sorry, I don't yet know how to solve that geometry problem."
