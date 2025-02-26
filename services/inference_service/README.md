pip install -r requirements.txt

docker compose build


navigates to kubernets dir

kubectl apply -f cassandra-statefulset.yaml
kubectl apply -f inference-service-deployment.yaml