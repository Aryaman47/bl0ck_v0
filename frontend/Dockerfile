# ────────────────────────────────────────────────
# Frontend build stage
# ────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy only package.json first for caching
COPY package.json package-lock.json* ./

# Install dependencies (skip gracefully if missing)
RUN npm install --silent
RUN npm install -g sass
# Copy the rest of the frontend code
COPY . .

# Compile SCSS → CSS (skip gracefully if no sass)
RUN npx sass styles/styles.scss styles/styles.css || true

# ────────────────────────────────────────────────
# Nginx stage
# ────────────────────────────────────────────────
FROM nginx:alpine

# Copy built frontend
COPY --from=builder /app /usr/share/nginx/html

# Copy custom Nginx config for reverse proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]