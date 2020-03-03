# Quarkus Mutual TLS Quickstart


## Build

```
 mvn clean package
```

## Build Native

```
 mvn clean package -Pnative
```

## Run

### Server

Listening on 8443.

* JVM 
  ```
    java -jar target/rest-server-tck-1.0-SNAPSHOT-runner.jar
  ```
* Native
  ```
    ./target/rest-server-tck-1.0-SNAPSHOT-runner
  ```
 
### Client

Listening on 8080.

* JVM 
  ```
    java -jar target/rest-client-tck-1.0-SNAPSHOT-runner.jar
  ```
* Native
  ```
    ./target/rest-client-tck-1.0-SNAPSHOT-runner
  ```
  
## Test

```
 curl http://localhost:8080/hello
 hello
```



