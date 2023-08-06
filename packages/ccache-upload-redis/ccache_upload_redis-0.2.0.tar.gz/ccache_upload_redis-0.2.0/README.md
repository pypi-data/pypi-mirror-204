# ccache-upload-redis / ccache-download-redis GitHub Action

An GitHub Action for using ccache-upload-redis / ccache-download-redis
to uploads / downloads the contents of the local ccache cache from a Redis remote storage.

## Usage

- 
- 


```yaml
name: Test ccache-download-upload-redis
on:
  workflow_dispatch:
jobs:
  # Label of the container job
  container-job:
    # Containers must run in Linux based operating systems
    runs-on: ubuntu-latest
    # Service containers to run with `container-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis:7.0.10-alpine3.17
        # Set health checks to wait until redis has started
        options: >-
          --interactive
          --hostname redis
          --add-host=host.docker.internal:host-gateway
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          --restart always
        ports:
          - 6379/tcp
          # get the rendom port via ${{ job.services.redis.ports['6379'] }}
          # https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idservices
          # https://docs.github.com/en/actions/learn-github-actions/contexts#job-context
          # Maps port 6379 on service container to the host
          #- 6379:6379

    steps:
      - name: "Set some redis settings"
        run: |
          docker network ls
          docker network ls --format='{{.ID }} {{.Name}}'
          docker inspect ${{ job.services.redis.id }}
          docker exec ${{ job.services.redis.id }} /bin/sh -c 'echo "cat /etc/redis/redis.conf ||:" '
          docker exec ${{ job.services.redis.id }} /bin/sh -x -c 'mkdir -p /etc/redis ||: '
          docker exec ${{ job.services.redis.id }} /bin/sh -x -c 'echo "save 60 100" >> /etc/redis/redis.conf'
          docker exec ${{ job.services.redis.id }} /bin/sh -x -c 'echo "loglevel verbose" >> /etc/redis/redis.conf'
          docker exec ${{ job.services.redis.id }} /bin/sh -x -c 'echo "# see https://github.community/t/how-do-i-properly-override-a-service-entrypoint/17435/8" >> /etc/redis/redis.conf'
          docker exec ${{ job.services.redis.id }} /bin/sh -x -c 'echo "# https://hub.docker.com/_/redis" >> /etc/redis/redis.conf'
          docker kill --signal=SIGHUP ${{ job.services.redis-y9g98g58d.id }} ||:

      - name: Checkout repository
        uses: actions/checkout@v3

      - upload-test: "upload-test"
        run: |
          ccache-upload-redis
        env: |
          REDIS_CONF='localhost:${{ job.services.redis.ports['6379'] }}'
          CCACHE_DIR='~/.cache/ccache'
          
      - download-test: "download-test"
        run: |
          ccache-download-redis
        env: |
          REDIS_CONF='localhost:${{ job.services.redis.ports['6379'] }}'
          CCACHE_DIR='~/.cache/ccache'

      - name: Connect REDIS
        uses: ./
        with:
          host: ${{ variable.REDIS_SERVER }}
          username: ${{ variable.USERNAME }}
          password: ${{ variable.PASSWORD }}
          ccachedir: ${{ variable.CCACHEDIR }}

