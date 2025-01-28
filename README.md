# KubeSage  

![KubeSage](https://img.shields.io/badge/Kubernetes-Troubleshooting-blue.svg)  
![License](https://img.shields.io/badge/license-MIT-green.svg)  
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)  

KubeSage is an AI-powered troubleshooting and compliance auditing tool for Kubernetes environments. It helps DevOps and SRE teams detect misconfigurations, performance bottlenecks, and security risks while providing guided remediations.  

---

## 🚀 Features  

- **AI-Powered Troubleshooting**: Uses LLMs to analyze Kubernetes logs and configurations.  
- **Compliance Auditing**: Maps security controls to frameworks like FedRAMP, ISO, and SOC2.  
- **Cluster Risk Analysis**: Scans Kubernetes clusters and workloads for vulnerabilities.  
- **Intelligent Remediation**: Provides fix suggestions based on historical data and best practices.  
- **Interactive Chatbot**: Ask troubleshooting queries via a CLI or web UI.  

---

## 🏗 Installation  

### Prerequisites  

- Kubernetes cluster (Minikube, AKS, EKS, GKE, etc.)  
- Helm  
- Docker  
- Python 3.8+  
- OpenAI API Key (Optional, for AI-powered insights)  

### Steps  

1. Clone the repository:  

   ```sh
   git clone https://github.com/yourusername/kubesage.git
   cd kubesage
   ```

2. Deploy using Helm:  

   ```sh
   helm install kubesage ./deploy/helm
   ```

3. Start the interactive troubleshooting chatbot:  

   ```sh
   python cli.py
   ```

---

## 📖 Usage  

- **Check cluster health:**  
  ```sh
  python cli.py --check-health
  ```  

- **Analyze logs for failures:**  
  ```sh
  python cli.py --analyze-logs --namespace=default
  ```

- **List compliance violations:**  
  ```sh
  python cli.py --compliance-check
  ```

---

## 🛠️ Configuration  

Modify `config.yaml` to customize scanning rules and compliance frameworks.  

```yaml
scan_interval: 5m
enable_ai_suggestions: true
compliance_frameworks:
  - FedRAMP
  - ISO27001
  - SOC2
```

---

## 🛡️ Security  

- Uses Role-Based Access Control (RBAC) to manage permissions.  
- Does not modify Kubernetes resources unless explicitly allowed.  

---

## 📜 License  

This project is licensed under the **MIT License**, a permissive open-source license that allows anyone to use, modify, and distribute the software with minimal restrictions.  

### Why MIT License?  

- **Freedom to Use**: Anyone can use, modify, and distribute the software.  
- **Permissive & Business-Friendly**: Allows commercial and private use without restrictions.  
- **Minimal Liability**: Protects contributors from legal claims.  
- **Broad Adoption**: The most widely used open-source license, making it easier for others to contribute.  

Full MIT License text:  

```text
MIT License  

Copyright (c) 2025 Your Name  

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
```

---

## 🤝 Contributing  

Contributions are welcome! Open an issue or submit a pull request to improve KubeSage.  

---

## 📧 Contact  

For questions, reach out to **adeeshdevanand@gmail.com** or visit the GitHub repository.  
