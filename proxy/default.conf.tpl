server {

    listen ${LISTEN_PORT};

    location /.well-known/acme-challenge/ {
    root /var/www/certbot;
}
    location /static {
        alias /vol/static; 
    }

    location /media {
        alias /vol/media;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    20M;
    }
}