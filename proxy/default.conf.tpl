server {
    listen 80;
    server_name revelvolsuppliermanagement.online;

    location /.well-known/acme-challenge/ {
        allow all;
        root /usr/share/nginx/html/letsencrypt;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}




server {
    listen 443 ssl;
    server_name revelvolsuppliermanagement.online;

    ssl_certificate /etc/letsencrypt/live/revelvolsuppliermanagement.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/revelvolsuppliermanagement.online/privkey.pem;

    location /static {
        alias /vol/static;
    }

    location /media {
        alias /vol/media;
    }

    # Pass all other requests to the uWSGI server
    location / {
        uwsgi_pass              app:8000;
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    20M;
    }
}