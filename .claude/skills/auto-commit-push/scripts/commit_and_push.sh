#!/bin/bash
# Auto-commit and push helper script
# This script is a reference - Claude typically uses Bash tool directly

set -e  # Exit on error

echo "🔍 Checking for changes..."

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes to commit"
    exit 0
fi

echo ""
echo "📊 Current status:"
git status --short

echo ""
echo "📝 Recent commits (for style reference):"
git log --oneline -3

echo ""
echo "🔄 Changes to be committed:"
git diff --stat
git diff --cached --stat

echo ""
echo "⚠️  This script is a reference. Claude will:"
echo "   1. Analyze the changes shown above"
echo "   2. Create an appropriate commit message"
echo "   3. Stage relevant files"
echo "   4. Commit with the generated message"
echo "   5. Push to remote"
echo ""
echo "   Use 'Skill: auto-commit-push' to invoke via Claude"
