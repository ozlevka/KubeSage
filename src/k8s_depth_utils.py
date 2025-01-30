import os
from kubernetes import client, config

def load_kube_config():
    """Load Kubernetes configuration (In-Cluster or Local)."""
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

def describe_pod_with_restart_count(namespace: str, pod_name: str):
    """Fetches detailed pod info including restart count."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(pod_name, namespace)

        restart_count = sum(cs.restart_count for cs in (pod.status.container_statuses or []))

        return {
            "status": "success",
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "pod_status": pod.status.phase if pod.status else "Unknown",
            "node": pod.spec.node_name if pod.spec else "Unknown",
            "restart_count": restart_count,
            "containers": [{"name": c.name, "image": c.image} for c in (pod.spec.containers or [])]
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_pod_logs(namespace: str, pod_name: str):
    """Fetches the last 10 log lines from a specific pod."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        logs = v1.read_namespaced_pod_log(pod_name, namespace) or ""
        return {"status": "success", "logs": logs.split("\n")[-10:]}
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def describe_service(namespace: str, service_name: str):
    """Fetches detailed information about a specific service."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        svc = v1.read_namespaced_service(service_name, namespace)

        return {
            "status": "success",
            "name": svc.metadata.name,
            "namespace": svc.metadata.namespace,
            "type": svc.spec.type if svc.spec else "Unknown",
            "cluster_ip": svc.spec.cluster_ip if svc.spec else "N/A",
            "ports": [{"port": p.port, "target_port": p.target_port, "protocol": p.protocol} for p in (svc.spec.ports or [])]
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def describe_deployment(namespace: str, deployment_name: str):
    """Fetches detailed information about a specific deployment."""
    try:
        load_kube_config()
        apps_v1 = client.AppsV1Api()
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)

        return {
            "status": "success",
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "replicas": deployment.status.replicas if deployment.status else 0,
            "available_replicas": getattr(deployment.status, "available_replicas", 0),
            "containers": [{"name": c.name, "image": c.image} for c in (deployment.spec.template.spec.containers or [])]
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_node_status_and_capacity(node_name: str):
    """Fetches node health conditions and resource pressure."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        node = v1.read_node_status(node_name)

        return {
            "status": "success",
            "name": node.metadata.name,
            "conditions": [{"type": cond.type, "status": cond.status} for cond in (node.status.conditions or [])],
            "capacity": node.status.capacity if node.status else {}
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_rbac_events_and_role_bindings():
    """Fetches RBAC events, RoleBindings, and ClusterRoleBindings."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        rbac_v1 = client.RbacAuthorizationV1Api()

        # Fetch RBAC-related events
        events = v1.list_event_for_all_namespaces().items
        rbac_events = [
            {"type": event.type, "message": event.message, "object": event.involved_object.kind}
            for event in events if event.message and "denied" in event.message.lower()
        ]

        # Fetch RoleBindings & ClusterRoleBindings
        role_bindings = rbac_v1.list_role_binding_for_all_namespaces().items
        cluster_role_bindings = rbac_v1.list_cluster_role_binding().items

        return {
            "status": "success",
            "rbac_events": rbac_events,
            "role_bindings": [
                {
                    "name": rb.metadata.name,
                    "namespace": rb.metadata.namespace if rb.metadata.namespace else "N/A",
                    "role_ref": rb.role_ref.name if rb.role_ref else "Unknown"
                }
                for rb in role_bindings if rb.metadata and rb.role_ref
            ],
            "cluster_role_bindings": [
                {
                    "name": crb.metadata.name,
                    "role_ref": crb.role_ref.name if crb.role_ref else "Unknown"
                }
                for crb in cluster_role_bindings if crb.metadata and crb.role_ref
            ]
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_persistent_volumes_and_claims():
    """Fetches all Persistent Volumes (PVs) and Persistent Volume Claims (PVCs)."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()

        # Fetch PVs
        pvs = v1.list_persistent_volume().items
        pv_data = [
            {
                "name": pv.metadata.name,
                "capacity": pv.spec.capacity.get("storage", "Unknown") if pv.spec and pv.spec.capacity else "Unknown",
                "access_modes": pv.spec.access_modes if pv.spec and pv.spec.access_modes else [],
                "reclaim_policy": pv.spec.persistent_volume_reclaim_policy if pv.spec else "Unknown",
                "status": pv.status.phase if pv.status else "Unknown"
            }
            for pv in pvs
        ]

        # Fetch PVCs
        pvcs = v1.list_persistent_volume_claim_for_all_namespaces().items
        pvc_data = [
            {
                "name": pvc.metadata.name,
                "namespace": pvc.metadata.namespace,
                "access_modes": pvc.spec.access_modes if pvc.spec and pvc.spec.access_modes else [],
                "volume_name": pvc.spec.volume_name if pvc.spec and pvc.spec.volume_name else "Unbound",
                "status": pvc.status.phase if pvc.status else "Unknown"
            }
            for pvc in pvcs
        ]

        return {
            "status": "success",
            "persistent_volumes": pv_data,
            "persistent_volume_claims": pvc_data
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_running_jobs_and_cronjobs():
    """Fetches all active Jobs & CronJobs in the cluster."""
    try:
        load_kube_config()
        batch_v1 = client.BatchV1Api()

        # Fetch Jobs
        jobs = batch_v1.list_job_for_all_namespaces().items
        running_jobs = [
            {
                "name": job.metadata.name,
                "namespace": job.metadata.namespace,
                "active_pods": job.status.active if job.status and job.status.active else 0,
                "completions": job.spec.completions if job.spec and job.spec.completions else "N/A",
                "parallelism": job.spec.parallelism if job.spec and job.spec.parallelism else "N/A"
            }
            for job in jobs if job.status and job.status.active and job.status.active > 0
        ]

        # Fetch CronJobs
        batch_v1beta1 = client.BatchV1Api()
        cronjobs = batch_v1beta1.list_cron_job_for_all_namespaces().items
        cronjob_data = [
            {
                "name": cron.metadata.name,
                "namespace": cron.metadata.namespace,
                "schedule": cron.spec.schedule if cron.spec else "Unknown",
                "active_jobs": len(cron.status.active) if cron.status and cron.status.active else 0
            }
            for cron in cronjobs
        ]

        return {
            "status": "success",
            "running_jobs": running_jobs,
            "cronjobs": cronjob_data
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_ingress_resources():
    """Fetches all Ingress resources and their associated rules & annotations."""
    try:
        load_kube_config()
        networking_v1 = client.NetworkingV1Api()
        ingresses = networking_v1.list_ingress_for_all_namespaces().items

        ingress_data = [
            {
                "name": ing.metadata.name,
                "namespace": ing.metadata.namespace,
                "hosts": [rule.host for rule in ing.spec.rules] if ing.spec and ing.spec.rules else [],
                "annotations": ing.metadata.annotations if ing.metadata and ing.metadata.annotations else {}
            }
            for ing in ingresses
        ]

        return {
            "status": "success",
            "ingress_resources": ingress_data
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def check_pod_affinity(namespace: str, pod_name: str):
    """Analyzes pod affinity and anti-affinity rules for a given pod."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(pod_name, namespace)

        affinity = pod.spec.affinity if pod.spec else None
        affinity_data = {
            "node_affinity": affinity.node_affinity if affinity and affinity.node_affinity else "None",
            "pod_affinity": affinity.pod_affinity if affinity and affinity.pod_affinity else "None",
            "pod_anti_affinity": affinity.pod_anti_affinity if affinity and affinity.pod_anti_affinity else "None"
        }

        return {
            "status": "success",
            "pod": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "affinity_details": affinity_data
        }
    except client.exceptions.ApiException as e:
        return {"status": "error", "message": f"API error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
