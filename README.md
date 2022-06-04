# Lunchbox
A web portal that connects local home masterchefs with people who wish to eat healthy home cooked meals but are too busy to cook daily. 

Check it out here - [bit.ly/lunchbox-app](https://www.bit.ly/lunchbox-app)

## Demo


https://user-images.githubusercontent.com/29813712/171992031-f153228e-5d50-4314-88db-24554bf68112.mp4



## Commands 
### Kill flask process
`ps aux | grep 'python'`
`kill -9 <PID>`

### heroku python
`heroku run python -a lunchbox-app`

### heroku psql
`heroku pg:psql -a lunchbox-app`

### local psql
`psql lunchbox postgres`

### heroku open
`heroku open -a lunchbox-app` 

### migrate db
`flask db stamp head`
`flask db migrate`
`flask db upgrade`

### create tables
`from app import db`
`db.create_all()`
`exit()`

```
ALTER TABLE meals ADD COLUMN create_time_holder TIMESTAMP without time zone NULL;

UPDATE meals SET create_time_holder = updated_at::TIMESTAMP;

ALTER TABLE meals ALTER COLUMN updated_at TYPE TIMESTAMP without time zone USING create_time_holder;

ALTER TABLE meals DROP COLUMN create_time_holder;
```

## Links
https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

## Video
https://www.youtube.com/watch?v=w25ea_I89iM&t=297s
