#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
error() { echo -e "${RED}✗${NC} $*"; exit 1; }

echo ""
echo "🔥 fireworks-ai-tools-memory Codex setup"
echo "────────────────────────────────────────"
echo ""

command -v python3 >/dev/null 2>&1 || error "Python 3 is required but not found."

CODEX_HOME_DIR="${CODEX_HOME:-}"
if [[ -z "$CODEX_HOME_DIR" ]]; then
  error "CODEX_HOME is not set. Start from a Codex environment or export CODEX_HOME first."
fi

MEMORY_HOME="$CODEX_HOME_DIR/memories/fireworks-ai-tools-memory"
TOOLS_DIR="$MEMORY_HOME/tools"
GLOBAL_DIR="$MEMORY_HOME/global"

mkdir -p "$TOOLS_DIR" "$GLOBAL_DIR"
info "Created tool memory directories under $MEMORY_HOME"

GLOBAL_KNOWLEDGE="$GLOBAL_DIR/KNOWLEDGE.md"
if [[ ! -f "$GLOBAL_KNOWLEDGE" ]]; then
  cat > "$GLOBAL_KNOWLEDGE" <<'EOF'
# Global Tool Principles

> **Scope**: Cross-tool operational principles.
> Auto-maintained by fireworks-ai-tools-memory.

## Principles

- [placeholder] No global tool principles recorded yet.
EOF
  info "Bootstrapped global knowledge file"
else
  warn "Global knowledge file already exists — leaving it untouched"
fi

echo ""
echo "Next commands:"
echo "  python3 cli/tools_memory.py inject --tool <tool-key>"
echo "  python3 cli/tools_memory.py checkpoint --tool <tool-key> --note \"...\""
echo "  python3 cli/tools_memory.py flush --tool <tool-key> --summary-file ./session-summary.md"
echo "  python3 cli/tools_memory.py register-script --tool <tool-key> --source ./path/to/script.sh"
echo ""
info "Codex setup complete"
