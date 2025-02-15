# Étape 1 : Construction du frontend
FROM node:18 AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
RUN npm install bootstrap

COPY . .
RUN npm run build

# Étape 2 : Serveur Nginx pour servir l’app React
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
