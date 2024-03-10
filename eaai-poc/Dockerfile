FROM node:18-alpine

WORKDIR /eaai-poc

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

RUN npm run build

# CMD ["npm", "run", "dev", "--", "--host"]
CMD ["npm", "run", "preview", "--", "--host"]