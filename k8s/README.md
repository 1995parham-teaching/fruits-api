# Kubernetes manifests

Deploys the Fruits API with a persistent SQLite database.

| File                  | Purpose                                                            |
| --------------------- | ------------------------------------------------------------------ |
| `deployment.yaml`     | Runs the API container (non-root, with health probes).             |
| `service.yaml`        | `ClusterIP` service exposing the app on port 80 → container 8000.  |
| `pvc.yaml`            | `PersistentVolumeClaim` holding the SQLite file across restarts.   |
| `kustomization.yaml`  | Bundles the above and sets the container image.                    |

## Deploy

1. Point the manifests at your published image. Either edit `image:` in
   `deployment.yaml` directly, or use kustomize:

   ```bash
   cd k8s
   kustomize edit set image ghcr.io/OWNER/REPO=ghcr.io/<your-org>/<repo>:latest
   ```

2. Apply:

   ```bash
   kubectl apply -k k8s/
   ```

3. Verify and try it:

   ```bash
   kubectl rollout status deployment/fruits-api
   kubectl port-forward svc/fruits-api 8000:80
   curl http://localhost:8000/fruits
   ```

## Notes

- **Single replica by design.** SQLite is file-based and single-writer, backed by a
  `ReadWriteOnce` volume, so the Deployment uses `replicas: 1` and a `Recreate` strategy.
  To scale horizontally, switch `DATABASE_URL` to a networked database (e.g. PostgreSQL)
  — the application reads it straight from the environment.
- If your cluster has no default `StorageClass`, add `storageClassName` to `pvc.yaml`.
- To expose the service externally, add an `Ingress` or change the Service `type` to
  `LoadBalancer`.
