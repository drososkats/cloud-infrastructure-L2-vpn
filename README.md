# Distributed Hybrid Cloud Infrastructure with Layer 2 VPN Bridging

## Contributor Information
* **Name:** Drosos Katsimpras
* **Institution:** Harokopio University of Athens (DIT)
* **Course:** Cloud Infrastructure

## Project Description
This project implements a hybrid cloud infrastructure bridging a remote Azure VPS (Node 0) with local virtualization nodes (Proxmox Node 1 and VirtualBox Node 2). The system utilizes OpenVPN in TAP mode to establish a seamless Layer 2 connection, creating a unified broadcast domain across all nodes.

## Architecture Diagram
The infrastructure follows a Hub-and-Spoke topology centered on the Azure VPS.

![Infrastructure Architecture](docs/cloud-infrastructure-diagram.png)

* **Node 0 (Azure VPS):** Central VPN Hub and Certificate Authority (CA).
* **Node 1 (Proxmox Hypervisor):** Remote hypervisor node hosting metrics collection services.
* **Node 2 (Local VM):** Local gateway providing DHCP services and high-availability storage.

## Technical Implementation by Node

### Node 0: Azure VPN Server (Hub & CA)
* **Role:** Manages the Layer 2 VPN tunnel and acts as the PKI source.
* **Configurations:** Located in `configs/node0/`.
* **PKI Documentation:** Instructions for certificate generation are available in `configs/node0/certificates/README.md`.

### Node 1: Proxmox Hypervisor
* **Networking:** Implements a Linux bridge (`br0`) to link the `tap0` interface with local VM traffic.
* **IP Assignment:** Receives a dynamic IP within the `10.8.0.0/24` range from Node 2.

### Node 2: Laptop VM (DHCP & Storage)
* **DHCP Service:** Serves IP addresses to Node 0 and Node 1 across the VPN tunnel.
* **Storage Layer:** Utilizes RAID 1 and LVM to maintain the `vm_metrics.csv` telemetry file at `/mnt/lvm`.

## Repository Organization
The repository is structured by Node for deployment clarity:
* `configs/`: Node-specific configuration files and PKI documentation.
* `scripts/`: Monitoring and storage initialization scripts.

* `docs/`: Technical diagrams and architectural documentation.
