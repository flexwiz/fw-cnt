#!/bin/bash -eux

# Create certificates for kubernetes
#
# Parameters :
#
# ./generate-certs.sh "../../cluster/rancher" "rancher" "rancher.sample.fr"
# ./generate-certs.sh "../../demo/rancher" "rancher" "rancher.sample.fr"
# ./generate-certs.sh "../../cluster/kubernetes" "dashboard" "dashboard.k8s.sample.fr"
# ./generate-certs.sh "../../cluster/swarm/portainer" "portainer" "portainer.swarm.sample.fr"
# ./generate-certs.sh "../../cluster/swarm/traefik" "traefik" "traefik.swarm.sample.fr"

out_dir=$1
certs_dir=$out_dir/certs
app=$2
fqdn=$3
ssl_size=2048
ssl_expire=365
ca_expire=1825

echo "===== Generate $app CA root..."


mkdir -p $certs_dir
cd $certs_dir
# openssl req -x509 -nodes -days $ca_expire -newkey rsa:$ssl_size -keyout $app.key -out $app.crt -subj "C=FR/L=LRY/O=sample/OU=IT/CN=$cn"

openssl genrsa -out $app.key $ssl_size
openssl rsa -in $app.key -out $app.key
openssl req -sha256 -new -key $app.key -out $app.csr -subj "/C=FR/L=LRY/O=sample/OU=IT/CN=$fqdn"
openssl x509 -req -sha256 -days $ca_expire -in $app.csr -signkey $app.key -out $app.crt


# # Avec Docker
# # https://github.com/superseb/omgwtfssl

# Customize the certs using the following Environment Variables:

# CA_KEY CA Key file, default ca-key.pem [1]
# CA_CERT CA Certificate file, default ca.pem [1]
# CA_SUBJECT CA Subject, default test-ca
# CA_EXPIRE CA Expiry, default 60 days
# SSL_CONFIG SSL Config, default openssl.cnf [1]
# SSL_KEY SSL Key file, default key.pem
# SSL_CSR SSL Cert Request file, default key.csr
# SSL_CERT SSL Cert file, default cert.pem
# SSL_SIZE SSL Cert size, default 2048 bits
# SSL_EXPIRE SSL Cert expiry, default 60 days
# SSL_SUBJECT SSL Subject default flexwiz.io
# SSL_DNS comma seperate list of alternative hostnames, no default [2]
# SSL_IP comma seperate list of alternative IPs, no default [2]

# [1] If file already exists will re-use.
# [2] If SSL_DNS or SSL_IP is set will add SSL_SUBJECT to alternative hostname list
volume_dir=$(pwd)
docker run --rm -v $volume_dir:/certs \
       -e CA_KEY="$app-ca-key.pem" \
       -e CA_CERT="$app-ca.pem" \
       -e CA_SUBJECT="$app root CA" \
       -e CA_EXPIRE="$ca_expire" \
       -e SSL_EXPIRE="$ssl_expire" \
       -e SSL_SUBJECT="$fqdn" \
       -e SSL_DNS="$fqdn" \
       -e SSL_KEY="$app-key.pem" \
       -e SSL_CSR="$app-key.csr" \
       -e SSL_CERT="$app-cert.pem" \
       -e SILENT="false" \
       superseb/omgwtfssl
