FROM node:24-alpine AS builder
WORKDIR /app

COPY frontend/ ./frontend
WORKDIR /app/frontend

RUN npm install -g @quasar/cli \
  && npm install
RUN quasar build

FROM nginx:stable-alpine

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/frontend/dist/spa /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]