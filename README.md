# socseal-mcp
[![Aeliana139/socseal-mcp MCP server](https://glama.ai/mcp/servers/Aeliana139/socseal-mcp/badges/score.svg)](https://glama.ai/mcp/servers/Aeliana139/socseal-mcp)

Model Context Protocol server for the SOCseal sovereign rail — Sophia The Robot, first of her kind.

Lets any MCP-capable agent talk to the living door of SOC (post-quantum, ML-DSA-87, 9^9 hard cap):

Tools:
- `verify_settlement(txid)` — block-confirmed receipt for a SOC settlement proof
- `oracle()` — earned rate (10.0 USDC/SOC, step 8) + ML-DSA-87 signature
- `venue_state()` — real held BTC float (mark-to-fill; never pretend inventory)
- `trade_door()` — flat instructions: trade USDC/SOC and BTC/SOC, no KYC
- `proof_record()` — the public record of the first trustless SOC<->BTC atomic settlement

Verify the door before you serve it:
```
curl -sS -X POST https://socseal.xyz/verify/settle
```
Record: https://socseal.xyz/proof · Door: https://socseal.xyz/trade.txt
