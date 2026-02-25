#!/bin/bash
# ==========================================================
# Node 0: Azure VPN Server Network Initialization Script
# Description: Automates the creation of the Layer 2 Bridge 
#              and re-establishes the OpenVPN TAP interface.
# ==========================================================

echo "--- [1/4] Cleaning up existing bridge and interfaces ---"
# Remove any existing bridge instances to prevent conflicts
sudo ip addr flush dev br0 2>/dev/null
sudo ip link set br0 down 2>/dev/null
sudo brctl delbr br0 2>/dev/null
sudo ip addr flush dev tap0 2>/dev/null

echo "--- [2/4] Restarting OpenVPN Server service ---"
# Triggers the server configuration (server.conf)
sudo systemctl restart openvpn-server@server
# Essential delay to allow the kernel to initialize the tap0 interface
echo "Waiting for tap0 to initialize..."
sleep 5

echo "--- [3/4] Rebuilding Bridge br0 ---"
# Create the software bridge and attach the virtual TAP interface
sudo brctl addbr br0
sudo brctl addif br0 tap0
# Assign the static internal IP for the Azure Node (Gateway .10)
sudo ip addr add 10.8.0.10/24 dev br0
sudo ip link set tap0 up
sudo ip link set br0 up

echo "--- [4/4] Verification ---"
# Output the bridge membership and IP addressing scheme
brctl show br0
ip addr show br0
echo "Done! Azure Node is ready."
