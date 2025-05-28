import json
import re
import math
from datetime import datetime, timedelta


APL = "+ Add Playground"

def get_playground_types():
    return [
        "Math Evaluator",
        "Boolean Logic",
        "Code Evaluation",
        "Text Manipulation",
        "Regex Tester",
        "Date/Time",
        "Currency Conversion",
        "Unit Converter",
        "Code Linter",
        "Data Format Converter",
        "Code Formatter (Python)",
        "Expression Simplifier",
        "String Rewriter",
        "JSON Explorer",
    ]


def run_playground(playground_type, input_text):
    try:
        if playground_type == "Math Evaluator":
            # Evaluate math expressions safely using math module namespace
            return str(eval(input_text, {"__builtins__": {}}, math.__dict__))

        elif playground_type == "Boolean Logic":
            # Simple boolean eval - allow only True/False and operators
            allowed_names = {"True": True, "False": False}
            return str(eval(input_text, {"__builtins__": None}, allowed_names))

        elif playground_type == "Code Evaluation":
            # Execute Python code and capture output (very basic)
            # Warning: Insecure, for demo only
            local_vars = {}
            exec(input_text, {"__builtins__": {}}, local_vars)
            return str(local_vars)

        elif playground_type == "Text Manipulation":
            # Support simple commands: reverse:, upper:, lower:
            if input_text.startswith("reverse:"):
                return input_text[len("reverse:"):].strip()[::-1]
            elif input_text.startswith("upper:"):
                return input_text[len("upper:"):].strip().upper()
            elif input_text.startswith("lower:"):
                return input_text[len("lower:"):].strip().lower()
            else:
                return "Commands supported: reverse:, upper:, lower:"

        elif playground_type == "Regex Tester":
            # Expected input format: text || regex pattern
            if "||" not in input_text:
                return "Format: text || regex_pattern"
            text, pattern = map(str.strip, input_text.split("||", 1))
            matches = list(re.finditer(pattern, text))
            if not matches:
                return "No matches found."
            return "\n".join(f"Match at {m.start()}-{m.end()}: {m.group()}" for m in matches)

        elif playground_type == "Date/Time":
            # Simple date/time parser (support 'now', 'YYYY-MM-DD', 'X days ago')
            if input_text.lower() == "now":
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif "days ago" in input_text.lower():
                try:
                    days = int(input_text.lower().split("days ago")[0].strip())
                    dt = datetime.now() - timedelta(days=days)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    return "Format example: '3 days ago'"
            else:
                try:
                    dt = datetime.strptime(input_text.strip(), "%Y-%m-%d")
                    return dt.strftime("%A, %B %d, %Y")
                except:
                    return "Formats supported: 'now', 'YYYY-MM-DD', 'X days ago'"

        elif playground_type == "Currency Conversion":
            # Stub example: just echo input with a fake rate
            return f"Converted result for '{input_text}' (demo only)"

        elif playground_type == "Unit Converter":
            # Basic unit conversions for demo
            try:
                value, unit_from, _, unit_to = input_text.lower().split()
                value = float(value)
                conversions = {
                    ("cm", "m"): lambda x: x / 100,
                    ("m", "cm"): lambda x: x * 100,
                    ("kg", "g"): lambda x: x * 1000,
                    ("g", "kg"): lambda x: x / 1000,
                    ("c", "f"): lambda x: (x * 9/5) + 32,
                    ("f", "c"): lambda x: (x - 32) * 5/9,
                    ("km", "m"): lambda x: x * 1000,
                    ("m", "km"): lambda x: x / 1000,
                }
                conv = conversions.get((unit_from, unit_to))
                if conv:
                    return f"{value} {unit_from} = {conv(value)} {unit_to}"
                else:
                    return f"No converter for '{unit_from} to {unit_to}'"
            except:
                return "Format: '100 cm to m'"

        elif playground_type == "Code Linter":
            # Very basic syntax check using compile()
            try:
                compile(input_text, '<string>', 'exec')
                return "No syntax errors detected."
            except SyntaxError as e:
                return f"Syntax error: {e}"

        elif playground_type == "Data Format Converter":
            # Simple JSON <-> YAML (if PyYAML installed) converter stub
            if "to yaml" in input_text.lower():
                try:
                    import yaml
                    json_data = json.loads(input_text.lower().replace("to yaml", "").strip())
                    return yaml.dump(json_data)
                except Exception as e:
                    return f"Error converting to YAML: {e}"
            elif "to json" in input_text.lower():
                try:
                    import yaml
                    yaml_data = yaml.safe_load(input_text.lower().replace("to json", "").strip())
                    return json.dumps(yaml_data, indent=2)
                except Exception as e:
                    return f"Error converting to JSON: {e}"
            else:
                return "Add 'to yaml' or 'to json' to your input for conversion."

        elif playground_type == "Code Formatter (Python)":
            import ast
            tree = ast.parse(input_text)
            return ast.unparse(tree)

        elif playground_type == "Expression Simplifier":
            from sympy import sympify, simplify
            expr = sympify(input_text)
            return str(simplify(expr))

        elif playground_type == "String Rewriter":
            return f"""Upper: {input_text.upper()}
Lower: {input_text.lower()}
Title: {input_text.title()}
Reversed: {input_text[::-1]}
Words: {len(input_text.split())}
Characters: {len(input_text)}
"""

        elif playground_type == "JSON Explorer":
            parsed = json.loads(input_text)
            return json.dumps(parsed, indent=4)

        elif playground_type == APL:
            return (
                "You selected '+ Add playground'.\n"
                "This feature lets you add custom playgrounds.\n"
                "Currently, this is a placeholder. Please implement your playground logic."
            )

        else:
            return "Playground type not recognized."

    except Exception as e:
        return f"[Error] {str(e)}"
