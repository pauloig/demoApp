server {
    listen ${LISTEN_PORT};

    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout       600s;
    fastcgi_send_timeout 600s;
    fastcgi_read_timeout 600s;

    location /static {
        alias /vol/static;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout       600s;
        fastcgi_send_timeout 600s;
        fastcgi_read_timeout 600s;
    }

    location / {
        uwsgi_read_timeout 600s;
        uwsgi_send_timeout 600s;
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    30M;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout       600s;
        fastcgi_send_timeout 600s;
        fastcgi_read_timeout 600s;
    }
}