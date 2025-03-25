FROM node:18

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve static files
RUN npm install -g serve
CMD ["serve", "-s", "build"]
