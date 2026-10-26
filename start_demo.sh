#!/usr/bin/env bash

# ==============================================================================
# EduCred: Capstone Project Live Demonstration & Viva Showcase Launcher
# NMIMS MPSTME Shirpur Campus • Design Experience II (Vertical: Industry Innovation)
# Team: Himanshu Garg (E250), Manthan Patil (E323), Vaishnavi Mali (B348)
# Mentor: Dr. Srikanth Pullipeti
# ==============================================================================

echo "======================================================================"
echo "  🎓 EduCred: Decentralized Academic Credential Verification System"
echo "  🏛️  SVKM's NMIMS MPSTME Shirpur Campus • Design Experience II"
echo "======================================================================"
echo "  Team: Himanshu Garg (E250) | Manthan Patil (E323) | Vaishnavi Mali (B348)"
echo "  Mentor: Dr. Srikanth Pullipeti, Associate Professor, MPSTME"
echo "======================================================================"
echo ""
echo "  🚀 Starting EduCred React + Vite Web3 Dashboard..."
echo "  🔗 Open URL in browser: http://localhost:5173"
echo "  ⚡ Evaluator Simulation Mode: Active (Zero MetaMask setup required)"
echo "  Press Ctrl + C anytime to stop the server."
echo "======================================================================"
echo ""

cd "$(dirname "$0")/client" || exit 1
npm run dev
