FROM alpine:3.14


##- This is a test
RUN apk add --no-cache mysql-client

##- Second test
# TO-DO: Update entrypoint 
ENTRYPOINT ["mysql"]

##- Third test >:(
    