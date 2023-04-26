server {

    listen ${LISTEN_PORT};

    location /.well-known/acme-challenge/ {
        allow-all;
        root /usr/share/nginx/html/letsencrypt;
    }

}

