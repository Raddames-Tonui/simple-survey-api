docker run -d \
  --name sky_survey_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=sky_survey_db \
  -p 5432:5432 \
  -v sky_survey_pgdata:/var/lib/postgresql/data \
  postgres:latest