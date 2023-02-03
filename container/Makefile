# Borrowed from:
# https://github.com/silven/go-example/blob/master/Makefile
# https://vic.demuzere.be/articles/golang-makefile-crosscompile/

IMAGE = "alliance-auth"
VERSION = "1.0.25"
AA_VERSION = "v3.3.0"

# Symlink into GOPATH
GITHUB_USERNAME=wonko

container:
	docker buildx build --build-arg imageTag=${AA_VERSION} --platform=linux/amd64 -t ${GITHUB_USERNAME}/${IMAGE}:${AA_VERSION}-${VERSION} -t ${GITHUB_USERNAME}/${IMAGE}:latest --push .
