#!/bin/bash
# ==========================================================
# Node 2: Hybrid Cloud Integration & DHCP Gateway Script
# Description: Automates Bridge creation, VPN handshake, 
#              and DHCP service initialization for L2 segment.
# ==========================================================

echo "--- [1/5] Ensuring Local Network Persistence ---"
# Maintaining the primary interface (enp0s3) connectivity
sudo ip link set enp0s3 up
sudo ip addr add 192.168.1.5/24 dev enp0s3 2>/dev/null
sudo ip route add default via 192.168.1.1 dev enp0s3 2>/dev/null

echo "--- [2/5] Cleaning Existing VPN/Bridge State ---"
sudo systemctl stop isc-dhcp-server 2>/dev/null
sudo ip addr flush dev br0 2>/dev/null
sudo ip link set br0 down 2>/dev/null
sudo brctl delbr br0 2>/dev/null

echo "--- [3/5] Initializing OpenVPN Tunnel ---"
sudo systemctl restart openvpn-client@client
echo "Waiting 15s for VPN handshake and TAP creation..."
sleep 15

# Verify TAP interface existence
if ! ip link show tap0 > /dev/null 2>&1; then
    echo "CRITICAL ERROR: VPN failed to create tap0 interface!"
    exit 1
fi

echo "--- [4/5] Establishing Layer 2 Bridge (br0) ---"
sudo brctl addbr br0
sudo brctl addif br0 tap0
sudo ip addr add 10.8.0.1/24 dev br0
sudo ip link set tap0 up
sudo ip link set br0 up

echo "--- [5/5] Launching DHCP Service & Connectivity Trace ---"
sudo systemctl restart isc-dhcp-server
ping -c 2 8.8.8.8 > /dev/null && echo "External Internet: OK" || echo "External Internet: FAILED"

echo "----------------------------------------------------"
brctl show br0
echo "Done! Node 2 is ready."