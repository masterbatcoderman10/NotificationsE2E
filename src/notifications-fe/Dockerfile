FROM node:14.15.4-alpine3.12 as build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . ./
RUN npm run build

FROM nginx:1.19.6-alpine
COPY --from=build /app/public /usr/share/nginx/html