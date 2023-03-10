FROM alpine:3.14


##- This is a test
RUN apk add --no-cache mysql-client

##- Second test
# TO-DO: Update entrypoint 
ENTRYPOINT ["mysql"]

##- Third test >:(

# All comment types:
# // TO-DO: This is a single line comment in Java
# – – TO-DO: This is a single line comment in Haskell
# <!-- TO-DO: This is a single line comment in HTML -->
# /* TO-DO: This is a single line comment in CSS *
# % TO-DO: This is a single line comment in Erlang
