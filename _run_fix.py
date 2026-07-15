import base64, sys
with open(r"C:\Users\Administrator\Documents\Poolians\_fix_script.b64", "r") as f:
    code = base64.b64decode(f.read()).decode()
exec(code)
