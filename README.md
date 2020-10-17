# SearchDevelopers
sample code to search developers with github api v3 
this is just sample code to use github api v3. 

## how to use
```cp .env.example .env ```

set your access token on .env file. Then run shell script.

```bash start.sh```

## how to customize
`main.py`
change queries whatever you want.
```
queries = ['vue', 'laravel', 'php', 'javascript', 'serviceworker']
```

# main.py doing what?
based on queries , it requests github api search users while handling rate limits.
Simply output json result.

# format_csv.py doing what?
just convert json files to csv as human readable source

# get_user_details.py doing what?
from csv files, get each user row and request github api for getting user detail information while handling rate limits
 