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
# - Web app is within directory "web_registry".
# - Dependencies installed via a "yarn install".
# - Also require dependencies from "web_shared".
# - Build via a "yarn prod_build".
# - Then serve via a "yarn prod_serve".
# - Will listen on port 3000.
#
FROM node:15-alpine AS stage_build_serve

WORKDIR /cloned_repository
COPY --from=stage_git /cloned_repository .

# Install dependencies
WORKDIR /cloned_repository/web_registry
RUN yarn install
WORKDIR /cloned_repository/web_shared
RUN yarn install

# Pre-build web app, ensure the "dist" directory exists
WORKDIR /cloned_repository/web_registry
RUN yarn prod_build
RUN test -d dist

EXPOSE 3000
CMD ["yarn", "prod_serve"]
