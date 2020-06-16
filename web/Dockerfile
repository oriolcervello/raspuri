FROM nginx

RUN rm /etc/nginx/conf.d/default.conf \
&& rm /etc/nginx/nginx.conf

COPY web-rasp/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/

# sudo docker build -t webrasp .
# sudo docker run --name webR --rm -p 80:80 -d -v /home/ori/OUT:/usr/share/nginx/html/OUT webrasp




