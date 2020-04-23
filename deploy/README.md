# Deploy

## Create a namespace

```
    oc new-project mtls
```

## Create certificate

```
mkdir -p tls/{ca,server,client}
```

### Certificate Autority

This section is to simulate a private certificate authority.

1. Certificate Authority (CA)

    ```
    openssl req -new -newkey rsa:2048 -x509 -keyout tls/ca/ca.key -out tls/ca/ca.crt -days 365 -subj "/CN=mycompany.com"
    ```

2. Create a Truststore

    ```
    keytool -import -storepass password -file tls/ca/ca.crt -alias mycompany.com -keystore tls/ca/truststore
    ```

### Server Certificate

1. Server Key

    ```
    keytool -genkeypair -storepass password -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -keystore tls/server/server.keystore
    ```

2. Certificate Signing Request (CSR)

    ```
    keytool -certreq -storepass password -keyalg rsa -alias server -keystore tls/server/server.keystore -file tls/server/server.csr
    ```

3. Certificate Authority Sign

    ```
    openssl x509 -req -CA tls/ca/ca.crt -CAkey tls/ca/ca.key -in tls/server/server.csr -out tls/server/server.crt -days 365 -CAcreateserial
    
    keytool -import -v -trustcacerts -alias root -file tls/ca/ca.crt -keystore tls/server/server.keystore
    keytool -import -v -trustcacerts -alias server -file tls/server/server.crt -keystore tls/server/server.keystore
    ```

    3.1 Verify the chain

        ```
        keytool -list -v -keystore tls/server/server.keystore
        ```

4. Import to truststore

    ```
    keytool -import -storepass password -file tls/server/server.crt -alias server -keystore tls/ca/truststore
    ```

### Client Certificate

1. Client Key

    ```
    keytool -genkeypair -storepass password -keyalg RSA -keysize 2048 -dname "CN=client" -alias client -keystore tls/client/client.keystore
    ```

2. Certificate Signing Request (CSR)

    ```
    keytool -certreq -storepass password -keyalg rsa -alias client -keystore tls/client/client.keystore -file tls/client/client.csr
    ```

3. Certificate Authority Sign

    ```
    openssl x509 -req -CA tls/ca/ca.crt -CAkey tls/ca/ca.key -in tls/client/client.csr -out tls/client/client.crt -days 365 -CAcreateserial

    keytool -import -v -trustcacerts -alias root -file tls/ca/ca.crt -keystore tls/client/client.keystore
    keytool -import -v -trustcacerts -alias client -file tls/client/client.crt -keystore tls/client/client.keystore
    ```

    3.1 Verify the chain

        ```
        keytool -list -v -keystore tls/client/client.keystore
        ```

4. Import to truststore

    ```
    keytool -import -storepass password -file tls/client/client.crt -alias client -keystore tls/ca/truststore
    ```

## Create Secret

1. Server Secret

   ```
   oc create secret generic server --from-file=tls/server/
   ```

2. Client Secret

   ```
   oc create secret generic client --from-file=tls/client/
   ```

3. Truststore Secret

   ```
   oc create secret generic truststore --from-file=tls/ca/truststore
   ```

## Deploy Server Application

### Server

1. Build

    JVM:
    ```
    oc new-build --name=server registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift~https://github.com/openlab-red/quarkus-mtls-quickstart#kubernetes-config --context-dir=/quarkus-server-mtls
    ```

    Native:
    ```
    oc new-build --name=server quay.io/quarkus/ubi-quarkus-native-s2i:19.3.1-java11~https://github.com/openlab-red/quarkus-mtls-quickstart --context-dir=/quarkus-server-mtls
    oc patch bc/server -p '{"spec":{"resources":{"limits":{"cpu":"6", "memory":"6Gi"}}}}'
    ```

2. Deploy

    ```
    oc apply -f manifest/server/
    ```

    > If you built native, the ConfigMap volumeMount on the Deployment is `/home/quarkus`
    >
    > To use the native Deployment launch also: `oc apply -f manifest/server/native/`

### Client

1. Build

    JVM:
    ```
    oc new-build --name=client registry.access.redhat.com/redhat-openjdk-18/openjdk18-openshift~https://github.com/openlab-red/quarkus-mtls-quickstart --context-dir=/quarkus-client-mtls
    ```

    Native:
    ```
    oc new-build --name=client quay.io/quarkus/ubi-quarkus-native-s2i:19.3.1-java11~https://github.com/openlab-red/quarkus-mtls-quickstart --context-dir=/quarkus-client-mtls
    oc patch bc/client -p '{"spec":{"resources":{"limits":{"cpu":"6", "memory":"6Gi"}}}}'
    ```

2. Deploy

    ```
    oc apply -f manifest/client/
    ```

    > If you built native, the ConfigMap volumeMount on the Deployment is `/home/quarkus`
    >
    > To use the native Deployment launch also: `oc apply -f manifest/client/native/`


## Test it

```
curl http://client-mtls.apps-crc.testing/hello-client
hello from server
```
