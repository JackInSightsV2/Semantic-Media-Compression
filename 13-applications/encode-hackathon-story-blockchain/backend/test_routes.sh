#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api"

echo "=== Testing Backend API Routes ==="
echo ""

echo "1. Health Check:"
curl -s "$BASE_URL/../healthz" | jq .
echo ""
echo ""

echo "2. Registration - Upload Asset:"
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/registration/uploads" \
  -F "title=Test Story" \
  -F "asset_type=text" \
  -F "text=Once upon a time in a hackathon.")
echo "$UPLOAD_RESPONSE" | jq .
ASSET_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.asset_id')
echo ""
echo "Asset ID: $ASSET_ID"
echo ""

echo "3. Registration - Get Asset Details:"
curl -s "$BASE_URL/registration/$ASSET_ID" | jq .
echo ""
echo ""

echo "4. Registration - Register Story:"
STORY_RESPONSE=$(curl -s -X POST "$BASE_URL/registration/register-story" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"metadata\": {\"chain\": \"testnet\"}}")
echo "$STORY_RESPONSE" | jq .
echo ""
echo ""

echo "5. Scans - Create Scan:"
SCAN_RESPONSE=$(curl -s -X POST "$BASE_URL/scans" \
  -F "source_type=upload" \
  -F "source_reference=test-scan-1" \
  -F "text=Once upon a time in a hackathon with creative stories.")
echo "$SCAN_RESPONSE" | jq .
SCAN_ID=$(echo "$SCAN_RESPONSE" | jq -r '.scan_id')
echo ""
echo "Scan ID: $SCAN_ID"
echo ""

echo "6. Scans - Get Scan Details:"
sleep 2  # Wait for processing
curl -s "$BASE_URL/scans/$SCAN_ID" | jq .
echo ""
echo ""

echo "7. Scans - List Recent Scans:"
curl -s "$BASE_URL/scans/recent?limit=5" | jq .
echo ""
echo ""

echo "8. Disputes - Get Options:"
curl -s "$BASE_URL/disputes/options" | jq .
echo ""
echo ""

echo "9. Disputes - Create Dispute:"
DISPUTE_RESPONSE=$(curl -s -X POST "$BASE_URL/disputes" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"suspect_reference\": \"$SCAN_ID\", \"notes\": \"Potential infringement detected.\"}")
echo "$DISPUTE_RESPONSE" | jq .
DISPUTE_ID=$(echo "$DISPUTE_RESPONSE" | jq -r '.dispute.id')
echo ""
echo "Dispute ID: $DISPUTE_ID"
echo ""

echo "10. Disputes - Get Dispute Details:"
curl -s "$BASE_URL/disputes/$DISPUTE_ID" | jq .
echo ""
echo ""

echo "11. Disputes - Get Active Disputes:"
curl -s "$BASE_URL/disputes/active" | jq .
echo ""
echo ""

echo "12. Dashboard - Summary:"
curl -s "$BASE_URL/dashboard/summary" | jq .
echo ""
echo ""

echo "13. Dashboard - Activity:"
curl -s "$BASE_URL/dashboard/activity?range=7d" | jq .
echo ""
echo ""

echo "14. Dashboard - Notifications:"
curl -s "$BASE_URL/dashboard/notifications" | jq .
echo ""
echo ""

echo "15. Dashboard - Insights:"
curl -s "$BASE_URL/dashboard/insights" | jq .
echo ""
echo ""

echo "=== All Tests Complete ==="

