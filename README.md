# Quarkus Mutual TLS Quickstart

![mutual_tls.png](diagram/mutual_tls.png)

## Local Deployment

### Build

* JVM 
  ```
  mvn clean package -Dquarkus.profile=dev
  ```
* Native
  ```
  mvn clean package -Pnative -Dquarkus.profile=dev
  ```

### Run

On Server listening on 8443.

* JVM 
  ```
    java -jar target/quarkus-server-mtls-1.0-SNAPSHOT-runner.jar 
  ```
* Native
  ```
    ./target/quarkus-server-mtls-1.0-SNAPSHOT-runner
  ```
 
On Client listening on 8080.

* JVM 
  ```
    java -jar target/quarkus-client-mtls-1.0-SNAPSHOT-runner.jar
  ```
* Native
  ```
    ./target/quarkus-client-mtls-1.0-SNAPSHOT-runner
  ```
  
### Test

```
 curl http://localhost:8080/hello-client
 hello from server
```

## On Kubernetes / OpenShift

[Deploy](./deploy/README.md)