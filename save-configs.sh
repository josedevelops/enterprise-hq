#!/bin/bash
# Exports running config from each SR Linux node to configs/ directory
# Run this after every commit now on any node

NODES=("mdf-sw-01" "idf-sw-01" "idf-sw-02" "mdf-core-01" "edge-router-01")
IPS=("172.20.20.11" "172.20.20.12" "172.20.20.13" "172.20.20.10" "172.20.20.14")

for i in "${!NODES[@]}"; do
    NODE="${NODES[$i]}"
    IP="${IPS[$i]}"
    echo "Saving $NODE..."
    docker exec clab-enterprise-hq-$NODE \
        sr_cli -d "info" | \
        docker exec -i clab-enterprise-hq-$NODE \
        cat /etc/opt/srlinux/config.json \
        > ~/labs/enterprise-hq/configs/$NODE/config.json 2>/dev/null
    
    # simpler direct copy from container
    docker cp clab-enterprise-hq-$NODE:/etc/opt/srlinux/config.json \
        ~/labs/enterprise-hq/configs/$NODE/config.json
    
    if [ $? -eq 0 ]; then
        echo "  ✅ $NODE saved"
    else
        echo "  ❌ $NODE failed"
    fi
done
echo "Done."
