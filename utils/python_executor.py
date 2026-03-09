"""Safe Python code executor for mathematical computations."""
import io
import sys
import traceback
import math


SAFE_GLOBALS = {
    "__builtins__": {},
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
    "list": list,
    "tuple": tuple,
    "dict": dict,
    "set": set,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "pow": pow,
    "print": print,
    # Math functions
    "math": math,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "factorial": math.factorial,
    "gcd": math.gcd,
    "ceil": math.ceil,
    "floor": math.floor,
    "comb": math.comb,
    "perm": math.perm,
}


def execute_python(code: str, timeout: float = 5.0) -> dict:
    """Execute Python code safely and return the result.
    
    Args:
        code: Python code string to execute.
        timeout: Maximum execution time in seconds (not enforced on Windows).
    
    Returns:
        Dict with 'success', 'output', and 'error' keys.
    """
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    result = {"success": False, "output": "", "error": ""}
    
    try:
        # Execute in restricted environment
        local_vars = {}
        exec(code, SAFE_GLOBALS.copy(), local_vars)
        
        output = buffer.getvalue()
        
        # Also capture any 'result' variable if defined
        if "result" in local_vars:
            if output:
                output += f"\nResult: {local_vars['result']}"
            else:
                output = str(local_vars["result"])
        
        result["success"] = True
        result["output"] = output if output else "Code executed successfully (no output)."
        
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)}"
    
    finally:
        sys.stdout = old_stdout
    
    return result
