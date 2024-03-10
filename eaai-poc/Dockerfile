FROM node:18-alpine

WORKDIR /eaai-poc

COPY package*.json ./

# RUN npm install -g http-serve
RUN npm install

COPY . .

RUN npm run build

# EXPOSE 8080
EXPOSE 5173

# CMD ["http-server", "dist"]
CMD ["npm", "run", "dev", "--", "--host"]