FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/ssl

COPY ./polycoid.com_ssl_certificate.crt.pem /etc/nginx/ssl/public.crt.pem
COPY ./*.polycoid.com_private_key.key.pem /etc/nginx/ssl/private.key.pem

# EXPOSE 443
# EXPOSE 80