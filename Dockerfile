FROM node:current-buster-slim

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

CMD ["node", "index.js"]