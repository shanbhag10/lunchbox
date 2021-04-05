# lunchbox
A web app that connects local home chefs to busy folks for healthy home-made food

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