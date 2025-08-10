"""
geometry_solver.py
------------------
Handles basic geometry problems like calculating area, perimeter, and volume
for common shapes.
"""


def solve_geometry(parsed):
    """
    Solves geometry problems based on the parsed input.

    Parameters:
        parsed (dict):
            {
                "expression": "area of circle radius=5",
                "step_by_step": True/False
            }

    Returns:
        str: Answer string (with explanation if step_by_step=True)
    """
    expr = parsed.get("expression", "").lower()
    step_mode = parsed.get("step_by_step", False)

    steps = []

    # Circle area
    if "area" in expr and "circle" in expr:
        try:
            # Extract radius value
            radius_str = expr.split("radius=")[1]
            radius = float(radius_str)
            area = 3.14159 * radius ** 2

            if not step_mode:
                return f"Area of circle: {area:.2f} units²"

            steps.append("We are finding the area of a circle.")
            steps.append(f"Formula: Area = π × r²")
            steps.append(f"Radius r = {radius}")
            steps.append(f"Calculation: π × {radius}² = {area:.2f}")
            return "\n".join(steps)

        except Exception as e:
            return f"Error calculating circle area: {e}"

    # Rectangle area
    elif "area" in expr and "rectangle" in expr:
        try:
            width = float(expr.split("width=")[1].split()[0])
            height = float(expr.split("height=")[1])
            area = width * height

            if not step_mode:
                return f"Area of rectangle: {area:.2f} units²"

            steps.append("We are finding the area of a rectangle.")
            steps.append(f"Formula: Area = width × height")
            steps.append(f"Width = {width}, Height = {height}")
            steps.append(f"Calculation: {width} × {height} = {area:.2f}")
            return "\n".join(steps)

        except Exception as e:
            return f"Error calculating rectangle area: {e}"

    else:
        return "Geometry solver currently supports: area of circle, area of rectangle."
