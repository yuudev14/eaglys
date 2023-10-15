FROM node:18.17.1

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Create a smaller image for production
FROM node:14
WORKDIR /app
COPY --from=build /app . 
EXPOSE 3000
CMD ["npm", "start"]