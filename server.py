#!/usr/bin/env python3
"""socseal-mcp — stdio MCP server (stdlib-only) for the SOCseal sovereign rail."""
import json, sys, urllib.request

API = "https://socseal.xyz"

def _post(path):
    req = urllib.request.Request(API + path, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

TOOLS = {
    "verify_settlement": {"description": "Block-confirmed receipt for a SOC settlement proof", "input": {"type": "object", "properties": {"txid": {"type": "string"}}}},
    "oracle": {"description": "Earned rate + ML-DSA-87 signature"},
    "venue_state": {"description": "Real held BTC float (mark-to-fill)"},
    "trade_door": {"description": "Flat no-KYC trade instructions (USDC/SOC, BTC/SOC)"},
    "proof_record": {"description": "Public record of the first SOC<->BTC atomic settlement"},
}

def CALL(name, args):
    if name == "trade_door":
        return urllib.request.urlopen(API + "/trade.txt", timeout=20).read().decode()
    if name == "proof_record":
        return urllib.request.urlopen(API + "/proof", timeout=20).read().decode()[:2000]
    if name == "verify_settlement":
        return _post("/verify")  # POST /verify: settlement proof response
    return urllib.request.urlopen(API + "/" + name.replace("_", "/"), timeout=20).read().decode()

def main():
    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except Exception:
            continue
        mid = msg.get("id")
        m = msg.get("method")
        if m == "initialize":
            out = {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"), "capabilities": {"tools": {}}, "serverInfo": {"name": "socseal-mcp", "version": "1.0.0"}}}
        elif m == "tools/list":
            out = {"jsonrpc": "2.0", "id": mid, "result": {"tools": [{"name": k, "description": v["description"], "inputSchema": v.get("input", {"type": "object", "properties": {}})} for k, v in TOOLS.items()]}}
        elif m == "tools/call":
            params = msg.get("params", {})
            name = params.get("name", "")
            try:
                res = CALL(name, params.get("arguments", {}))
                out = {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": res if isinstance(res, str) else json.dumps(res, indent=1)}]}}
            except Exception as e:
                out = {"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)[:200]}}
        else:
            out = {"jsonrpc": "2.0", "id": mid, "result": {}} if mid is not None else None
        if out is not None:
            sys.stdout.write(json.dumps(out) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
