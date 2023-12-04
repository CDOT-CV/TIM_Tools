FROM redis:alpine

ENV WORKDIR /app

WORKDIR $WORKDIR

COPY . .

CMD ["redis-server", "redis.conf"]