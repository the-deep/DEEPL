FROM nginx:1.13

RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | \
   tee /etc/apt/sources.list.d/backports.list && \
   apt-get update -y && \
   apt-get install -y python-certbot-nginx -t stretch-backports

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
