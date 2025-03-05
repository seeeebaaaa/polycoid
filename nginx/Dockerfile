FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/ssl

COPY .secret/polycoid.com_ssl_certificate.crt.pem /etc/nginx/ssl/public.crt.pem
COPY .secret/*.polycoid.com_private_key.key.pem /etc/nginx/ssl/private.key.pem