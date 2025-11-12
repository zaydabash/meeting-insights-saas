FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Expose port
EXPOSE 5173

# Dev command (override in docker-compose)
CMD ["npm", "run", "dev"]

