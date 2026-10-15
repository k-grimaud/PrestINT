# check that this version matches with that in apps/frontend/.nvmrc
FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

CMD ["npm","run","dev","--","--host"]