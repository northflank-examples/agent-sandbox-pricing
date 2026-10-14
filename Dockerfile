# Static web estimator. Deploy on Northflank as a combined service (port 8080).
FROM nginx:1.27-alpine
COPY web/nginx.conf /etc/nginx/conf.d/default.conf
COPY web/index.html web/app.js web/model.js web/styles.css /usr/share/nginx/html/
COPY data/pricing.json /usr/share/nginx/html/data/pricing.json
EXPOSE 8080
