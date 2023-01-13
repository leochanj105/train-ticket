FROM openresty/openresty:trusty

RUN /bin/ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf

COPY static /usr/share/nginx/html