FROM alpine:latest as builder

RUN apk add --no-cache yarn

COPY unvesting-app /app

WORKDIR /app

RUN yarn install --ignore-optional
RUN yarn add npx
RUN yarn build


FROM nginx:latest

COPY --from=builder /app/dist /usr/share/nginx/html
