rm app.zip &
zip -r app.zip twitter_handler.py trongn requests &
aws lambda update-function-code \
--function-name   twit \
--zip-file fileb:///Users/nguyentrong/Dropbox/Projects/udacity-fullstack/aws_lambda/app.zip \
--publish