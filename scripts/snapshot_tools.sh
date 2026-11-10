#!/usr/bin/env bash
# The tools the model learns to call, as the real servers list them:
# crag-mcp (retrieval) and filesystem-mcp (bounded file access), both from
# cMCP. Written to data/tools.json; regenerate when a server changes.
#
#   CMCP_DIR=../cMCP CRAG_DB=../askdocs/data/docs.db scripts/snapshot_tools.sh
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CMCP_DIR=${CMCP_DIR:-$ROOT/../cMCP}
CRAG_DB=${CRAG_DB:-$ROOT/../askdocs/data/docs.db}
INSPECT=$CMCP_DIR/tools/cmcp-inspect/cmcp-inspect
FSROOT=$(mktemp -d); trap 'rm -rf "$FSROOT"' EXIT
crag=$("$INSPECT" -j -- "$CMCP_DIR/tools/crag-mcp/crag-mcp" --db "$CRAG_DB" 2>/dev/null)
fs=$("$INSPECT" -j -- "$CMCP_DIR/tools/filesystem-mcp/filesystem-mcp" --root "$FSROOT" 2>/dev/null)
python3 - "$crag" "$fs" > "$ROOT/data/tools.json" <<'PY'
import json, sys
tools = []
for server, listing in zip(("crag-mcp", "filesystem-mcp"), sys.argv[1:]):
    for t in json.loads(listing)["tools"]:
        tools.append({"server": server, "name": t["name"], "description": t.get("description", ""),
                      "inputSchema": t["inputSchema"]})
print(json.dumps({"tools": tools}, indent=1))
PY
python3 -c "import json;d=json.load(open('$ROOT/data/tools.json'));print(len(d['tools']),'tools:',' '.join(t['name'] for t in d['tools']))"
