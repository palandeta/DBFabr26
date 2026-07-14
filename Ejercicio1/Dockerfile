FROM node:25.9-alpine3.22
RUN mkdir -p /home/app
COPY . /home/app
WORKDIR /home/app
RUN npm install
EXPOSE 3000
CMD ["node", "/home/app/index.js"]
