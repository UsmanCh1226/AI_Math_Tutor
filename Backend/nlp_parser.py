

import re
from nlp_preprocessor import normalize_math_text, detect_variables, split_multi_steps

# operation → (topic, canonical_operation)
OP_KEYWORDS = {
    "differentiate": ("calculus", "differentiate"),
    "derivative": ("calculus", "differentiate"),
    "integrate": ("calculus", "integrate"),
    "antiderivative": ("calculus", "integrate"),
    "simplify": ("algebra", "simplify"),
    "expand": ("algebra", "expand"),
    "factor": ("algebra", "factor"),
    "solve": ("algebra", "solve"),
    "area": ("geometry", "area"),
    "perimeter": ("geometry", "perimeter"),
    "circumference": ("geometry", "perimeter"),
    "volume": ("geometry", "volume"),
    "mean": ("statistics", "mean"),
    "average": ("statistics", "mean"),
    "median": ("statistics", "median"),
    "mode": ("statistics", "mode"),
    "variance": ("statistics", "variance"),
    "standard deviation": ("statistics", "std"),
    "std": ("statistics", "std"),
    "probability": ("statistics", "probability"),
    "combination": ("statistics", "combination"),
    "permutation": ("statistics", "permutation"),
    "ncr": ("statistics", "combination"),
    "npr": ("statistics", "permutation"),
}

STEP_HINT_PATTERN = re.compile(r"(step|explain|how to|show work|show steps)", re.IGNORECASE)


def _detect_step_mode(text: str) -> bool:
    return STEP_HINT_PATTERN.search(text) is not None


def _guess_topic_from_ops(ops: list) -> str:
    """Pick the first topic implied by operations; fallback algebra."""
    for op in ops:
        topic = OP_KEYWORDS.get(op, (None, None))[0]
        if topic:
            return topic
    return "algebra"


def _detect_operations(text: str) -> list:
    """
    Return operations (in order) mentioned in the text.
    We check multi-word keys first by sorting by length descending.
    """
    ops = []
    for key in sorted(OP_KEYWORDS.keys(), key=len, reverse=True):
        if re.search(rf"\b{re.escape(key)}\b", text, flags=re.IGNORECASE):
            ops.append(key)
    # Preserve the textual order (stable by scanning)
    ordered = []
    cursor = text.lower()
    for key in sorted(set(ops), key=lambda k: cursor.find(k)):
        ordered.append(key)
    return ordered


def parse_user_input(user_input: str) -> dict:

    step_by_step = _detect_step_mode(user_input)
    raw_steps = split_multi_steps(user_input)

    # If multi-step, build a pipeline
    if len(raw_steps) > 1:
        pipeline = []
        # Use the last step to extract the base expression if earlier steps omit it
        # Strategy: the first segment that contains numbers/variables becomes the base expression
        base_expr = None
        for seg in raw_steps:
            norm = normalize_math_text(seg)
            if not base_expr and re.search(r"[a-zA-Z0-9]", norm):
                base_expr = norm
        base_expr = base_expr or normalize_math_text(user_input)

        # Build pipeline with operations inferred per step; if a step has no explicit expr, reuse base_expr
        for seg in raw_steps:
            norm = normalize_math_text(seg)
            ops = _detect_operations(seg)
            op = ops[0] if ops else None
            subject = _guess_topic_from_ops(ops)
            expr = norm
            # If the normalized segment is mostly operation words, attach base expression
            if len(norm) <= 20 and op is not None:
                expr = base_expr
            pipeline.append({
                "subject": subject,
                "operation": OP_KEYWORDS.get(op, (None, None))[1] if op else None,
                "expression": expr
            })

        variables = detect_variables(base_expr)
        return {"pipeline": pipeline, "variables": variables, "step_by_step": step_by_step}

    # Single-step path
    normalized = normalize_math_text(user_input)
    ops = _detect_operations(user_input)
    subject = _guess_topic_from_ops(ops)
    operation = OP_KEYWORDS.get(ops[0], (None, None))[1] if ops else None
    variables = detect_variables(normalized)

    # Try to keep only the right-hand side after keywords like 'of', 'for', '='
    m = re.search(r"(?:of|for|=)\s*(.*)", normalized, flags=re.IGNORECASE)
    expression = m.group(1) if m else normalized

    return {
        "subject": subject,
        "operation": operation,
        "expression": expression.strip(),
        "variables": variables,
        "step_by_step": step_by_step
    }
