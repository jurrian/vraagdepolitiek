FROM node:10.11-alpine
EXPOSE 3000
CMD yarn serve out -p 3000

COPY . /opt/vraagdepolitiek/frontend
WORKDIR /opt/vraagdepolitiek/frontend
RUN yarn install && yarn run build && yarn run export
