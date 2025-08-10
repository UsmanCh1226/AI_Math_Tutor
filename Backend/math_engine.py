from Solvers.algebra_solver import solve_algebra
from Solvers.calculus_solver import solve_calculus
from Solvers.geometry_solver import solve_geometry
from Solvers.stats_solver import solve_statistics

def solve_expression(parsed):
    subject = parsed.get("subject", "").lower()

    if subject == "algebra":
        return solve_algebra(parsed)
    elif subject == "calculus":
        return solve_calculus(parsed)
    elif subject == "geometry":
        return solve_geometry(parsed)
    elif subject in ["stats", "statistics"]:
        return solve_statistics(parsed)
    else:
        return f"❌ Unknown subject: '{subject}'. Supported: algebra, calculus, geometry, statistics."
