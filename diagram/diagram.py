# diagram.py
from urllib.request import urlretrieve

from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Pod
from diagrams.k8s.rbac import User


quarkus_url = "https://github.com/openlab-red/quarkus-mtls-quickstart/raw/master/diagram/quarkus.png"
quarkus_icon = "quarkus.png"

urlretrieve(quarkus_url, quarkus_icon)

with Diagram("Mutual TLS", show=False):

    with Cluster("Request"):
        users = [User("Users")]

    with Cluster("Mutual TLS"):
        client = Custom("http://client:8080/hello", quarkus_icon)
        server = Custom("https://server:8443/hello", quarkus_icon)
        client >> [server]
        server >> [client]

    users >> client


    