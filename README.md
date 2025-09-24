# WingzPH
A solution for managing ride information using django rest framework.

## Description

An API that returns a list for Rides. The API


## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Bonus Question

```
WITH
	RIDES_AND_DRIVER_WITH_TRIPS_MORE_THAN_HOUR AS (
		WITH
			RIDES_WITH_PICKUP_TO_DROPOFF AS (
				SELECT
					ID_RIDE_ID,
					MIN(CREATED_AT) AS MIN_TIMESTAMP,
					MAX(CREATED_AT) AS MAX_TIMESTAMP
				FROM
					RIDELIST_RIDE_EVENT
				WHERE
					DESCRIPTION = 'Changed status to Pickup'
					OR DESCRIPTION = 'Changed status to Dropoff'
				GROUP BY
					ID_RIDE_ID
				ORDER BY
					ID_RIDE_ID
			)
		SELECT
			A.ID_RIDE_ID,
			B.ID_DRIVER_ID,
			CASE
				WHEN EXTRACT(
					EPOCH
					FROM
						(MAX_TIMESTAMP - MIN_TIMESTAMP)
				) / 3600 > 1 THEN 'Yes'
				ELSE 'No'
			END AS MORE_THAN_1_HOURS
		FROM
			RIDES_WITH_PICKUP_TO_DROPOFF A
			INNER JOIN RIDELIST_RIDE B ON A.ID_RIDE_ID = B.ID_RIDE
	)
SELECT
	COUNT(A.ID_DRIVER_ID) AS COUNT_OF_TRIPS_MORE_THAN_1_HOUR,
	B.FIRST_NAME
FROM
	RIDES_AND_DRIVER_WITH_TRIPS_MORE_THAN_HOUR A
	INNER JOIN RIDELIST_USER B ON A.ID_DRIVER_ID = B.ID_USER
WHERE
	MORE_THAN_1_HOURS = 'Yes'
GROUP BY
	A.ID_DRIVER_ID,
	B.FIRST_NAME
ORDER BY
	A.ID_DRIVER_ID;

```
Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
