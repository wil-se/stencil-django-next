FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY backend.conf /etc/nginx/sites-available/backend.conf
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]