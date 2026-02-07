# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies.
COPY package.json package-lock.json ./
RUN npm ci

# Copy source and build.
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine

# Copy built assets from builder stage.
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration to handle React Router.
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
