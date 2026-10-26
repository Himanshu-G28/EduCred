#!/usr/bin/env bash

# ==============================================================================
# EduCred: GitHub Remote Setup & Push Automation Script
# NMIMS MPSTME Shirpur Campus • Design Experience II
# Team: Himanshu Garg (E250), Manthan Patil (E323), Vaishnavi Mali (B348)
# ==============================================================================

REPO_URL="${1:-https://github.com/Himanshu-G28/EduCred.git}"

echo "======================================================================"
echo "  🚀 EduCred GitHub Push Automation"
echo "  Target Remote: $REPO_URL"
echo "======================================================================"

cd "$(dirname "$0")" || exit 1

# Check if origin already exists
if git remote | grep -q "^origin$"; then
    echo "  Updating existing remote origin..."
    git remote set-url origin "$REPO_URL"
else
    echo "  Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

echo "  Current branch: $(git branch --show-current)"
echo "  Pushing to GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "  ✅ SUCCESS! EduCred is live on GitHub at:"
    echo "  $REPO_URL"
    echo "======================================================================"
else
    echo ""
    echo "======================================================================"
    echo "  ⚠️ Push did not complete."
    echo "  Please verify:"
    echo "  1. You created the empty repository on GitHub."
    echo "  2. You are logged into GitHub in your terminal / browser keychain."
    echo "======================================================================"
fi
