#
# Expected arguments
#

# GIT_REPOSITORY:
#   GitHub repository URL (e.g., https://github.com/fogies/aws-infrastructure.git)
ARG GIT_REPOSITORY
# GIT_REPOSITORY_BRANCH:
#   Branch to use from GIT_REPOSITORY (e.g., main)
ARG GIT_REPOSITORY_BRANCH

#
# Stage arguments
#
# Confirm required arguments.
#
FROM alpine:3 as stage_required

ARG GIT_REPOSITORY
ARG GIT_REPOSITORY_BRANCH

RUN test -n "$GIT_REPOSITORY" || (echo "Argument GIT_REPOSITORY required" && false)
RUN test -n "$GIT_REPOSITORY_BRANCH" || (echo "Argument GIT_REPOSITORY_BRANCH required" && false)

#
# Stage git
#
# Obtain the web source from GitHub.
#
FROM alpine:3 AS stage_git

ARG GIT_REPOSITORY
ARG GIT_REPOSITORY_BRANCH

# Install git. Modeled on alpine/git:
# https://github.com/alpine-docker/git
RUN apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*

# Clone web repository
RUN git clone -b $GIT_REPOSITORY_BRANCH $GIT_REPOSITORY cloned_repository

#
# Stage build and serve
#
# Build and serve the project. Assumptions about the project:
# - Flask server is within directory "server_flask".
# - Dependencies installed via "pipenv sync".
# - Then serve via a "waitress-serve" command.
#   Do not rely on invoke because this creates hidden constraints on invoke tasks
#   (e.g., that task setup cannot access files that will not exist in production).
# - Will listen on port 4000.
#
# Do not use alpine for python:
# https://pythonspeed.com/articles/alpine-docker-python/
#
# Do not use slim variants of Python, as they lack git.
# Causes failure when pipenv dependencies include git dependencies.
FROM python:3.9 AS stage_build_serve

WORKDIR /cloned_repository
COPY --from=stage_git /cloned_repository .

# Install dependencies
WORKDIR /cloned_repository/server_flask
RUN pip install pipenv
RUN pipenv sync

# Ensure a FLASK_ENV environment variable
RUN echo "FLASK_ENV=production" >> .env

EXPOSE 4000
CMD ["pipenv", "run", "waitress-serve", "--port=4000", "--call", "app:create_app"]
