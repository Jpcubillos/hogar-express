FROM node:24-alpine

WORKDIR /app

COPY package.json ./
# In development, we can run npm install if lockfile isn't present,
# but we will copy package-lock.json if available.
COPY package-lock.json* ./
RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
