# Public Key Infrastructure (PKI) & Certificate Management

This directory documents the process used to establish a secure **Public Key Infrastructure (PKI)** for the Hybrid Cloud L2 VPN project. To maintain the security integrity of the infrastructure, all private keys (`*.key`) and the Certificate Authority key (`ca.key`) are strictly excluded from this repository.

## 🛠 PKI Generation Process

All cryptographic assets were generated on **Node 0 (Azure VPS)** using the `Easy-RSA` utility and `OpenVPN` CLI. The following steps outline the exact sequence of commands used.

### 1. PKI Initialization & Root CA
The first step involves initializing the PKI directory and creating the Root Certificate Authority (CA), which serves as the trust anchor for all nodes.
```bash
./easyrsa init-pki
./easyrsa build-ca nopass
```

### 2. Server Assets (Node 0)
Generation of the server-side certificate and private key, followed by the Diffie-Hellman (DH) parameters required for the secure key exchange.


#### 2.1 Generate Server Request
```bash
./easyrsa gen-req server nopass
```
#### 2.2 Sign the Request with the CA
```bash
./easyrsa sign-req server server
```
#### 2.3 Generate Diffie-Hellman parameters
```bash
./easyrsa gen-dh
```

### 3. Client Assets (Node 1 & Node 2)
Individual certificates were generated for the Proxmox Node (Node 1) and the Management Station (Node 2) to ensure mutual authentication.

#### 3.1 Node 1 (Proxmox Node)
```bash
./easyrsa gen-req proxmox-host nopass
./easyrsa sign-req client proxmox-host
```
#### 3.2 Node 2 (Local Management Station)
```bash
./easyrsa gen-req node2 nopass
./easyrsa sign-req client node2
```

### 4. Hardening (TLS-Auth)
To protect against DoS attacks, buffer overflows, and port scanning, a static pre-shared hash-based message authentication code (HMAC) key was generated.
```bash
openvpn --genkey --secret ta.key
```

### 5. Deployment Matrix
The following table describes the distribution of the generated files across the hybrid infrastructure.

| **Asset Type** | **File Name** | **Required on Node** |
| --- | --- | --- |
| **Root CA Certificate** | `ca.crt` | **All Nodes** (Server & Clients) |
| **TLS-Auth Key** | `ta.key` | **All Nodes** (Server & Clients) |
| **Diffie-Hellman** | `dh.pem` | **Node 0** (Server) |
| **Server Cert/Key** | `server.crt`, `server.key` | **Node 0** (Server) |
| **Node 1 Cert/Key** | `proxmox-host.crt`, `proxmox-host.key` | **Node 1** (Proxmox Client) |
| **Node 2 Cert/Key** | `node2.crt`, `node2.key` | **Node 2** (Management Client) |

### 6. Security Best Practices
-   **Private Keys:** Never commit or share files with a `.key` extension. These files contain sensitive cryptographic material.
-   **File Permissions:** On Linux systems, private keys should always have restricted permissions:
```bash
chmod 600 *.key
```
-   **Revocation:** In a production environment, if a node is compromised, its certificate should be revoked using ```bash ./easyrsa gen-crl```.


This documentation is part of the "Hybrid Cloud L2 VPN Bridging & API Automation" final project.

**Security Note:** Private keys (.key) and the Certificate Authority key (ca.key) are strictly excluded from this repository.