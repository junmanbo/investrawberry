# 빌드 스테이지
FROM node:18 as build-stage

WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY ./ /app/

RUN npm run build

# 배포 스테이지
FROM nginx:stable

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
