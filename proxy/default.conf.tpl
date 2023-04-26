server {
    listen ${LISTEN_PORT};
    server_name revelvolsuppliermanagement.online;

    location /.well-known/acme-challenge/ {
        allow all;
        root /usr/share/nginx/html/letsencrypt;
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




