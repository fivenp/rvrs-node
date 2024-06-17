Development
`docker build -t rvrs-node .`
`docker run -it --env TOKEN=myToken --rm --name rvrs-node rvrs-node`

Production
`docker run -d --env TOKEN=myToken fivenp:rvrs-node`
