#!/usr/bin/env bash
curl -v \
    -H "Content-Type: application/json" \
    -d '{"ref":"refs/heads/main"}' \
    http://0.0.0.0:11444/webhook
