FROM alpine:latest

MAINTAINER cmb87403@web.de

RUN apk add --update nodejs npm
# RUN apk add --update nodejs-current npm

RUN addgroup -S node && adduser -S node -G node
RUN mkdir /home/node/app

WORKDIR /home/node/app

COPY dist/demoapp /home/node/app/

RUN chown -R node /home/node/app/

USER node

RUN npm ci
EXPOSE 5000

CMD ["node", "app.js"]
