# Use a more recent Node.js version
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . ./

# Set environment variable
ENV VITE_API_URL=/api

# Build the app and output logs
RUN npm run build || { echo 'Build failed'; exit 1; }

# Output the contents of /app after build
RUN echo "=== Contents of /app after build ===" && ls -la /app

# Output the contents of the dist directory
RUN echo "=== Contents of /app/dist ===" && ls -la /app/dist

# Ensure 'dist' directory exists
RUN if [ ! -d "dist" ]; then echo "Build failed: dist directory not found"; exit 1; fi

FROM nginx:alpine

# Copy the built files from the dist directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3173