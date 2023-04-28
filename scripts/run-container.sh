APP_NAME=${1:?"Specify 'APP_NAME' as argv[1]"}
HEROKU_API_KEY=${2:?"Specify 'HEROKU_API_KEY' as argv[2]"}
APP_ENV=${3:?"Specify 'APP_ENV' as argv[3]"}
M_TURK_PREVIEW_URL_PREFIX=${4:?"Specify 'M_TURK_PREVIEW_URL_PREFIX' as argv[4]"}



docker run -d --rm --init -v $APP_NAME-volume:/mephisto/data \
    --name $APP_NAME \
    -e HEROKU_API_KEY=$HEROKU_API_KEY \
    -e APP_ENV=$APP_ENV \
    $APP_NAME;
    
timeout 1800 \
    sh -c "while ! docker logs -f $(docker ps -q --filter ancestor=$APP_NAME --format="{{.ID}}")| grep -q '$M_TURK_PREVIEW_URL_PREFIX'; \
            do sleep 1; done";


docker logs $(docker ps -q --filter ancestor=$APP_NAME --format="{{.ID}}");
