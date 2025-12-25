FROM node:20.19.6-alpine@sha256:16858294071a56ffd4cce9f17b57136cc39e41507b40e245b4f8e906f7a19463 AS builder

RUN apk add --update --no-cache python3 make g++

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install --only=production

FROM alpine:3.22.2@sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412

RUN apk add --no-cache nodejs

WORKDIR /usr/src/app

COPY --from=builder /usr/src/node_modules ./node_modules

COPY . .

EXPOSE 3000

ENTRYPOINT ["node", "/src/app/page.js"]