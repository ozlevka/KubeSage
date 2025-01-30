# KubeSage: AI-Powered Kubernetes Troubleshooting Assistant

![KubeSage](https://your-logo-url-here.com) *(Replace with actual project logo if available)*

 **KubeSage** is an **AI-driven Kubernetes troubleshooting assistant** that integrates **LangChain Agents** with Kubernetes APIs. It provides **real-time diagnostics, resource monitoring, and troubleshooting recommendations** for Kubernetes clusters using OpenAI's **GPT-4o**.

---

##  Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Available Tools](#-available-tools)
- [Architecture](#️-architecture)
- [WebSocket Integration](#-websocket-integration)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## Features
✅ AI-powered **Kubernetes troubleshooting**  
✅ **LangChain Agents** for intelligent decision-making  
✅ Real-time **Kubernetes monitoring** (Pods, Deployments, Services, Nodes)  
✅ **Deep dive diagnostics** (logs, resource usage, RBAC, etc.)  
✅ **WebSocket interface** for interactive debugging  
✅ **Secure** authentication using OpenAI API keys  

---

## Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/KubeSage.git
cd KubeSage
```

### 2️⃣ Set Up Virtual Environment
```bash
conda create -n kube-sage python=3.9 -y
conda activate kube-sage
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Kubernetes Access
Ensure your Kubernetes cluster is accessible:
- **Inside Cluster:** Automatically loads service account credentials.  
- **Outside Cluster:** Set up `KUBECONFIG`:
  ```bash
  export KUBECONFIG=$HOME/.kube/config
  ```

### 5️⃣ Run the WebSocket API
```bash
python src/main.py
```

---

## Usage
### Start WebSocket Connection
Use **`wscat`** or a WebSocket client:
```bash
wscat -c ws://localhost:6000/ws
```
You can then start **chatting with the AI assistant**.

---

## Available Tools
### Broad Insights (Cluster Overview)
| Tool | Description |
|------|------------|
| `Get All Pods with Resource Usage` | Lists all pods with CPU & memory usage. |
| `Get All Services` | Lists all services and their types/ports. |
| `Get All Deployments` | Fetches deployment details. |
| `Get All Nodes` | Lists nodes with health & capacity. |
| `Get Cluster Events` | Shows recent warnings & failures. |
| `Get Namespace List` | Fetches all Kubernetes namespaces. |

### Deep Dive (Detailed Diagnostics)
| Tool | Description |
|------|------------|
| `Describe Pod with Restart Count` | Fetches pod details + restart count. |
| `Get Pod Logs` | Retrieves last 10 log lines for a pod. |
| `Describe Service` | Gets details of a Kubernetes service. |
| `Describe Deployment` | Fetches deployment details (replica count, images). |
| `Check RBAC Events & Role Bindings` | Analyzes security permissions. |
| `Get Ingress Resources` | Lists ingress rules, hosts & annotations. |
| `Check Pod Affinity & Anti-Affinity` | Analyzes scheduling constraints. |

---

## Architecture
![Architecture Diagram](https://your-diagram-url-here.com) *(Replace with actual architecture diagram if available)*

### Components
1️⃣ **FastAPI WebSocket Server** - Handles real-time interactions.  
2️⃣ **LangChain Agent** - Uses OpenAI GPT-4o to select appropriate tools.  
3️⃣ **Kubernetes API Client** - Fetches cluster insights and diagnostics.  
4️⃣ **RBAC & Authentication** - Secure access to cluster resources.  

---

## WebSocket Integration
KubeSage uses **WebSockets** for real-time AI troubleshooting.

### Connecting to the WebSocket
Example connection using **Python WebSockets**:
```python
import websockets
import asyncio

async def connect():
    uri = "ws://localhost:6000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Describe Pod with Restart Count")
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(connect())
```

---

## Troubleshooting
### 1️⃣ WebSocket Error: `Connection Refused`
✅ Ensure **WebSocket server is running**:
```bash
python src/main.py
```

### 2️⃣ Kubernetes API `403 Forbidden`
✅ Verify **RBAC permissions**:
```bash
kubectl auth can-i get pods --as=system:serviceaccount:default:kubesage-sa
```
If denied, apply:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: metrics-reader-binding
subjects:
  - kind: ServiceAccount
    name: kubesage-sa
    namespace: default
roleRef:
  kind: ClusterRole
  name: metrics-reader
  apiGroup: rbac.authorization.k8s.io
```

### 3️⃣ Metrics API `404 Not Found`
✅ **Enable Metrics Server:**
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

---

## License
**MIT License** - Free to use, modify, and distribute.  
**Contributions welcome!**

---

## Next Steps
**To-Do List**
- [ ] Add Prometheus/Grafana integration for advanced monitoring  
- [ ] Support multi-cluster troubleshooting  
- [ ] Add more AI-powered insights  

**Want to contribute?** Open a PR! 

---

## Acknowledgments
Thanks to **Kubernetes, FastAPI, LangChain, and OpenAI** for making AI-driven DevOps possible!

