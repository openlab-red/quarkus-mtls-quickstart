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

### Launch 
* Server
  ```
    java -jar target/rest-server-tck-1.0-SNAPSHOT-runner.jar
  ```
  
* Client
  ```
    java -jar target/rest-client-tck-1.0-SNAPSHOT-runner.jar
  ```
  
### Launch Native

* Server
  ```
    ./target/rest-server-tck-1.0-SNAPSHOT-runner
  ```
  
* Client
  ```
    ./target/rest-client-tck-1.0-SNAPSHOT-runner
  ```

## Test

```
 curl http://localhost:8080/hello
 hello
```



