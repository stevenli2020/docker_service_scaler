# docker_service_scaler

Docker Service Scaler provides a set of RESTFul API, which manages docker swarm service scaling. This scaler can work with Grafana Alert Webhook mode, so the alert can automatically trigger service scaling. 

docker run -dit -m 32MB --name scaler -p 8080:80 -v /var/run/docker.sock:/var/run/docker.sock -w /app stevenli2019/docker_service_scaler:1.0
