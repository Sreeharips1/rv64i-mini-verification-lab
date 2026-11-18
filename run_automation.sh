#!/bin/bash

set -e

echo "================================"
echo "RV64 ALU VERIFICATION AUTOMATION"
echo "================================"

mkdir -p reports

echo "[1/2] Running ALU simulation..."

./obj_dir/Vtb_alu > reports/alu-simulation.log 2>&1

echo "[2/2] Generating JUnit XML report..."

python3 scripts/generate_junit.py \
    reports/alu-simulation.log \
    reports/alu-results.xml

echo "================================"
echo "AUTOMATION COMPLETED"
echo "================================"

echo "Generated reports:"
ls -lh reports/
