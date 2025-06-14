# Use Node.js 18 alpine image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Create package.json if it doesn't exist
RUN echo '{ \
  "name": "taskmaster-frontend", \
  "version": "1.0.0", \
  "description": "TaskMaster Pro Frontend", \
  "main": "server.js", \
  "scripts": { \
    "start": "node server.js", \
    "dev": "nodemon server.js" \
  }, \
  "dependencies": { \
    "express": "^4.18.2", \
    "cors": "^2.8.5" \
  } \
}' > package.json

# Install dependencies
RUN npm install

# Copy application files
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership of the app directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start the application
CMD ["npm", "start"]
