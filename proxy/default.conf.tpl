server {

    listen ${LISTEN_PORT};

    location /.well-known/acme-challenge/ {
        allow-all;
        root /var/www/certbot;
    }

}

