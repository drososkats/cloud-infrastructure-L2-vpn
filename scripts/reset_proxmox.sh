#!/bin/bash
# ==========================================================
# Node 1: Proxmox Hypervisor Network Initialization Script
# Description: Connects the Hypervisor to the L2 Bridge and
#              obtains an IP address via DHCP through the tunnel.
# ==========================================================

echo "--- [1/5] Cleaning up old network configurations ---"
# Terminating any active dhclient instances and flushing interfaces
killall dhclient 2>/dev/null
ip addr flush dev br0 2>/dev/null
ip link set br0 down 2>/dev/null
brctl delbr br0 2>/dev/null
ip addr flush dev tap0 2>/dev/null

echo "--- [2/5] Restarting OpenVPN Client (proxmox_vpn) ---"
# Triggering the proxmox_vpn.conf configuration
systemctl restart openvpn-client@proxmox_vpn

echo "Waiting for tap0 interface to initialize (15s)..."
sleep 15

echo "--- [3/5] Setting up Bridge and Linking VPN ---"
# Creating the bridge and attaching the virtual TAP interface
brctl addbr br0
brctl addif br0 tap0
ip link set tap0 up
ip link set br0 up

echo "--- [4/5] Requesting IP from Node 2 (Laptop) via DHCP ---"
# This demonstrates the L2 transparency - DHCP requests pass through the tunnel
dhclient -v br0

echo "--- [5/5] Connectivity Verification ---"
ip addr show br0 | grep "inet "
echo "Testing connectivity to Laptop (Node 2)..."
ping -c 3 10.8.0.1