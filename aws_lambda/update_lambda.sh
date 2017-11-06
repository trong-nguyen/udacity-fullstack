aws lambda update-function-code \
--function-name   twitter-api \
--zip-file fileb://./app.zip \
--publish &
aws lambda update-function-code \
--function-name   foursquare-api \
--zip-file fileb://./app.zip \
--publish &
aws lambda update-function-code \
--function-name   yelp-api \
--zip-file fileb://./app.zip \
--publish